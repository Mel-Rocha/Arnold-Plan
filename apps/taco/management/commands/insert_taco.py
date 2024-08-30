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

                    categoria_atual = None

                    # Lista de textos indicativos para ignorar
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

                    # Itera sobre as linhas da planilha
                    for row_idx in range(sheet.nrows):
                        row = sheet.row(row_idx)

                        # Verifica se a linha contém uma categoria
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
                            categoria_atual = row[0].value
                            continue  # Pular a linha de categoria

                        # Ignora linhas que contêm texto indicativo ou valores estranhos
                        if any(cell.value in discard_text for cell in row):
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
                                colesterol, carboidrato, fibraAlimentar, cinzas, categoria
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
                                cinzas,
                                categoria_atual  # Adiciona a categoria
                            )
                        )
                    connection.commit()
                    self.stdout.write(self.style.SUCCESS(f'Dados importados com sucesso do arquivo {xls_file_path}.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar dados: {e}'))
