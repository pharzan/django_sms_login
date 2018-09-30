from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views import View
import json
from sms_login.models import Users,Tokens
import random, hashlib


def random_code():
    # the following function creates a random four digit code
    # this function is supposed to be taken care of by the sms provider.
    codes = [random.choice(range(10)) for r in range(4)]
    return "".join(str(c) for c in codes)


def generate_token(phone_number):
    return hashlib.sha256(phone_number.encode()).hexdigest()


class Create(View):
    def get(self, request):
        # get logic
        return JsonResponse({'GET': 'true'})

    def post(self, request):
        # post logic
        json_data = json.loads(
            request.body)  # convert post incoming data to json
        if 'phone_number' in json_data:  # make usre phone number is sent from client
            is_new_user = False
            requested_phone_number = json_data['phone_number']
            query_result = Users.objects.filter(
                phone_number=requested_phone_number).values()
            four_digit_code = random_code()
            if len(query_result) == 0:
                # phone number not in db : new user
                # new_user created pk = 1 and so on...
                is_new_user = True
                new_user = Users(
                    phone_number=requested_phone_number,
                    four_digit_code=four_digit_code)
                new_user.save()

            else:
                Users.objects.filter(phone_number=requested_phone_number
                                     ).update(four_digit_code=four_digit_code)

            return JsonResponse({
                'code': four_digit_code,
                'status': 200,
                'is_new_user': is_new_user
            })

        return JsonResponse({'status': 999, 'messge': 'need phone number'})


class Verify(View):
    def post(self, request):
        is_verified = False
        json_data = json.loads(
            request.body)  # convert post incoming data to json

        if 'verification_code' in json_data and 'phone_number' in json_data:
            # handle compare from db to see if code is right
            phone_number = json_data['phone_number']
            verification_code = json_data['verification_code']
            user_result = Users.objects.filter(phone_number=phone_number)

            if user_result.values()[0]['four_digit_code'] == verification_code:

                is_verified = True
                token = generate_token(phone_number.join(verification_code))
                token_in_db = Tokens.objects.filter(token=token)
                token_exists = False
                if len(token_in_db) > 0:
                    token_exists = True
                if not token_exists:
                    new_token = Tokens(token=token, user=user_result[0])
                    new_token.save()

                return JsonResponse({
                    'status': 200,
                    'verified': is_verified,
                    'token': token
                })
            return JsonResponse({'status': 200, 'verified': is_verified})

        return JsonResponse({
            'status': 999,
            'messge': 'need verification code and phone number'
        })


class Authorize(View):
    def get(self, request):
        # request.META holds the headers and to access a custom
        # header HTTP_ >> followed by custom header, Here I'm
        # checking for TOKEN in the header
        if 'HTTP_TOKEN' in request.META:
            token = request.META['HTTP_TOKEN']
            print('found token')
            return JsonResponse({'status': 200, 'token': token})

        return JsonResponse({'status': 999, 'message': 'not authorized'})
