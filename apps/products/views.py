import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductsAPIView(APIView):
    """
    API View para consultar productos desde Strapi

    Este endpoint consulta la API externa de Strapi, procesa los datos
    y retorna solo los campos necesarios: id, title, description,
    img (imagen principal) e img_variants (variantes de imágenes).
    """

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener lista de productos desde API externa de Strapi",
        manual_parameters=[
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
                                "title": "**Un POS integral que** _combina potencia y "
                                         "versatilidad_ **en cada transacción**",
                                "description": "El N82 está pensado para negocios "
                                               "que buscan agilidad y conectividad "
                                               "avanzada...",
                                "img": "https://res.cloudinary.com/dsgcdhkwc/image/"
                                       "upload/v1717649909/gris_5b48bac258.png",
                                "img_variants": [
                                    {
                                        "id": 215,
                                        "img": "https://res.cloudinary.com/dsgcdhkwc/"
                                               "image/upload/v1717643491/"
                                               "G5_single_Image_b97a6efe04.png",
                                        "title": None
                                    },
                                    {
                                        "id": 216,
                                        "img": "https://res.cloudinary.com/dsgcdhkwc/"
                                               "image/upload/v1717649909/"
                                               "gris_5b48bac258.png",
                                        "title": None
                                    },
                                    {
                                        "id": 217,
                                        "img": "https://res.cloudinary.com/dsgcdhkwc/"
                                               "image/upload/v1717649638/"
                                               "azul_6f20cf6c32.png",
                                        "title": None
                                    }
                                ]
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

        Procesa los datos de Strapi y retorna solo los campos necesarios:
        - id: ID del producto
        - title: Título del producto
        - description: Descripción del producto
        - img: Imagen principal (del primer color disponible)
        - img_variants: Array con todas las variantes de imágenes
        """
        try:
            # URL de la API externa de Strapi con populate específico
            strapi_url = (
                "https://strapi-disglobal-production.up.railway.app/api/products"
            )

            # Construir parámetros de query
            params = {}

            # Parámetros de populate específicos (fijos)
            params["populate[0]"] = "product_color.images"
            params["populate[1]"] = "product_features"
            params["populate[2]"] = "product_tecnology"

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
                # Obtener los datos de Strapi
                strapi_data = response.json()

                # Procesar y filtrar los datos para devolver solo lo necesario
                filtered_products = []

                for product in strapi_data.get('data', []):
                    # Obtener la imagen principal del primer color disponible
                    main_image = None
                    if (product.get('product_color') and
                            len(product['product_color']) > 0):
                        main_image = product['product_color'][0].get('img')

                    # Obtener todas las imágenes variantes del primer color
                    image_variants = []
                    if (product.get('product_color') and
                            len(product['product_color']) > 0):
                        images = product['product_color'][0].get('images', [])
                        image_variants = [
                            {
                                "id": img.get('id'),
                                "img": img.get('img'),
                                "title": img.get('title')
                            }
                            for img in images
                        ]

                    # Crear el producto filtrado
                    filtered_product = {
                        "id": product.get('id'),
                        "title": product.get('title'),
                        "description": product.get('description'),
                        "img": main_image,
                        "img_variants": image_variants
                    }

                    filtered_products.append(filtered_product)

                # Crear la respuesta con la misma estructura de paginación
                filtered_response = {
                    "data": filtered_products,
                    "meta": strapi_data.get('meta', {})
                }

                return Response(filtered_response, status=status.HTTP_200_OK)
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
