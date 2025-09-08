from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from .models import NotificationHistory
import json

User = get_user_model()


@staff_member_required
def send_notification_view(request):
    """
    Vista personalizada para enviar notificaciones desde el admin
    """
    users = User.objects.all().order_by('username')
    recent_notifications = NotificationHistory.objects.all()[:10]
    
    # Estadísticas
    total_devices = FCMDevice.objects.filter(active=True).count()
    total_users_with_devices = FCMDevice.objects.filter(active=True).values('user').distinct().count()
    
    context = {
        'title': 'Enviar Notificaciones Push',
        'users': users,
        'recent_notifications': recent_notifications,
        'stats': {
            'total_devices': total_devices,
            'total_users_with_devices': total_users_with_devices,
        }
    }
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            notification_type = request.POST.get('notification_type')
            title = request.POST.get('title', '').strip()
            body = request.POST.get('body', '').strip()
            target_user_id = request.POST.get('target_user')
            data_payload = {}
            
            # Validaciones
            if not title or not body:
                messages.error(request, 'El título y el mensaje son obligatorios.')
                return render(request, 'admin/notifications/send_notification.html', context)
            
            # Agregar datos adicionales si se proporcionan
            if request.POST.get('data_action'):
                data_payload['action'] = request.POST.get('data_action')
            if request.POST.get('data_url'):
                data_payload['url'] = request.POST.get('data_url')
            if request.POST.get('data_custom'):
                try:
                    custom_data = json.loads(request.POST.get('data_custom', '{}'))
                    data_payload.update(custom_data)
                except json.JSONDecodeError:
                    messages.error(request, 'Los datos personalizados deben ser JSON válido.')
                    return render(request, 'admin/notifications/send_notification.html', context)
            
            # Crear registro en historial
            notification_record = NotificationHistory.objects.create(
                title=title,
                body=body,
                notification_type=notification_type,
                target_user_id=target_user_id if target_user_id else None,
                sent_by=request.user,
                data_payload=data_payload
            )
            
            # Determinar dispositivos objetivo
            if notification_type == 'broadcast':
                target_devices = FCMDevice.objects.filter(active=True)
                success_message = "Notificación broadcast enviada a todos los usuarios"
            elif notification_type == 'user' and target_user_id:
                target_user = User.objects.get(id=target_user_id)
                target_devices = FCMDevice.objects.filter(user=target_user, active=True)
                success_message = f"Notificación enviada a {target_user.username}"
            else:
                messages.error(request, 'Tipo de notificación inválido.')
                return render(request, 'admin/notifications/send_notification.html', context)
            
            if not target_devices.exists():
                notification_record.status = 'failed'
                notification_record.error_message = 'No hay dispositivos activos para el objetivo seleccionado'
                notification_record.save()
                messages.error(request, 'No hay dispositivos activos para enviar la notificación.')
                return render(request, 'admin/notifications/send_notification.html', context)
            
            # Crear mensaje Firebase
            message = Message(
                notification=Notification(
                    title=title,
                    body=body
                ),
                data=data_payload
            )
            
            # Enviar notificación
            target_devices.send_message(message)
            
            # Actualizar registro
            notification_record.status = 'sent'
            notification_record.devices_count = target_devices.count()
            notification_record.save()
            
            messages.success(request, f'{success_message} ({target_devices.count()} dispositivos)')
            return redirect('admin:send_notification')
            
        except User.DoesNotExist:
            messages.error(request, 'Usuario seleccionado no existe.')
        except Exception as e:
            # Actualizar registro con error
            if 'notification_record' in locals():
                notification_record.status = 'failed'
                notification_record.error_message = str(e)
                notification_record.save()
            
            messages.error(request, f'Error enviando notificación: {str(e)}')
    
    return render(request, 'admin/notifications/send_notification.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class GetUserDevicesView(View):
    """
    Vista AJAX para obtener información de dispositivos de un usuario
    """
    
    def post(self, request):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Sin permisos'}, status=403)
        
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            if not user_id:
                return JsonResponse({'error': 'user_id requerido'}, status=400)
            
            user = User.objects.get(id=user_id)
            devices = FCMDevice.objects.filter(user=user, active=True)
            
            devices_data = []
            for device in devices:
                devices_data.append({
                    'id': device.id,
                    'name': device.name or 'Sin nombre',
                    'type': device.get_type_display(),
                    'date_created': device.date_created.strftime('%Y-%m-%d %H:%M') if hasattr(device, 'date_created') else 'N/A'
                })
            
            return JsonResponse({
                'user': user.username,
                'devices': devices_data,
                'devices_count': devices.count()
            })
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def notification_history_view(request):
    """
    Vista para mostrar el historial detallado de notificaciones
    """
    notifications = NotificationHistory.objects.select_related('sent_by', 'target_user').all()
    
    context = {
        'title': 'Historial de Notificaciones',
        'notifications': notifications,
    }
    
    return render(request, 'admin/notifications/history.html', context)
