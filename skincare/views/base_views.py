from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from skincare.models import  UserProfile
import json
import openai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from PIL import Image
from loguru import logger
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logger
logger.add("logs/logfile.log", rotation="1 MB", level="DEBUG")  # Log file rotation example

def home(request):
    return render(request, 'skincare/home.html')


def notifications(request):
    return render(request, 'skincare/notifications.html')



@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Add logging to help diagnose the issue
        logger.info(f"Login attempt - Username: {username}")
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            logger.info(f"User found: {user.username}")
        except User.DoesNotExist:
            logger.warning(f"User not found: {username}")
            return JsonResponse({
                'success': False,
                'error': 'User does not exist'
            }, status=400)
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f"User logged in successfully: {username}")
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('skincare:home') 
            })
        else:
            logger.warning(f"Authentication failed for user: {username}")
            return JsonResponse({
                'success': False,
                'error': 'Invalid username or password'
            }, status=400)
    
    # If not a POST request
    return render(request, 'skincare/login.html')

def register(request):
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Username is already taken. Please choose a different username.'
                })
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Email is already registered. Please use a different email address.'
                })

            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Account created successfully!'
            })

        except Exception as e:
            logger.error(f"Register Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return render(request, 'skincare/register.html')



@login_required
def get_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'profile': {
                'skinType': profile.skin_type,
                'age': profile.age,
                'gender': profile.gender,
                'concerns': profile.concerns
            }
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Profile not found'
        }) 
    


@require_http_methods(["POST"])
def save_profile(request):
    try:
        # Parse incoming JSON data
        data = json.loads(request.body)
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'skin_type': data.get('skin_type'),
                'age': data.get('age'),
                'gender': data.get('gender')
            }
        )
        
        # Update existing profile
        if not created:
            profile.skin_type = data.get('skin_type')
            profile.age = data.get('age')
            profile.gender = data.get('gender')
            profile.save()
        
        # Save concerns
        concerns = data.get('concerns', [])
        profile.concerns = json.dumps(concerns)
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile saved successfully'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
