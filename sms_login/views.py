from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views import View



class Create(View):
    def get(self, request):
        # get logic
        return JsonResponse({'GET': 'true'})

    def post(self, request):
        # post logic
        return JsonResponse({'POST': 'true'})