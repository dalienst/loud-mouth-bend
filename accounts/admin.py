from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

admin.site.register(User)
admin.site.register(Profile)
