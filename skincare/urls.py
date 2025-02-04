from django.urls import path
from .views.daily_routine_views import *
from .views.monthly_routine_views import *
from .views.skin_analysis_views import *
from .views.base_views import *
app_name = 'skincare'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('routine/', routine, name='routine'),
    path('register/', register, name='register'),
    path('api/generate-routine', generate_routine, name='generate_routine'),
    path('api/save-routine/', save_routine, name='save_routine'),
    path('calendar/', calendar, name='calendar'),
    path('api/generate-monthly-routine', generate_monthly_routine, name='generate_monthly_routine'),
    path('notifications/', notifications, name='notifications'),
    path('api/save-profile/', save_profile, name='save_profile'),
    path('api/get-profile/', get_user_profile, name='get_profile'),
    path('skin-analysis/', skin_analysis, name='skin_analysis'),
    path('api/analyze-skin/', skin_analysis_view, name='analyze_skin'),

]
