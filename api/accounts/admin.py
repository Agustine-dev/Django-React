from django.contrib import admin
from . models import *
# Register your models here.

class BaseAdmin(admin.ModelAdmin):
    list_display = ("email",)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name')
    
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(User, BaseAdmin)