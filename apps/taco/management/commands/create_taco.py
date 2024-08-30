from django.core.management.base import BaseCommand

from apps.taco.utils import get_retention_db_connection

class Command(BaseCommand):
    help = 'Cria a tabela CMVColtaco3 no banco de retenção'

    def handle(self, *args, **kwargs):
        # Conexão com o banco de retenção
        try:
            connection = get_retention_db_connection()
            cursor = connection.cursor()

            # Comando para criar a tabela
            create_table_query = '''
            CREATE TABLE CMVColtaco3 (
                id SERIAL PRIMARY KEY,
                descricaoAlimento VARCHAR(1000) NOT NULL,
                umidade VARCHAR(200) NOT NULL,
                energiaKcal VARCHAR(200) NOT NULL,
                energiaKj VARCHAR(200) NOT NULL,
                proteina VARCHAR(200) NOT NULL,
                lipideos VARCHAR(200) NOT NULL,
                colesterol VARCHAR(200) NOT NULL,
                carboidrato VARCHAR(200) NOT NULL,
                fibraAlimentar VARCHAR(200) NOT NULL,
                cinzas VARCHAR(200) NOT NULL,
                categoria VARCHAR(200) NOT NULL
            );
            '''

            # Executa o comando para criar a tabela
            cursor.execute(create_table_query)
            connection.commit()
            self.stdout.write(self.style.SUCCESS("Tabela CMVColtaco3 criada com sucesso no banco de retenção."))

        except Exception as error:
            self.stdout.write(self.style.ERROR(f"Erro ao conectar ou criar a tabela: {error}"))

        finally:
            if connection:
                cursor.close()
                connection.close()
