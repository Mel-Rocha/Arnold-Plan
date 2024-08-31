import ast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .exceptions import InvalidCategoryError
from .serializers import CMVColtaco3Serializer
from .utils import get_retention_db_connection

class CMVColtaco3ListView(APIView):

    @staticmethod
    def get(request):
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

    @staticmethod
    def get(request, param, amount):
        try:
            try:
                amount = float(amount)
            except ValueError:
                return Response({"detail": "O parâmetro 'amount' deve ser um número válido."}, status=status.HTTP_400_BAD_REQUEST)

            if param.isdigit():  # Se o parâmetro for um ID
                query = "SELECT * FROM CMVColtaco3 WHERE id = %s"
                params = [param]
            else:  # Se o parâmetro for uma descrição
                query = "SELECT * FROM CMVColtaco3 WHERE food_description ILIKE %s LIMIT 1"
                params = [f'%{param}%']

            # Executando a query no banco de retenção
            with get_retention_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    row = cursor.fetchone()

                    if row:
                        # Captura a descrição das colunas
                        columns = [col[0] for col in cursor.description]
                        food = dict(zip(columns, row))

                        # Ajustando valores com base no 'amount'
                        for key in food:
                            if key not in ['id', 'food_description', 'category']:
                                try:
                                    value = float(food[key])
                                    food[key] = round((value * amount) / 100, 3)
                                except ValueError:
                                    # Se a conversão para float falhar, mantém o valor original
                                    continue

                        # Serializando o dado
                        serializer = CMVColtaco3Serializer(food)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "Alimento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CMVColtaco3CategoryView(APIView):

    @staticmethod
    def get(request, category):
        # Verifica se a categoria fornecida é válida usando a exceção personalizada
        valid_categories = InvalidCategoryError.VALID_CATEGORIES
        if category not in valid_categories:
            raise InvalidCategoryError(category)

        query = "SELECT * FROM CMVColtaco3 WHERE category = %s"
        params = [category]

        # Executando a query no banco de retenção
        try:
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

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CMVColtaco3BulkDetailView(APIView):

    @staticmethod
    def get(request, food_list):
        try:
            # Converte a string da URL para uma lista de tuplas
            try:
                food_list = ast.literal_eval(food_list)
            except (ValueError, SyntaxError):
                return Response({"detail": "O parâmetro 'food_list' deve ser uma lista de tuplas válida."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(food_list, list):
                return Response({"detail": "O parâmetro 'food_list' deve ser uma lista de tuplas."}, status=status.HTTP_400_BAD_REQUEST)

            results = []

            for item in food_list:
                if not isinstance(item, tuple) or len(item) != 2:
                    return Response({"detail": "Cada item na lista deve ser uma tupla contendo o ID do alimento e a quantidade."}, status=status.HTTP_400_BAD_REQUEST)

                food_id, amount = item

                try:
                    amount = float(amount)
                except ValueError:
                    return Response({"detail": f"O parâmetro 'amount' para o alimento com ID {food_id} deve ser um número válido."}, status=status.HTTP_400_BAD_REQUEST)

                query = "SELECT * FROM CMVColtaco3 WHERE id = %s"
                params = [food_id]

                # Executando a query no banco de retenção
                with get_retention_db_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params)
                        row = cursor.fetchone()

                        if row:
                            # Captura a descrição das colunas
                            columns = [col[0] for col in cursor.description]
                            food = dict(zip(columns, row))

                            # Ajustando valores com base no 'amount'
                            for key in food:
                                if key not in ['id', 'food_description', 'category']:
                                    try:
                                        value = float(food[key])
                                        food[key] = round((value * amount) / 100, 3)
                                    except ValueError:
                                        # Se a conversão para float falhar, mantém o valor original
                                        continue

                            results.append(food)
                        else:
                            return Response({"detail": f"Alimento com ID {food_id} não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # Serializando os dados
            serializer = CMVColtaco3Serializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)