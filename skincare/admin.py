from django.contrib import admin
from .models import UserProfile, SkinCareRoutine

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skin_type', 'age', 'gender')
    list_filter = ('skin_type', 'gender')
    search_fields = ('user__username', 'user__email')
    
    def get_concerns_display(self, obj):
        return obj.concerns if obj.concerns else "None"
    get_concerns_display.short_description = 'Skin Concerns'

@admin.register(SkinCareRoutine)
class SkinCareRoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'completed')
    list_filter = ('completed', 'date')
    search_fields = ('user__username',)
    date_hierarchy = 'date'

    def get_routine_steps_display(self, obj):
        return "Morning: {}\nNoon: {}\nNight: {}".format(
            obj.morning_routine,
            obj.noon_routine,
            obj.night_routine
        )
    get_routine_steps_display.short_description = 'Routine Steps'