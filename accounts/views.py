from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, get_connection
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import *
from accounts.serializers import ProfileSerializer
from orders.models import Order
from payments.models import Payment
from services.models import Service
from ticketing.models import ContactMessage
from utils.views import *


def admin_login(request):
    if request.method == 'POST':
        if 'admin.' in request.get_host() or 'api.' in request.get_host() or 'localhost' in request.get_host():
            context = {}
            email = request.POST.get('email')
            password = request.POST.get('password')
            signout = request.POST.get('logout')
            if signout:
                logout(request)
                return redirect('/super')
            user = User.objects.filter(Q(email=email) | Q(username=email))
            if len(user) > 0:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/super', )
                else:
                    context["error"] = True
                    context["message"] = "Invalid Credentials"
            else:
                context["error"] = True
                context["message"] = "Invalid Credentials"

            return render(request, 'admin-login.html', context)
    else:
        if 'api.' in request.get_host() or 'localhost' in request.get_host():
            context = {}
            if request.user.is_superuser:
                query = request.GET.get('q', 'orders')
                order_status = request.GET.get('order_status', 'all')
                if query == 'orders':
                    orders = Order.objects.all().exclude(payment__payment_status=Payment.PENDING).order_by('-updated_at')
                    if order_status == 'completed':
                        orders = Order.objects.filter(status=Order.COMPLETED).order_by('-updated_at')
                    if order_status == 'processing':
                        orders = Order.objects.filter(
                            Q(status=Order.PROCESSING) | Q(status=Order.IN_PROGRESS) | Q(status=Order.PARTIAL)).order_by('-updated_at')
                    if order_status == 'cancelled':
                        orders = Order.objects.filter(status=Order.CANCELLED).order_by('-updated_at')
                    if order_status == 'failed':
                        orders = Order.objects.filter(status=Order.FAILED).order_by('-updated_at')
                    context = {
                        'values': orders
                    }
                elif query == 'payments':
                    payment_status = request.GET.get('payment_status', 'all')
                    payments = Payment.objects.all().exclude(payment_status=Payment.PENDING).order_by('-updated_at')
                    if payment_status == 'completed':
                        payments = Payment.objects.filter(payment_status=Payment.COMPLETED).order_by('-updated_at')
                    if payment_status == 'processing':
                        payments = Payment.objects.filter(payment_status=Payment.PROCESSING).order_by('-updated_at')
                    if payment_status == 'cancelled':
                        payments = Payment.objects.filter(payment_status=Payment.CANCELLED).order_by('-updated_at')
                    if payment_status == 'failed':
                        payments = Payment.objects.filter(payment_status=Payment.FAILED).order_by('-updated_at')
                    if payment_status == 'pending':
                        payments = Payment.objects.filter(payment_status=Payment.PENDING).order_by('-updated_at')
                    context = {
                        'values': payments
                    }
                elif query == 'tickets':
                    contact_messages = ContactMessage.objects.all().order_by('-updated_at')
                    context = {
                        'values': contact_messages
                    }
                elif query == 'users':
                    profiles = Profile.objects.all().order_by('-updated_at')
                    context = {
                        'values': profiles
                    }
                elif query == 'services':
                    services = Service.objects.all().order_by('platform')
                    context = {
                        'values': services
                    }
            return render(request, 'admin-login.html', context)
    redirect_buy_real = '<meta http-equiv="refresh" content="5;URL=%s" />' % 'https://buyrealfollows.com'
    return HttpResponseNotFound(redirect_buy_real)


class LoginUser(generics.CreateAPIView):
    name = 'login-user'

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
        try:

            # import pdb;pdb.set_trace()

            email = request.data.get('email', '')
            password = request.data.get('password', '')
            users = User.objects.filter(email=email)
            if len(users) > 0:
                user = authenticate(request, username=users[0].username, password=password)

                if user is None:
                    response.update({
                        'message': "Email or password is incorrect",
                        'success': False,
                    })
                    return Response(response, status=status_code)

                status_code = status.HTTP_200_OK
                token, created = Token.objects.get_or_create(user=user)
                response.update({
                    'message': 'Logged in successfully',
                    'token': token.key,
                    'success': True,
                })
            else:
                response.update({
                    'message': 'Email or password is incorrect',
                    'success': False,
                })

        except Exception as e:
            response.update({
                'message': 'Logged in failed',
                'success': False,
                'error': str(e)
            })
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


class ProfileInfo(generics.CreateAPIView):
    name = 'profile-info'

    @action(methods=['get'], detail=True)
    def list(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST

        try:

            insta_username = request.query_params.get('insta_username')
            email = request.query_params.get('email', '')
            product = request.query_params.get('product', '')

            user = User.objects.filter(email=email)
            order = []

            status_code = status.HTTP_200_OK
            response.update({
                "profile": {
                    "has_account_already": len(user) > 0,
                    "previous_order": len(order) > 0
                },
                'success': True,
            })

            return Response(response, status=status_code)

        except Exception as e:
            response.update({
                'message': 'Profile info fetch failed',
                'success': False,
                'error': str(e)
            })

        return Response(response, status=status_code)


class RegisterUser(generics.CreateAPIView):
    name = 'register-user'

    def sendWelcomeEmail(self, subject, txtmes, fromUser, to, token):
        html_content = render_to_string('welcome.html', {'token': token})

        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER_SUPPORT,
                password=settings.EMAIL_HOST_PASSWORD_SUPPORT,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            mail = send_mail(subject,
                             message=txtmes,
                             recipient_list=[to],
                             from_email='Support Buyrealfollows <%s>' % settings.EMAIL_HOST,
                             connection=connection,
                             fail_silently=False,
                             html_message=html_content)
            print(mail)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }

        email = request.data.get('email', '')
        full_name = request.data.get('full_name', '')
        password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')
        source = request.data.get('source', '')
        status_code = status.HTTP_400_BAD_REQUEST
        with transaction.atomic():
            try:
                temp_profile = Profile.objects.filter(email=email, active=True)

                if len(temp_profile) > 0:
                    temp_user = User.objects.filter(email=temp_profile[0].email)
                    temp_user = temp_user[0]

                    status_code = status.HTTP_400_BAD_REQUEST

                    response.update({
                        "message": "Account already exists with this email",
                        "success": False
                    })
                    return Response(response, status=status_code)
                user = User.objects.create_user(
                    username=email, email=email, password=password)

                profile = Profile.objects.create(user=user, email=email, name=full_name)

                profile.flags.is_user = True
                profile.save()
                temp_token = TempToken.objects.create(user=user)
                self.sendWelcomeEmail("Welcome to Buyrealfollows", "", "support@buyrealfollows.com", email,
                                      temp_token.token)

                status_code = status.HTTP_200_OK
                response.update({
                    "message": "Your profile has been successfully created, please check your email",
                    "success": True
                })
                return Response(response, status=status_code)
            except IntegrityError as e:
                response.update({
                    "message": "Email already exists",
                    "success": False,
                    "server_response": str(e)
                })

        return Response(response, status=status_code)


class GetUserInfo(generics.ListAPIView):
    name = 'get-user-info'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # filterset_fields = ['shop__', 'status']

    def get_queryset(self):
        user = self.request.user
        queryset = Profile.objects.filter(user=user)
        return queryset


class ChangePassword(generics.CreateAPIView):
    name = 'change-password'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        currentPassword = request.data.get('current_password', '')
        newPassword = request.data.get('new_password', '')
        confirmPassword = request.data.get('confirm_password', '')
        status_code = status.HTTP_400_BAD_REQUEST
        try:

            user = request.user
            email = user.email
            authuser = authenticate(request, username=user.username, password=currentPassword)

            if authuser is not None:
                if newPassword == confirmPassword:
                    authuser.set_password(newPassword)
                    authuser.save()
                    status_code = status.HTTP_200_OK

                    response.update({
                        "message": "Password changed successfully",
                        "success": True
                    })
                    return Response(response, status=status_code)

                status_code = status.HTTP_400_BAD_REQUEST

                response.update({
                    "message": "Password change failed",
                    "success": False
                })
                return Response(response, status=status_code)

            else:
                raise Exception("Auth user is none")


        except Exception as e:
            response.update({
                "message": "Password change failed",
                "success": False,
                "server_response": str(e)
            })

        return Response(response, status=status_code)


class ChangeUserPassword(generics.CreateAPIView):
    name = 'change-user-password'

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        token = request.data.get('token', '')
        newPassword = request.data.get('new_password', '')
        confirmPassword = request.data.get('confirm_password', '')
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            temp_token = TempToken.objects.filter(token=token, active=False)
            if newPassword == confirmPassword:
                if len(temp_token) > 0:
                    temp_token = temp_token[0]
                    user = temp_token.user
                    user.set_password(newPassword)
                    user.save()
                    temp_token.active = True
                    temp_token.save()
                    status_code = status.HTTP_200_OK
                    response.update({
                        "message": "Password changed successfully",
                        "success": True
                    })
                    return Response(response, status=status_code)
                raise Exception("Token not found")

            status_code = status.HTTP_400_BAD_REQUEST
            response.update({
                "message": "Password change failed",
                "success": False
            })
            return Response(response, status=status_code)

        except Exception as e:
            response.update({
                "message": "Password change failed",
                "success": False,
                "server_response": str(e)
            })

        return Response(response, status=status_code)


class ChangeEmail(generics.CreateAPIView):
    name = 'change-email'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }

        oldEmail = request.user.email
        newEmail = request.data.get('email', '')
        status_code = status.HTTP_400_BAD_REQUEST
        try:

            user = User.objects.filter(email=oldEmail)

            if len(user) > 0:
                temp_user = User.objects.filter(email=newEmail)

                if len(temp_user) > 0:
                    status_code = status.HTTP_400_BAD_REQUEST

                    response.update({
                        "message": "Email already exists",
                        "success": False
                    })
                    return Response(response, status=status_code)

                user = user[0]
                user.email = newEmail
                user.save()

                status_code = status.HTTP_200_OK
                response.update({
                    "message": "Email changed successfully",
                    "success": True
                })
                return Response(response, status=status_code)


        except IntegrityError as e:
            response.update({
                "message": "Email change failed",
                "success": False,
                "server_response": str(e)
            })

        return Response(response, status=status_code)


class ResetPassword(generics.CreateAPIView):
    name = 'reset-password'

    def sendResetEmail(self, subject, txtmes, fromUser, to, token):
        html_content = render_to_string('reset-password.html', {'token': token})
        # txtmes = render_to_string('text-message.html')
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER_SUPPORT,
                password=settings.EMAIL_HOST_PASSWORD_SUPPORT,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            mail = send_mail(subject,
                             message=txtmes,
                             recipient_list=[to],
                             from_email='Support Buyrealfollows <%s>' % settings.EMAIL_HOST,
                             connection=connection,
                             fail_silently=False,
                             html_message=html_content)
            print(mail)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        email = request.data.get('email', '')
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            user = User.objects.filter(email=email)

            if len(user) > 0:
                temp_token = TempToken.objects.create(user=user[0])
                self.sendResetEmail("Reset password request", "", "support@buyrealfollows.com", email, temp_token.token)

            status_code = status.HTTP_200_OK
            response.update({
                "message": "If the email exists you will receive a Verification Email",
                "success": True
            })
            return Response(response, status=status_code)


        except Exception as e:
            response.update({
                "message": "Email sending failed",
                "success": False,
                "server_response": str(e)
            })

        return Response(response, status=status_code)


class VerifyToken(generics.CreateAPIView):
    name = 'verify-token'

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        token = request.data.get('token', '')
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            token = TempToken.objects.filter(token=token, active=False)
            if len(token) > 0:
                token = token[0]

                status_code = status.HTTP_200_OK
                response.update({
                    "message": "Token verified, you can continue changing password",
                    "success": True,
                    "email": token.user.email
                })
                return Response(response, status=status_code)
            else:
                raise Exception("Invalid token or expired ")


        except Exception as e:
            response.update({
                "message": "Token verification Failed",
                "success": False,
                "server_response": str(e)
            })

        return Response(response, status=status_code)
