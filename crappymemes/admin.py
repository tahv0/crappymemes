from django.contrib import admin
from django import forms
from crappymemes.models import Meme

# Register your models here.

class AdminMemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['title', 'pic', 'author']


class AdminMeme(admin.ModelAdmin):
    form = AdminMemeForm


admin.site.register(Meme, AdminMeme)
