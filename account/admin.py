from django.contrib import admin
from .models import User, Address, Profession, Certifications

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Profession)

admin.site.register(Certifications)
