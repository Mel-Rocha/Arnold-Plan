from openpyxl import Workbook
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from openpyxl.styles import Border, Side, Alignment
from rest_framework.permissions import IsAuthenticated

from apps.diet.models import Diet
from apps.user.models import Athlete
from apps.core.permissions import IsAthleteUser
from apps.diet.serializers import DietSerializer
from apps.daily_records.models import DailyRecords
from apps.core.mixins import AthleteNutritionistPermissionMixin


class DietViewSet(AthleteNutritionistPermissionMixin):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset_model_class(self):
        return Diet

    def get_related_model_id(self):
        return self.request.data.get('athlete')

    def get_related_model_class(self):
        return Athlete

    @action(detail=False, methods=['get'], url_path='diet-count', permission_classes=[IsAuthenticated, IsAthleteUser])
    def diet_dates(self, request):
        diets = Diet.objects.all().values('id', 'initial_date', 'final_date')
        return Response(diets)


    def destroy(self, request, *args, **kwargs):
        diet = self.get_object()
        daily_records = DailyRecords.objects.filter(meal__diet=diet)

        if daily_records.exists():
            return Response(
                {"detail": "Cannot delete this diet because the athlete has already started executing it and has daily records associated with its meals."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'], url_path='export', permission_classes=[IsAuthenticated])
    def export_diet(self, request, pk=None):
        diet = self.get_object()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=diet_{diet.id}.xlsx'

        # Criação da planilha
        wb = Workbook()
        ws = wb.active
        ws.title = "Diet"

        # Remover as linhas de grade
        ws.sheet_view.showGridLines = False

        # Adicionando meta, observações e datas
        ws['A1'] = "Meta"
        ws['A2'] = "Observações"
        ws['A3'] = "Data Inicial"
        ws['A4'] = "Data Final"

        # Mesclando as células da coluna A e B
        ws.merge_cells('A1:B1')
        ws.merge_cells('A2:B2')
        ws.merge_cells('A3:B3')
        ws.merge_cells('A4:B4')

        # Preenchendo as informações na célula mesclada (A) após a mesclagem
        ws['A1'] = f"Meta: {diet.goal}"  # Preenchendo a meta
        ws['A2'] = f"Observações: {diet.observations}"  # Preenchendo as observações
        ws['A3'] = f"Data Inicial: {diet.initial_date.strftime('%Y-%m-%d')}"  # Preenchendo a data inicial
        ws['A4'] = f"Data Final: {diet.final_date.strftime('%Y-%m-%d')}"  # Preenchendo a data final

        # Espaçamento para cabeçalho da tabela de alimentos
        ws.append([""])

        # Adicionando cabeçalhos da tabela
        headers = ["Refeição", "Horário", "Alimento", "kcal", "PTN", "CHO", "LIP", "Quantidade", "Fibras (g)"]
        ws.append(headers)

        # Ajustando largura das colunas
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 40

        # Estilo das bordas
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                             bottom=Side(style='thin'))

        row_num = 7
        for meal in diet.meals.all():
            first_row = row_num
            foods = meal.foods  # Acessando os alimentos da refeição (JSONField)

            # Verificar se foods é uma lista de dicionários
            if isinstance(foods, list) and foods:
                for food in foods:
                    ws.append([
                        meal.name,  # Nome da refeição
                        meal.time,  # Horário da refeição
                        food.get('food_description', ''),  # Nome do alimento
                        food.get('energy_kcal', 0),  # Valor calórico
                        food.get('protein', 0),  # Proteínas
                        food.get('carbohydrates', 0),  # Carboidratos
                        food.get('lipids', 0),  # Lipídios
                        food.get('quantity', 0),  # Quantidade
                        food.get('dietary_fiber', 0)  # Fibras
                    ])
                    row_num += 1
            else:
                # Caso não tenha alimentos na refeição
                ws.append([
                    meal.name,  # Nome da refeição
                    meal.time,  # Horário da refeição
                    "Sem alimentos",  # Indicação de que não há alimentos
                    '', '', '', '', '', ''  # Células vazias para as colunas de nutrientes
                ])
                row_num += 1

            # Verificar se a refeição tem mais de um alimento antes de mesclar
            if row_num - first_row > 1:
                ws.merge_cells(start_row=first_row, start_column=1, end_row=row_num - 1,
                               end_column=1)  # Mesclando "Refeição"
                ws.merge_cells(start_row=first_row, start_column=2, end_row=row_num - 1,
                               end_column=2)  # Mesclando "Horário"

            # Aplicando bordas e alinhamento às células
            for col in range(1, len(headers) + 1):
                for row in range(first_row, row_num):
                    ws.cell(row=row, column=col).border = thin_border
                    ws.cell(row=row, column=col).alignment = Alignment(horizontal='center', vertical='center')

            # Pular uma linha entre as refeições
            ws.append([""])
            row_num += 1

        # Salvando o arquivo no response
        wb.save(response)
        return response