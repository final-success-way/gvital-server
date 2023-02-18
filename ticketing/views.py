from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ticketing.models import *
from ticketing.serializers import TicketSerializer


# Create your views here.
class ContactRequest(generics.CreateAPIView):
    name = 'contact-request'

    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        email = request.data.get('email', '')
        name = request.data.get('name', '')
        message = request.data.get('message', '')
        extra = request.data.get('extra', '')
        status_code = status.HTTP_400_BAD_REQUEST
        # import pdb;pdb.set_trace()
        try:
            contactRequest = ContactMessage.objects.create(message=message, name=name, email=email, extra=extra)

            status_code = status.HTTP_200_OK
            response.update({
                "message": "Hi %s, We've received your contact request. Someone will be in touch with you shortly."%name,
                "success": True
            })
            return Response(response, status=status_code)

        except Exception as e:
            response.update({
                "message": "Something wrong happened",
                "success": False,
                "server_response": str(e)
            })
            return Response(response, status=status_code)


class RaiseIssue(generics.CreateAPIView):
    name = 'raise-issue'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }

        subject = request.data.get('subject', '')
        name = request.data.get('name', '')
        message = request.data.get('message', '')
        user = request.user
        status_code = status.HTTP_400_BAD_REQUEST
        # import pdb;pdb.set_trace()
        try:
            temp_user = request.user

            status_code = status.HTTP_400_BAD_REQUEST

            message = Message.objects.create(message=message, user=request.user)
            ticket = Ticket.objects.create(subject=subject, user=user)
            ticket.messages.add(message)
            ticket.save()

            status_code = status.HTTP_200_OK
            response.update({
                "message": "Ticket raised successfully",
                "success": True
            })
            return Response(response, status=status_code)

        except Exception as e:
            response.update({
                "message": "Something wrong happened",
                "success": False,
                "server_response": str(e)
            })
            return Response(response, status=status_code)


class UpdateTicket(generics.CreateAPIView):
    name = 'update-ticket'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }

        message = request.data.get('message', '')
        attachment = request.FILES.get('attachment', False)
        ticketId = request.data.get('ticket_id', '')
        user = request.user
        status_code = status.HTTP_400_BAD_REQUEST
        # import pdb;pdb.set_trace()
        try:
            temp_user = request.user
            status_code = status.HTTP_400_BAD_REQUEST

            message = Message.objects.create(message=message, user=request.user)
            ticket = Ticket.objects.filter(uid=ticketId)
            if len(ticket) > 0:
                ticket = ticket[0]
                ticket.messages.add(message)
                ticket.save()

                status_code = status.HTTP_200_OK
                response.update({
                    "message": "Message received successfully",
                    "success": True
                })
            return Response(response, status=status_code)

        except Exception as e:
            response.update({
                "message": "Something wrong happened",
                "success": False,
                "server_response": str(e)
            })
            return Response(response, status=status_code)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class GetTickets(generics.ListAPIView):
    name = 'get-tickets-list'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = StandardResultsSetPagination

    # filterset_fields = ['shop__', 'status']

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(user=user).order_by('-updated_at')
        return queryset
