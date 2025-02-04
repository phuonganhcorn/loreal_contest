# from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     skin_type = models.CharField(max_length=50)
#     age = models.IntegerField()
#     gender = models.CharField(max_length=20)
#     concerns = models.JSONField(default=list)
#     climate = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.user.username}'s profile"

# class SkinCareRoutine(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()
#     morning_routine = models.TextField()
#     noon_routine = models.TextField()
#     night_routine = models.TextField()
#     diet_recommendations = models.TextField()
#     completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'date']


from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skin_type = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    concerns = ArrayField(models.CharField(max_length=100), blank=True, default=list)

class SkinAnalysisImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='skin_analysis/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# class SkinAnalysis(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = "None"
#     skin_type = models.CharField(max_length=50)
#     skin_concerns = models.TextField()  # JSON-serialized list
#     recommendations = models.TextField()
#     confidence_score = models.FloatField(default=0.0)
#     analyzed_at = models.DateTimeField(auto_now_add=True)

class SkinAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skin_type = models.CharField(max_length=50)
    skin_concerns = models.TextField()  # Store as JSON string
    recommendations = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Skin Analysis - {self.skin_type}"

class SkinCareRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    morning_routine = models.TextField()
    noon_routine = models.TextField()
    night_routine = models.TextField()
    diet_recommendations = models.TextField()
    completed = models.BooleanField(default=False)