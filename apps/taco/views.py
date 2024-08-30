from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CMVColtaco3Serializer
from .utils import get_retention_db_connection

class CMVColtaco3ListView(APIView):
    def get(self, request):
        description = request.query_params.get('description', None)
        query = "SELECT * FROM CMVColtaco3"

        if description:
            query += " WHERE food_description LIKE %s"
            params = [f'%{description}%']
        else:
            params = []

        # Executando a query no banco de retenção
        with get_retention_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Captura a descrição das colunas
                columns = [col[0] for col in cursor.description]

        # Convertendo os resultados para uma lista de dicionários
        foods = [dict(zip(columns, row)) for row in rows]

        # Serializando os dados
        serializer = CMVColtaco3Serializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CMVColtaco3DetailView(APIView):
    def get(self, request, param):
        try:
            if param.isdigit():  # Se o parâmetro for um ID
                query = "SELECT * FROM CMVColtaco3 WHERE id = %s"
                params = [param]
            else:  # Se o parâmetro for uma descrição
                query = "SELECT * FROM CMVColtaco3 WHERE food_description LIKE %s LIMIT 1"
                params = [f'%{param}%']

            # Executando a query no banco de retenção
            with get_retention_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    row = cursor.fetchone()

                    if row:
                        # Captura a descrição das colunas
                        columns = [col[0] for col in cursor.description]
                        alimento = dict(zip(columns, row))

                        # Serializando o dado
                        serializer = CMVColtaco3Serializer(alimento)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "Alimento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
