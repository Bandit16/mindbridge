# Register your models here.
from django.contrib import admin
from .models import Letter, LetterImage

admin.site.register(Letter)
admin.site.register(LetterImage)
