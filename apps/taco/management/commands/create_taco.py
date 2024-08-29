from django.core.management.base import BaseCommand
import psycopg2
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Cria a tabela CMVColtaco3 no banco de retenção'

    def handle(self, *args, **kwargs):
        # Carrega variáveis do arquivo .env
        load_dotenv()

        # Variáveis de ambiente do banco de retenção
        PG_HOST_RETENTION = os.getenv("PG_HOST_RETENTION")
        PG_PORT_RETENTION = os.getenv("PG_PORT_RETENTION")
        PG_USER_RETENTION = os.getenv("PG_USER_RETENTION")
        PG_PASSWORD_RETENTION = os.getenv("PG_PASSWORD_RETENTION")
        DATABASE_RETENTION = os.getenv("DATABASE_RETENTION")

        # Conexão com o banco de retenção
        try:
            connection = psycopg2.connect(
                host=PG_HOST_RETENTION,
                port=PG_PORT_RETENTION,
                user=PG_USER_RETENTION,
                password=PG_PASSWORD_RETENTION,
                database=DATABASE_RETENTION
            )
            cursor = connection.cursor()

            # Comando para criar a tabela
            create_table_query = '''
            CREATE TABLE CMVColtaco3 (
                id SERIAL PRIMARY KEY,
                categoria VARCHAR(100) NOT NULL,
                numeroAlimento VARCHAR(10) NOT NULL,
                descricaoAlimento VARCHAR(255) NOT NULL,
                umidade VARCHAR(20) NOT NULL,
                energiaKcal VARCHAR(20) NOT NULL,
                energiaKj VARCHAR(20) NOT NULL,
                proteina VARCHAR(20) NOT NULL,
                lipideos VARCHAR(20) NOT NULL,
                colesterol VARCHAR(20) NOT NULL,
                carboidrato VARCHAR(20) NOT NULL,
                fibraAlimentar VARCHAR(20) NOT NULL,
                cinzas VARCHAR(20) NOT NULL,
                calcio VARCHAR(20) NOT NULL,
                magnesio VARCHAR(20) NOT NULL,
                manganes VARCHAR(20) NOT NULL,
                fosforo VARCHAR(20) NOT NULL,
                ferro VARCHAR(20) NOT NULL,
                sodio VARCHAR(20) NOT NULL,
                potassio VARCHAR(20) NOT NULL,
                cobre VARCHAR(20) NOT NULL,
                zinco VARCHAR(20) NOT NULL,
                retinol VARCHAR(20) NOT NULL,
                re VARCHAR(20) NOT NULL,
                rae VARCHAR(20) NOT NULL,
                tiamina VARCHAR(20) NOT NULL,
                riboflavina VARCHAR(20) NOT NULL,
                piridoxina VARCHAR(20) NOT NULL,
                niacina VARCHAR(20) NOT NULL,
                vitaminaC VARCHAR(20) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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
