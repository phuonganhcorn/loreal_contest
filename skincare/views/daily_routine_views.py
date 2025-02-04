from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from skincare.models import SkinCareRoutine, UserProfile
import json
import openai
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import os
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logger
logger.add("logs/logfile.log", rotation="1 MB", level="DEBUG")  # Log file rotation example

def routine(request):
    return render(request, 'skincare/routine.html')

@csrf_exempt
@login_required
def generate_routine(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get user preferences
            # profile = UserProfile.objects.get(user=request.user)
            skin_type = data.get('skinType')
            age = data.get('age')
            gender = data.get('gender')
            concerns = data.get('concerns', [])
            climate = data.get('climate')
            # Generate routine using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"""Generate a detailed skincare routine for:
                        Skin Type: {skin_type}
                        Age: {age}
                        Concerns: {', '.join(concerns)}
                        Climate: {climate}
                        Gender: {gender}
                        
                        Please provide:
                        1. Morning routine (3-5 steps)
                        2. Noon routine (2-3 steps)
                        3. Night routine (4-6 steps)
                        4. Diet recommendations
                        
                            
                        Format the response in clear markdown with:
                        - Use # for main headings
                        - Use ## for subheadings
                        - Use - for list items
                        - Use **bold** for emphasis
                        - Ensure clear, readable formatting`
                        """
                }]
            )
            
            # Parse response and save to database
            recommendations = response.choices[0].message.content
            
            # SkinCareRoutine.objects.create(
            #     user=request.user,
            #     morning_routine=recommendations['morning'],
            #     noon_routine=recommendations['noon'],
            #     night_routine=recommendations['night'],
            #     diet_recommendations=recommendations['diet']
            # )
            
            return JsonResponse({
                'success': True,
                'recommendations': recommendations
            })
        
        
        except Exception as e:
            logger.error(f"Generate Routine Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    

@login_required
def save_routine(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            completed = data.get('completed', False)
            
            routine = SkinCareRoutine.objects.get(
                user=request.user,
                date=date
            )
            routine.completed = completed
            routine.save()
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            logger.error(f"Save Routine Error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False}) 

