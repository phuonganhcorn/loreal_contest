from django.shortcuts import render, redirect
from django.http import JsonResponse
from skincare.models import UserProfile, SkinAnalysisImage, SkinAnalysis
import json
import openai
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import random
import os
from loguru import logger
from dotenv import load_dotenv
load_dotenv()
# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logger
logger.add("logs/logfile.log", rotation="1 MB", level="DEBUG")  # Log file rotation example

def skin_analysis(request):
    return render(request, 'skincare/skin_analysis.html')

@csrf_exempt
@login_required
def skin_analysis_view(request):
    if request.method == 'POST':
        try:
            # Validate image upload
            if 'image' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'No image uploaded'
                }, status=400)
            
            uploaded_image = request.FILES['image']
            
            # Enhanced image validation
            if not uploaded_image:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid image file'
                }, status=400)
            
            # Size validation
            if uploaded_image.size > 10 * 1024 * 1024:  # 10MB max
                return JsonResponse({
                    'success': False,
                    'error': 'Image size too large. Maximum 10MB allowed.'
                }, status=400)
            
            # File type validation
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if uploaded_image.content_type not in allowed_types:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid image type. Only JPEG and PNG allowed.'
                }, status=400)
            
            # Verify user profile
            # try:
            #     profile = UserProfile.objects.get(user=request.user)
            # except UserProfile.DoesNotExist:
            #     return JsonResponse({
            #         'success': False,
            #         'error': 'Please complete your profile first.'
            #     }, status=403)
            
            # Save the uploaded image
            # try:
            #     analysis_image = SkinAnalysisImage.objects.create(
            #         user=request.user,
            #         image=uploaded_image
            #     )
            # except Exception as storage_error:
            #     logger.error(f"Image storage error: {str(storage_error)}")
            #     return JsonResponse({
            #         'success': False,
            #         'error': 'Failed to save image. Please try again.'
            #     }, status=500)
            
            # Perform AI Analysis 
            try:
                analysis_results = perform_skin_analysis()
                # analysis_results = perform_skin_analysis(analysis_image.image.path)
            except Exception as analysis_error:
                logger.error(f"AI Analysis Error: {str(analysis_error)}")
                return JsonResponse({
                    'success': False,
                    'error': 'AI analysis failed. Please try a different image.'
                }, status=500)
            
            # Save analysis results
            # try:
            #     skin_analysis = SkinAnalysis.objects.create(
            #         user=request.user,
            #         skin_type=analysis_results.get('skin_type', ''),
            #         skin_concerns=json.dumps(analysis_results.get('concerns', [])),
            #         recommendations=analysis_results.get('recommendations', ''),
            #         confidence_score=analysis_results.get('confidence', 0.0)
            #     )
            # except Exception as save_error:
            #     logger.error(f"Analysis save error: {str(save_error)}")
            #     return JsonResponse({
            #         'success': False,
            #         'error': 'Failed to save analysis results.'
            #     }, status=500)
            
            return JsonResponse({
                'success': True,
                'analysis': {
                    'skin_type': analysis_results.get('skin_type', ''),
                    'concerns': analysis_results.get('concerns', []),
                    'confidence': analysis_results.get('confidence', 0.0),
                    'recommendations': analysis_results.get('recommendations', ''),
                }
            })
        
        except Exception as unexpected_error:
            # Catch-all for any unexpected errors
            logger.error(f"Unexpected Skin Analysis Error: {str(unexpected_error)}")
            
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred. Please try again later.'
            }, status=500)
    
    # # Render the skin analysis page for GET requests
    # return render(request, 'skincare/skin_analysis.html')



def perform_skin_analysis():
    """
    Enhanced placeholder function for AI skin analysis
    """
    try:
        
        # Existing random analysis logic
        skin_types = ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive']
        concerns = [
            'Acne', 'Wrinkles', 'Hyperpigmentation', 
            'Redness', 'Uneven Skin Tone', 'Large Pores'
        ]
        
        return {
            'skin_type': random.choice(skin_types),
            'concerns': random.sample(concerns, k=random.randint(1, 3)),
            'recommendations': generate_recommendations(),
            'confidence': round(random.uniform(0.7, 1.0), 2)
        }
    
    except Exception as e:
        logger.error(f"AI Analysis Error: {str(e)}")
        return {
            'skin_type': 'Unknown',
            'concerns': [],
            'recommendations': 'Unable to perform analysis',
            'confidence': 0.0
        }

def generate_recommendations(skin_type=None):
    """
    Generate recommendations with optional skin type consideration
    """
    recommendation_categories = {
        'Cleansing': {
            'general': [
                "Use a gentle cleanser twice daily",
                "Choose a cleanser suited to your skin type",
                "Avoid harsh scrubbing"
            ],
            'Oily': [
                "Use a foaming cleanser",
                "Cleanse morning and night",
                "Use salicylic acid-based cleansers"
            ],
            'Dry': [
                "Use a creamy, hydrating cleanser",
                "Avoid hot water",
                "Use gentle, fragrance-free cleansers"
            ]
        },
        'Protection': [
            "Apply sunscreen with SPF 30+ every morning",
            "Reapply sunscreen every 2 hours",
            "Use protective clothing and seek shade"
        ],
        'Hydration': {
            'general': [
                "Drink at least 8 glasses of water daily",
                "Use hyaluronic acid for extra moisture"
            ],
            'Dry': [
                "Use a rich, ceramide-based moisturizer",
                "Apply moisturizer to damp skin"
            ],
            'Oily': [
                "Use lightweight, non-comedogenic moisturizers",
                "Use gel-based hydrators"
            ]
        },
        'Maintenance': [
            "Exfoliate 1-2 times per week",
            "Use a weekly face mask",
            "Get 7-8 hours of sleep"
        ]
    }
    
    # Prevent infinite recursion
    if skin_type is None:
        skin_type = random.choice(['Oily', 'Dry', 'Normal', 'Combination', 'Sensitive'])
    
    customized_recommendations = []
    
    for category, options in recommendation_categories.items():
        if isinstance(options, dict):
            # Prioritize skin type specific recommendations
            skin_specific = options.get(skin_type, [])
            general = options.get('general', [])
            
            # Combine and choose
            combined = skin_specific + general
            customized_recommendations.append(random.choice(combined))
        else:
            # For categories without skin type specifics
            customized_recommendations.append(random.choice(options))
    
    return ". ".join(customized_recommendations)