import os
import re

import xlrd
from django.core.management.base import BaseCommand

from apps.taco.utils import get_retention_db_connection


class Command(BaseCommand):
    help = 'Imports specific data from the fixed XLS file into the CMVColtaco3 table'

    def handle(self, *args, **kwargs):
        # Fixed path to the XLS file
        xls_file_path = os.path.join('apps', 'taco', 'data', 'alimentos.xls')

        # Check if the file exists
        if not os.path.isfile(xls_file_path):
            self.stdout.write(self.style.ERROR(f'The XLS file {xls_file_path} was not found.'))
            return

        # Connection to the retention database using the utility function
        try:
            with get_retention_db_connection() as connection:
                with connection.cursor() as cursor:
                    # Read the XLS file and insert data into the table
                    workbook = xlrd.open_workbook(xls_file_path)
                    sheet = workbook.sheet_by_index(0)

                    current_category = None

                    # List of texts to ignore
                    discard_text = [
                        "Número do Alimento", "Descrição dos alimentos",
                        "as análises estão sendo reavaliadas",
                        "Valores em branco nesta tabela: análises não solicitadas",
                        "Teores alcoólicos (g/100g): ¹ Cana, aguardente: 31,1 e ² Cerveja, pilsen: 3,6.",
                        "Abreviações: g: grama; mg: micrograma; kcal: kilocaloria; kJ: kilojoule; mg:miligrama; NA: não aplicável; Tr: traço. Adotou-se traço nas seguintes situações: a)valores de nutrientes arredondados para números que caiam entre 0 e 0,5; b) valores de nutrientes arredondados para números com uma casa decimal que caiam entre 0 e 0,05; c) valores de nutrientes arredondados para números com duas casas decimais que caiam entre 0 e 0,005 e; d) valores abaixo dos limites de quantificação (29).",
                        "Limites de Quantificação: a) composição centesimal: 0,1g/100g; b) colesterol: 1mg/100g; c) Cu, Fe, Mn, e Zn: 0,001mg/100g; d) Ca, Na: 0,04mg/100g; e) K e P: 0,001mg/100g; f) Mg 0,015mg/100g; g) tiamina, riboflavina e piridoxina: 0,03mg/100g; h) niacina e vitamina C: 1mg/100g; i) retinol em produtos cárneos e outros: 3μg/100g e; j) retinol em lácteos: 20μg/100g.",
                        "Valores correspondentes à somatória do resultado analítico do retinol mais o valor calculado com base no teor de carotenóides segundo o livro Fontes brasileiras de carotenóides: tabela brasileira de composição de carotenóides em alimentos.",
                        "Valores retirados do livro Fontes brasileiras de carotenóides: tabela brasileira de composição de carotenóides em alimentos."
                    ]

                    # Function to remove punctuation
                    def clean_description(description):
                        return re.sub(r'[^\w\s]', '', description).strip()

                    # Iterate over the rows in the sheet
                    for row_idx in range(sheet.nrows):
                        row = sheet.row(row_idx)

                        # Check if the row contains a category
                        if row[0].value in [
                            "Cereais e derivados",
                            "Verduras, hortaliças e derivados",
                            "Frutas e derivados",
                            "Gorduras e óleos",
                            "Pescados e frutos do mar",
                            "Carnes e derivados",
                            "Leite e derivados",
                            "Bebidas (alcoólicas e não alcoólicas)",
                            "Ovos e derivados",
                            "Produtos açucarados",
                            "Miscelâneas",
                            "Outros alimentos industrializados",
                            "Alimentos preparados",
                            "Leguminosas e derivados",
                            "Nozes e sementes"
                        ]:
                            current_category = row[0].value
                            continue  # Skip the category row

                        # Ignore rows that contain indicative text or strange values
                        if any(cell.value in discard_text for cell in row):
                            continue

                        description = (row[1].value if row[1].value else '')[:1000]  # Truncate to 1000 characters

                        # Check if the description is empty or null
                        if not description.strip():
                            continue

                        # Clean the description
                        cleaned_description = clean_description(description)

                        def format_value(value):
                            try:
                                return f"{float(value):.3f}" if value else '0.000'
                            except ValueError:
                                return '0.000'

                        moisture = format_value(row[2].value)
                        energy_kcal = format_value(row[3].value)
                        energy_kj = format_value(row[4].value)
                        protein = format_value(row[5].value)
                        lipids = format_value(row[6].value)
                        cholesterol = format_value(row[7].value)
                        carbohydrates = format_value(row[8].value)
                        dietary_fiber = format_value(row[9].value)
                        ashes = format_value(row[10].value)

                        cursor.execute(
                            """
                            INSERT INTO CMVColtaco3 (
                                food_description, moisture, energy_kcal, energy_kj, protein, lipids,
                                cholesterol, carbohydrates, dietary_fiber, ashes, category
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """,
                            (
                                cleaned_description,
                                moisture,
                                energy_kcal,
                                energy_kj,
                                protein,
                                lipids,
                                cholesterol,
                                carbohydrates,
                                dietary_fiber,
                                ashes,
                                current_category  # Add the category
                            )
                        )
                    connection.commit()
                    self.stdout.write(self.style.SUCCESS(f'Data successfully imported from the file {xls_file_path}.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
