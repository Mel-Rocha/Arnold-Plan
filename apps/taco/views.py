import ast

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.taco.exceptions import InvalidCategoryError
from apps.taco.serializers import CMVColtaco3Serializer
from apps.taco.utils import get_retention_db_connection


class CMVColtaco3ListView(APIView):
    """
    Objective: List all foods, paged.

    Parameters:
    optional:
    - page: (int) Page number.
    - page_size: (int) Number of records per page.

    Returns:
    JSON.
    """

    @staticmethod
    def get(request):
        description = request.query_params.get('description', None)
        page = int(request.query_params.get('page', 1))  # Página atual
        page_size = int(request.query_params.get('page_size', 10))  # Tamanho da página

        # Construa a query para obter o total de registros
        count_query = "SELECT COUNT(*) FROM CMVColtaco3"
        if description:
            count_query += " WHERE food_description LIKE %s"
            count_params = [f'%{description}%']
        else:
            count_params = []

        with get_retention_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(count_query, count_params)
                total_records = cursor.fetchone()[0]

        # Construa a query para obter os registros paginados
        query = "SELECT * FROM CMVColtaco3"
        if description:
            query += " WHERE food_description LIKE %s"
        query += " LIMIT %s OFFSET %s"
        params = []
        if description:
            params.append(f'%{description}%')
        params.extend([page_size, (page - 1) * page_size])

        # Execute a query no banco de retenção
        with get_retention_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]

        foods = [dict(zip(columns, row)) for row in rows]

        # Serializando os dados
        serializer = CMVColtaco3Serializer(foods, many=True)

        # Calcular total de páginas
        total_pages = (total_records + page_size - 1) // page_size

        # Montar a resposta com informações de paginação
        response_data = {
            'total_records': total_records,
            'total_pages': total_pages,
            'current_page': page,
            'page_size': page_size,
            'results': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CMVColtaco3DetailView(APIView):
    """
    Objective: Calculates the nutritional values of the food based on the amount in grams informed.

    Parameters:
    mandatory:
    - param: (str) Description or ID of the food.
    - amount: (str) Amount in grams.

    Returns:
    JSON.
    """

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
                query = """
                SELECT * 
                FROM CMVColtaco3
                WHERE food_description ILIKE %s
                ORDER BY similarity(food_description, %s) DESC
                LIMIT 1
                """
                params = [f'%{param}%', param]

            with get_retention_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    rows = cursor.fetchall()

                    if not rows:
                        return Response({"detail": "Alimento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

                    # Captura a descrição das colunas
                    columns = [col[0] for col in cursor.description]
                    row = rows[0]  # Seleciona a primeira linha retornada

                    food = dict(zip(columns, row))

                    # Ajustando valores com base no 'amount'
                    for key in food:
                        if key not in ['id', 'food_description', 'category']:
                            try:
                                value = float(food[key])
                                food[key] = round((value * amount) / 100, 3)
                            except ValueError:
                                continue

                    # Serializando o dado
                    serializer = CMVColtaco3Serializer(food)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CMVColtaco3CategoryView(APIView):
    """
    Objective: List all foods in a specific category, paged.

    Parameters:
    mandatory:
    - category: (str) Category of the food.

    optional:
    - page: (int) Page number.
    - page_size: (int) Number of records per page.

    Returns:
    JSON.
    """

    @staticmethod
    def get(request, category):
        # Verifica se a categoria fornecida é válida usando a exceção personalizada
        valid_categories = InvalidCategoryError.VALID_CATEGORIES
        if category not in valid_categories:
            raise InvalidCategoryError(category)

        page = int(request.query_params.get('page', 1))  # Página atual
        page_size = int(request.query_params.get('page_size', 10))  # Tamanho da página

        # Construa a query para obter o total de registros
        count_query = "SELECT COUNT(*) FROM CMVColtaco3 WHERE category = %s"
        count_params = [category]

        with get_retention_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(count_query, count_params)
                total_records = cursor.fetchone()[0]

        # Construa a query para obter os registros paginados
        query = "SELECT * FROM CMVColtaco3 WHERE category = %s"
        query += " LIMIT %s OFFSET %s"
        params = [category, page_size, (page - 1) * page_size]

        # Execute a query no banco de retenção
        try:
            with get_retention_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]

            foods = [dict(zip(columns, row)) for row in rows]

            # Serializando os dados
            serializer = CMVColtaco3Serializer(foods, many=True)

            # Calcular total de páginas
            total_pages = (total_records + page_size - 1) // page_size

            # Montar a resposta com informações de paginação
            response_data = {
                'total_records': total_records,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size,
                'results': serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CMVColtaco3BulkDetailView(APIView):
    """
    Objective: Calculates the nutritional values of the food based on the amount in grams informed,
    can be used for a single food or many.

    Parameters:
    - food_list: List of dictionaries containing the 'food_id' and 'quantity' keys.

    Returns:
    JSON, list of dictionaries.
    """

    @staticmethod
    def get(request, food_list):
        try:
            # Converte a string da URL para uma lista de dicionários
            try:
                food_list = ast.literal_eval(food_list)
            except (ValueError, SyntaxError):
                return Response({"detail": "O parâmetro 'food_list' deve ser uma lista de dicionários válida."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(food_list, list):
                return Response({"detail": "O parâmetro 'food_list' deve ser uma lista de dicionários."}, status=status.HTTP_400_BAD_REQUEST)

            results = []

            for item in food_list:
                if not isinstance(item, dict) or 'food_id' not in item or 'quantity' not in item:
                    return Response({"detail": "Cada item na lista deve ser um dicionário contendo as chaves 'id_food' e 'quantity'."}, status=status.HTTP_400_BAD_REQUEST)

                food_id = item['food_id']
                amount = item['quantity']

                try:
                    amount = float(amount)
                except ValueError:
                    return Response({"detail": f"O parâmetro 'quantity' para o alimento com ID {food_id} deve ser um número válido."}, status=status.HTTP_400_BAD_REQUEST)

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
