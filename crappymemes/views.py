from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
# Create your views here.


class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, '../templates/index.html', {})
