import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings


class ProductsAPIView(APIView):
    """
    API View para consultar productos desde Strapi

    Este endpoint consulta la API externa de Strapi y retorna
    exactamente la misma estructura de datos sin modificaciones.
    """

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener lista de productos desde API externa de Strapi",
        manual_parameters=[
            openapi.Parameter(
                "populate",
                openapi.IN_QUERY,
                description="Parámetro para incluir relaciones (valor por defecto: *)",
                type=openapi.TYPE_STRING,
                default="*",
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Número de página",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "pageSize",
                openapi.IN_QUERY,
                description="Cantidad de elementos por página",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Lista de productos obtenida exitosamente",
                examples={
                    "application/json": {
                        "data": [
                            {
                                "id": 141,
                                "documentId": "mpo7g5fw5ld0iyirxpi8oxmp",
                                "title": "**Un POS integral que** _combina potencia y versatilidad_ **en cada transacción**",
                                "slug": "n82",
                                "description": "El N82 está pensado para negocios que buscan agilidad y conectividad avanzada...",
                                "price": None,
                                "createdAt": "2025-08-14T23:33:27.683Z",
                                "updatedAt": "2025-08-18T15:54:18.653Z",
                                "publishedAt": "2025-08-18T15:54:21.294Z",
                                "technical_specification": "# **Especificaciones Técnicas**...",
                                "title2": "**POS** _inteligente_ **N82**",
                                "description2": "Diseñado para quienes necesitan rendimiento constante...",
                                "feature_title": "**Opera sin barreras,** _con tecnología inteligente_...",
                                "feature_description": "El N82 se adapta al ritmo de tu negocio...",
                                "slug_title": "N82",
                                "feature_title1": None,
                                "experiment_title": "**Diseño que optimiza tus cobros,**...",
                                "experiment_description": "El N82 es una herramienta integral...",
                                "payment_methods": None,
                                "payment_description": None,
                                "product_tecnology": {
                                    "id": 2,
                                    "documentId": "eq22r8cwt1w6ny1yemolxqj6",
                                    "createdAt": "2025-07-23T15:40:11.067Z",
                                    "updatedAt": "2025-07-23T15:40:11.067Z",
                                    "publishedAt": "2025-07-23T15:40:12.149Z",
                                    "title": "Android",
                                },
                                "product_features": [
                                    {
                                        "id": 450,
                                        "title": "Pantalla Táctil",
                                        "description": 'Pantalla táctil capacitiva de 5" para una interacción fluida.',
                                        "icon": None,
                                    }
                                ],
                                "product_color": [],
                            }
                        ],
                        "meta": {
                            "pagination": {
                                "page": 1,
                                "pageSize": 25,
                                "pageCount": 1,
                                "total": 10,
                            }
                        },
                    }
                },
            ),
            500: openapi.Response(
                description="Error al consultar la API externa",
                examples={
                    "application/json": {
                        "error": "Error al consultar la API de productos",
                        "detail": "Connection timeout",
                    }
                },
            ),
        },
        tags=["Productos"],
    )
    def get(self, request):
        """
        Consultar productos desde la API externa de Strapi

        Retorna exactamente la misma estructura de datos que viene de Strapi
        sin ninguna modificación o procesamiento adicional.
        """
        try:
            # URL de la API externa de Strapi
            strapi_url = (
                "https://strapi-disglobal-production.up.railway.app/api/products"
            )

            # Construir parámetros de query
            params = {}

            # Parámetro populate (por defecto *)
            populate = request.query_params.get("populate", "*")
            params["populate"] = populate

            # Parámetros de paginación
            page = request.query_params.get("page")
            if page:
                params["pagination[page]"] = page

            page_size = request.query_params.get("pageSize")
            if page_size:
                params["pagination[pageSize]"] = page_size

            # Realizar petición a la API externa
            response = requests.get(
                strapi_url,
                params=params,
                timeout=30,  # Timeout de 30 segundos
            )

            # Verificar si la petición fue exitosa
            if response.status_code == 200:
                # Retornar exactamente la misma data que viene de Strapi
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "error": "Error al consultar la API de productos",
                        "status_code": response.status_code,
                        "detail": response.text,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except requests.exceptions.Timeout:
            return Response(
                {
                    "error": "Error al consultar la API de productos",
                    "detail": "Timeout - La API externa no respondió a tiempo",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except requests.exceptions.ConnectionError:
            return Response(
                {
                    "error": "Error al consultar la API de productos",
                    "detail": "No se pudo conectar con la API externa",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response(
                {"error": "Error al consultar la API de productos", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
