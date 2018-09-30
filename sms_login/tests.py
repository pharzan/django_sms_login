#!/usr/bin/env python3

from sms_login.models import Users
from django.urls import reverse, resolve
import json
from django.test import TestCase, Client

client = Client()


class UserTestCase(TestCase):
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
