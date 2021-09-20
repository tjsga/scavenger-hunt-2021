from django.contrib import admin

from .models import Challenge, Class, Category

admin.site.register(Category)
admin.site.register(Challenge)
admin.site.register(Class)
