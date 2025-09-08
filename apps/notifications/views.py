from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.contrib.auth import get_user_model

User = get_user_model()


class SendTestNotificationView(APIView):
    """Endpoint para enviar notificaciones de prueba"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Enviar notificación de prueba al usuario autenticado",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, default='🧪 Test'),
                'body': openapi.Schema(type=openapi.TYPE_STRING, default='Prueba desde Django'),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, default={'type': 'test'})
            },
            required=['title', 'body']
        ),
        responses={200: "Notificación enviada", 404: "Sin dispositivos"},
        tags=['Notificaciones']
    )
    def post(self, request):
        """Enviar notificación de prueba"""
        try:
            title = request.data.get('title', '🧪 Notificación de Prueba')
            body = request.data.get('body', 'Esta es una prueba desde Django')
            data = request.data.get('data', {'type': 'test', 'action': 'open_app'})

            user_devices = FCMDevice.objects.filter(user=request.user, active=True)

            if not user_devices.exists():
                return Response({
                    'success': False,
                    'error': 'No tienes dispositivos registrados'
                }, status=status.HTTP_404_NOT_FOUND)

            message = Message(
                notification=Notification(title=title, body=body),
                data=data
            )

            user_devices.send_message(message)

            return Response({
                'success': True,
                'message': f'Notificación enviada a {user_devices.count()} dispositivos',
                'devices_count': user_devices.count()
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendNotificationToUserView(APIView):
    """Endpoint para admins enviar notificaciones a usuarios específicos"""
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Enviar notificación a usuario específico (solo admins)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'body': openapi.Schema(type=openapi.TYPE_STRING),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT)
            },
            required=['title', 'body']
        ),
        tags=['Notificaciones Admin']
    )
    def post(self, request):
        """Enviar notificación a usuario específico"""
        try:
            user_id = request.data.get('user_id')
            username = request.data.get('username')
            
            if user_id:
                target_user = User.objects.get(id=user_id)
            elif username:
                target_user = User.objects.get(username=username)
            else:
                return Response({'error': 'user_id o username requerido'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            title = request.data.get('title')
            body = request.data.get('body')
            data = request.data.get('data', {})

            user_devices = FCMDevice.objects.filter(user=target_user, active=True)
            
            if not user_devices.exists():
                return Response({
                    'error': f'Usuario {target_user.username} sin dispositivos'
                }, status=status.HTTP_404_NOT_FOUND)

            message = Message(
                notification=Notification(title=title, body=body),
                data=data
            )

            user_devices.send_message(message)

            return Response({
                'success': True,
                'message': f'Enviado a {target_user.username}',
                'devices_count': user_devices.count()
            })

        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendBroadcastView(APIView):
    """Enviar a todos los usuarios"""
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Enviar notificación a todos los usuarios",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'body': openapi.Schema(type=openapi.TYPE_STRING),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT)
            },
            required=['title', 'body']
        ),
        tags=['Notificaciones Admin']
    )
    def post(self, request):
        """Enviar broadcast"""
        try:
            title = request.data.get('title')
            body = request.data.get('body')
            data = request.data.get('data', {'type': 'broadcast'})

            all_devices = FCMDevice.objects.filter(active=True)

            message = Message(
                notification=Notification(title=title, body=body),
                data=data
            )

            all_devices.send_message(message)

            return Response({
                'success': True,
                'message': 'Broadcast enviado',
                'devices_count': all_devices.count()
            })

        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)