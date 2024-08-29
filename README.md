# Arnold Plan 💪 🔱


## Variáveis de Ambiente
### Banco Local 🐘

* DATABASE_URL=postgres://username:password@host:port/database_name

### Banco Retenção 🐘
- PG_HOST_RETENTION: Deve ser obtido com o comando abaixo.
- PG_PORT_RETENTION: Porta
- PG_USER_RETENTION: Usuário
- PG_PASSWORD_RETENTION: Senha
- DATABASE_RETENTION: Nome do banco de dados

* O host deve ser obtido por meio do seguinte comando que descobrirá o ip real
do servidor postgres.
```bash
# Linux
ip a 

# Windows
ipconfig
```

Rodar Localmente 🏠
* Passo 1 - Instale os módulos via VENV


```bash
# Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

* Passo 2 - Instale as dependências
```bash
pip install -r requirements.txt
```

* Passo 3 - Aplique as migrações das tabelas
```bash
python manage.py migrate
```

* Passo 4 - De os comandos personalizados para criar e carregar o banco de informações nutricionais

```bash 
# Criar a tabela
python manage.py create_taco

# Carregar a tabela
python manage.py insert_taco
```

* Passo 5 - Execute o servidor
```bash
python manage.py runserver
```



## Comandos Uteis Django 🚀
### Banco de Dados 🎲
Permite execação de comandos SQL diretamente no banco de dados.

```bash
python manage.py dbshell
```

Visualizar todas as tabelas
```bash
\dt
```

Visualizar a estrutura de uma tabela

Estrutura Básica
```bash
\d table_name  
```

Estrutura Detalhada (incluindo informações adicionais como descrições de colunas, índices e tabelas associadas).
```bash
\d+ table_name 
```

### Interagir com a API Django via shell 🖥️
```bash
python manage.py shell
```

Faça testes com suas models no shell

```bash
from django.contrib.auth.models import User

users = User.objects.all()
print(users)
Visualizar todas as urls do projeto

# Importar get_resolver
from django.urls import get_resolver

# Obter todas as URLs configuradas
urls = get_resolver().url_patterns

# Iterar sobre as URLs e imprimir cada uma
for url in urls:
    print(url)
```

# Template .env 📝
```bash
# GERAL
DEBUG="True"
SECRET_KEY="django-insecure-%%!5v*7a-v4cjkq%f85c3p7&=5u0wo06!nk5d9&@4b!k5tr"
ALLOWED_HOSTS="*"
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,https://example.com
CSRF_TRUSTED_ORIGINS=http://example.com,https://example.com

# DATABASE (DEFAULT SQLITE3)
DATABASE_URL="postgresql://user:password@localhost:5432/database_name"

# RETENTION
PG_HOST_RETENTION="localhost"
PG_PORT_RETENTION="5432"
PG_USER_RETENTION="user"
PG_PASSWORD_RETENTION="password"
DATABASE_RETENTION="database_name"

```