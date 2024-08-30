import os

import xlrd
from django.core.management.base import BaseCommand

from apps.taco.utils import get_retention_db_connection

class Command(BaseCommand):
    help = 'Importa dados específicos do arquivo XLS fixo para a tabela CMVColtaco3'

    def handle(self, *args, **kwargs):

        # Caminho fixo para o arquivo XLS
        xls_file_path = os.path.join('apps', 'taco', 'data', 'alimentos.xls')

        # Verifica se o arquivo existe
        if not os.path.isfile(xls_file_path):
            self.stdout.write(self.style.ERROR(f'O arquivo XLS {xls_file_path} não foi encontrado.'))
            return

        # Conexão com o banco de retenção usando a função utilitária
        try:
            with get_retention_db_connection() as connection:
                with connection.cursor() as cursor:
                    # Lê o arquivo XLS e insere dados na tabela
                    workbook = xlrd.open_workbook(xls_file_path)
                    sheet = workbook.sheet_by_index(0)

                    # Itera sobre as linhas da planilha
                    for row_idx in range(1, sheet.nrows):  # Começa da linha 1 para pular o cabeçalho
                        row = sheet.row(row_idx)

                        # Ignora linhas que contêm texto indicativo
                        if any(cell.value in ["Número do Alimento", "Descrição dos alimentos"] for cell in row):
                            continue

                        descricao = (row[1].value if row[1].value else '')[:1000]  # Truncar para 1000 caracteres

                        # Verifica se a descrição está vazia ou nula
                        if not descricao.strip():
                            continue

                        def format_value(value):
                            try:
                                return f"{float(value):.3f}" if value else '0.000'
                            except ValueError:
                                return '0.000'

                        umidade = format_value(row[2].value)
                        energiaKcal = format_value(row[3].value)
                        energiaKj = format_value(row[4].value)
                        proteina = format_value(row[5].value)
                        lipideos = format_value(row[6].value)
                        colesterol = format_value(row[7].value)
                        carboidrato = format_value(row[8].value)
                        fibraAlimentar = format_value(row[9].value)
                        cinzas = format_value(row[10].value)

                        cursor.execute(
                            """
                            INSERT INTO CMVColtaco3 (
                                descricaoAlimento, umidade, energiaKcal, energiaKj, proteina, lipideos,
                                colesterol, carboidrato, fibraAlimentar, cinzas
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """,
                            (
                                descricao,
                                umidade,
                                energiaKcal,
                                energiaKj,
                                proteina,
                                lipideos,
                                colesterol,
                                carboidrato,
                                fibraAlimentar,
                                cinzas
                            )
                        )
                    connection.commit()
                    self.stdout.write(self.style.SUCCESS(f'Dados importados com sucesso do arquivo {xls_file_path}.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar dados: {e}'))