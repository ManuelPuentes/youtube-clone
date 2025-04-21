from django.views import View
from django.shortcuts import render

class ErrorView(View):
    def get(self, request):
        return render(request, 'error.html')
