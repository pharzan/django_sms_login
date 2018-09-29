from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views import View
import json
from sms_login.models import Users


# the following function creates a random four digit code
# this function is supposed to be taken care of by the sms provider.
def random_code():
    codes = [random.choice(range(10)) for r in range(4)]
    return "".join(str(c) for c in codes)


class Create(View):
    def get(self, request):
        # get logic
        return JsonResponse({'GET': 'true'})

    def post(self, request):
        # post logic
        json_data = json.loads(request.body) # convert post incoming data to json
        if('phone_number' in json_data):
            is_new_user = False
            requested_phone_number = json_data['phone_number']
            query_result = Users.objects.filter(phone_number=requested_phone_number)

            if len(query_result)==0:
                # phone number not in db : new user
                # new_user created pk = 1 and so on...
                is_new_user = True
                new_user = Users(phone_number=requested_phone_number)
                new_user.save()
            
            return JsonResponse({'code': random_code(),'status':200,'is_new_user':is_new_user})

        return JsonResponse({'status': 200, 'messge': 'need phone number'})
import random
