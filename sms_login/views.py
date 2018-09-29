from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views import View
import json


class Create(View):
    def get(self, request):
        # get logic
        return JsonResponse({'GET': 'true'})

    def post(self, request):
        # post logic
        json_data = json.loads(request.body) # convert post incoming data to json
        if('phone_number' in json_data):
            return JsonResponse({'POST': 'true','status':200})
        return JsonResponse({'status': 200, 'messge': 'need phone number'})
