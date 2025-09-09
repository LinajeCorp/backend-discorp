from django.core.management.base import BaseCommand
from apps.projects.models import Project


class Command(BaseCommand):
    help = 'Carga todos los proyectos iniciales en la base de datos'

    def handle(self, *args, **options):
        """Carga todos los proyectos de la tabla"""
        
        projects_data = [
            {
                'nombre': 'App Polizas',
                'fase': 'ejecucion',
                'objetivo': 'Sistema de app móvil que permitirá la cotización y adquisición de seguros RCV y servicios funerarios con aseguradoras nacionales.',
                'status': 'en_curso',
                'prioridad': 'normal',
                'ultima_actualizacion': 'Iniciando el desarrollo.',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'Autopago',
                'fase': 'ejecucion',
                'objetivo': 'Desarrollar sistema para comercios y/o eventos que permita la consulta de un servicio o estado de cuenta a la vez el pago de la misma o de productos.',
                'status': 'en_curso',
                'prioridad': 'alta',
                'ultima_actualizacion': 'En fase de integración entre todos los sistema que lo constituye (backend portal, app POS).',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'Vuelo digital',
                'fase': 'completado',
                'objetivo': 'Desarrollar e implementar app que realice vuelos digitales a través de un pago móvil o crédito inmediato desde el POS. Con los bancos: Banco Activo, BDV, Exterior, BFC, Banco Plaza, Tesoro, Bancrece, Banplus',
                'status': 'en_seguimiento',
                'prioridad': 'normal',
                'ultima_actualizacion': 'Con todos los bancos en producción.',
                'listo_para_ofrecer': 'si'
            },
            {
                'nombre': 'DisAccess',
                'fase': 'ejecucion',
                'objetivo': 'Desarrollar app para el control de acceso a áreas restringidas usando los dispositivos POS N62.',
                'status': 'en_curso',
                'prioridad': 'normal',
                'ultima_actualizacion': 'En desarrollo.',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'DisApp',
                'fase': 'ejecucion',
                'objetivo': 'Implementar app para clientes Disglobal que permita la autogestión desde el POS, consulta de estado de cuenta, envío de saldos y contacto.',
                'status': 'pausado',
                'prioridad': 'normal',
                'ultima_actualizacion': 'El proyecto se encuentra detenido debido a no tener prioridad de ejecución.',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'DisChange',
                'fase': 'completado',
                'objetivo': 'Herramienta que permite realizar la conversión de montos en divisas a Bolívares y ejecutar el pago del mismo a través del POS.',
                'status': 'en_seguimiento',
                'prioridad': 'normal',
                'ultima_actualizacion': 'En producción primera versión.',
                'listo_para_ofrecer': 'si'
            },
            {
                'nombre': 'Disconnect BPlaza',
                'fase': 'completado',
                'objetivo': 'Desarrollar sistema de autogestión para el circuito cerrado de pagos en eventos fijos.',
                'status': 'en_seguimiento',
                'prioridad': 'alta',
                'ultima_actualizacion': 'Sistema en producción piloto con el banco. Se están realizando mejoras.',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'Disconnect Eventos',
                'fase': 'completado',
                'objetivo': 'Desarrollar sistema para el circuito cerrado de pagos en eventos temporales.',
                'status': 'en_seguimiento',
                'prioridad': 'alta',
                'ultima_actualizacion': 'Sistema en producción, ya se ha usado en eventos. Se están realizando mejoras.',
                'listo_para_ofrecer': 'si'
            },
            {
                'nombre': 'DisPay',
                'fase': 'ejecucion',
                'objetivo': 'Desarrollar app para ejecutar recargas de diferentes servicios, como operadoras telefónicas, desde el POS.',
                'status': 'pausado',
                'prioridad': 'normal',
                'ultima_actualizacion': 'El proyecto se encuentra detenido debido a no tener prioridad de ejecución.',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'Midaz',
                'fase': 'ejecucion',
                'objetivo': 'Desarrollar app para el manejo de facturación física y registro de inventario en comercios de distintas categorías.',
                'status': 'en_curso',
                'prioridad': 'alta',
                'ultima_actualizacion': 'En desarrollo.',
                'listo_para_ofrecer': 'no'
            },
            {
                'nombre': 'Corpoelec',
                'fase': 'completado',
                'objetivo': 'App que permite la consulta del estado de cuenta de los contratos y el pago del mismo a través de la integración con la app financiera.',
                'status': 'en_seguimiento',
                'prioridad': 'alta',
                'ultima_actualizacion': 'En producción. Con nueva versión generada en fase piloto.',
                'listo_para_ofrecer': 'si'
            },
            {
                'nombre': 'DisLink',
                'fase': 'completado',
                'objetivo': 'Ecosistema cerrado que brinda soluciones de conciliación de pagos',
                'status': 'en_seguimiento',
                'prioridad': 'alta',
                'ultima_actualizacion': 'En producción, actualmente implementado con Farmatodo y aerolíneas (las 4 user). Se está trabajando la última, en fase piloto.',
                'listo_para_ofrecer': 'si'
            }
        ]

        # Eliminar proyectos existentes si ya existen
        Project.objects.all().delete()
        
        # Crear los proyectos
        projects_created = 0
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                nombre=project_data['nombre'],
                defaults=project_data
            )
            if created:
                projects_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Proyecto creado: {project.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Proyecto ya existe: {project.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Proceso completado: {projects_created} proyectos creados de {len(projects_data)} total'
            )
        )
        
        # Mostrar estadísticas
        total_projects = Project.objects.count()
        en_curso = Project.objects.filter(status='en_curso').count()
        en_seguimiento = Project.objects.filter(status='en_seguimiento').count()
        pausados = Project.objects.filter(status='pausado').count()
        listos = Project.objects.filter(listo_para_ofrecer='si').count()
        
        self.stdout.write(
            self.style.SUCCESS(f'\n📊 Estadísticas:')
        )
        self.stdout.write(f'   Total de proyectos: {total_projects}')
        self.stdout.write(f'   En curso: {en_curso}')
        self.stdout.write(f'   En seguimiento: {en_seguimiento}')
        self.stdout.write(f'   Pausados: {pausados}')
        self.stdout.write(f'   Listos para ofrecer: {listos}')
