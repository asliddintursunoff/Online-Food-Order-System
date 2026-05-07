from django.contrib import admin

from apps.users.models import User,UserLocation

admin.site.register(User)
admin.site.register(UserLocation)