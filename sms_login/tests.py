#!/usr/bin/env python3


from sms_login.models import Users, Tokens
from django.urls import reverse, resolve
import json
from django.test import TestCase, Client
import requests
import unittest


client = Client()


class UserTestCase(unittest.TestCase):

    def setUp(self):

        self.valid_payload = {
            'phone_number': '0914123456',
        }

        self.existing_payload = {
            'phone_number': '09143134604',
        }

        self.invalid_payload = {
            'name': '2311413223',
        }
        self.dummy_phone = '09123456789'
        self.dummy_code = '1234'
        Users.objects.create(phone_number=self.dummy_phone,four_digit_code=self.dummy_code)
        Tokens.objects.create(user_id=1, token='1abcdef',)


    def test_create_valid_code(self):
        response = client.post(
            '/api/login/create',
            data=json.dumps(self.valid_payload),
            content_type='application/json')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

    def test_existing_phone_number_code(self):
        response = client.post(
            '/api/login/create',
            data=json.dumps(self.existing_payload),
            content_type='application/json')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

    def test_invalid_phone_number(self):
        response = client.post(
            '/api/login/create', content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_existing_verification_code_valid(self):
        response = client.post(
            '/api/login/verify',
            data={'phone_number': '09123456789',
                    'verification_code': '1234'
            },
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_existing_verification_code_invalid(self):
        response = client.post(
            '/api/login/verify',
            data={'phone_number': '09123456789',
                    'verification_code': '4321'
            },
            content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_valid_verification_token_creation(self):
        response = client.post(
            '/api/login/create',
            data=json.dumps(self.existing_payload),
            content_type='application/json')

        send_phone_number_result = json.loads(response.content)

        response = client.post(
            '/api/login/verify',
            data={
                "phone_number": "09143134604",
                "verification_code": send_phone_number_result['code']
            },
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content)

    def test_invalid_verification_token_creation(self):
        response = client.post(
            '/api/login/create',
            data=json.dumps(self.existing_payload),
            content_type='application/json')

        send_phone_number_result = json.loads(response.content)

        response = client.post(
            '/api/login/verify',
            data={
                "phone_number": "09143134604",
                "verification_code": '1234'            },
            content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_authorize(self):
        response = client.get(
            "/api/login/auth",
            HTTP_TOKEN= '1abcdef',
            content_type='application/json')
        response_content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['phone_number'], '09123456789')

    def test_unauthorize(self):
        response = client.get(
            "/api/login/auth",
            HTTP_TOKEN= '35mnb4jh6tuy76ghb',
            content_type='application/json')
        self.assertEqual(response.status_code, 401)




if __name__ == '__main__':
    unittest.main()
