from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from skincare.models import SkinCareRoutine, UserProfile
import json
import openai
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
import random
import os
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_API_KEY')
# Configure logger
logger.add("logs/logfile.log", rotation="1 MB", level="DEBUG")  # Log file rotation example

def calendar(request):
    return render(request, 'skincare/calendar.html')

@login_required
@csrf_exempt
def generate_monthly_routine(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            skinType = data.get('skinType')
            age = data.get('age')
            concerns = data.get('concerns', [])
            climate = data.get('climate')
                        
            # Get the number of days in the month
            
            routines = []

            # Generate new routine using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"""Generate a detailed skincare routine for:
                        Skin Type: {skinType}
                        Age: {age}
                        Climate: {climate}
                        Concerns: {', '.join(concerns)}
                        Date: {date}
                        
                        Please provide output strictly in below structure:
                        1. Morning routine (3-5 steps) \n
                        2. Noon routine (2-3 steps) \n
                        3. Night routine (4-6 steps) \n
                        4. Diet recommendations: """
                }]
            )
            
                    
            # # Save to database
            # SkinCareRoutine.objects.create(
            #     user=request.user,
            #     date=date,
            #     morning_routine=routine['morning'],
            #     noon_routine=routine['noon'],
            #     night_routine=routine['night'],
            #     diet_recommendations=routine['diet']
            # )

            routines = response.choices[0].message.content
            
            return JsonResponse({
                'success': True,
                'routines': routines
            })
            
        except Exception as e:
            logger.error(f"Error generating monthly routine: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
            
