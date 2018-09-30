from django.urls import path
from sms_login.views import Create, Verify, Authorize, UnAuthorize

urlpatterns = [
    path('create', Create.as_view()),
    path('verify', Verify.as_view()),
    path('auth', Authorize.as_view()),
    path('unauth', UnAuthorize.as_view()),
]
