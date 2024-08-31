from django.core.management.base import BaseCommand

from apps.taco.utils import get_retention_db_connection


class Command(BaseCommand):
    help = 'Cria a tabela CMVColtaco3 no banco de retenção e garante que a extensão pg_trgm esteja instalada'

    def handle(self, *args, **kwargs):
        # Conexão com o banco de retenção
        connection = None
        cursor = None
        try:
            connection = get_retention_db_connection()
            cursor = connection.cursor()

            # Comando para criar a extensão pg_trgm
            create_extension_query = '''
            CREATE EXTENSION IF NOT EXISTS pg_trgm;
            '''
            cursor.execute(create_extension_query)

            # Comando para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS CMVColtaco3 (
                id SERIAL PRIMARY KEY,
                food_description VARCHAR(1000) NOT NULL,
                moisture VARCHAR(200) NOT NULL,
                energy_kcal VARCHAR(200) NOT NULL,
                energy_kj VARCHAR(200) NOT NULL,
                protein VARCHAR(200) NOT NULL,
                lipids VARCHAR(200) NOT NULL,
                cholesterol VARCHAR(200) NOT NULL,
                carbohydrates VARCHAR(200) NOT NULL,
                dietary_fiber VARCHAR(200) NOT NULL,
                ashes VARCHAR(200) NOT NULL,
                category VARCHAR(200) NOT NULL
            );
            '''

            # Executa os comandos
            cursor.execute(create_table_query)
            connection.commit()
            self.stdout.write(self.style.SUCCESS("Tabela CMVColtaco3 criada com sucesso no banco de retenção."))
            self.stdout.write(self.style.SUCCESS("Extensão pg_trgm garantida no banco de retenção."))

        except Exception as error:
            self.stdout.write(self.style.ERROR(f"Erro ao conectar ou criar a tabela: {error}"))

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
