url: https://commission-back.onrender.com/api/v1/health-check

- `python -m venv venv`

Ativar o ambiente virtual
- `.\venv\Scripts\Activate.ps1`

exibe no terminal (venv) camilaqj@Camis:~/personal/comission$

Instalar o taskipy
- `pip install taskipy`

Instalar requirements
- `pip install -r requirements-dev.txt`

Sair do modo venv
- `deactivate`

Remover venv
- `Remove-Item -Recurse -Force .\venv`

Atualizar requiments.txt após instalar uma dependencias
- `pip freeze > requirements-dev.txt`

---
```
comission-back/
├── .env                # Variáveis sensíveis (senhas, chaves de API, DB_URL). Nunca vai para o Git.
├── .gitignore          # Lista de arquivos/pastas que o Git deve ignorar (ex: venv, __pycache__, .env).
├── launch.json         # Configuração de Debug do VS Code (permite apertar F5 para debugar a API).
├── pyproject.toml      # O "Cérebro" do projeto. Centraliza scripts (taskipy) e metadados.
├── README.md           # Documentação principal do projeto (como instalar e rodar).
├── requirements.txt    # Lista de dependências e suas versões exatas para produção.
├── start.sh            # Script shell para deploy ou inicialização rápida em ambientes Linux/Docker.
│
└── app/                # Pasta raiz do código fonte da aplicação.
    ├── __init__.py     # Transforma a pasta 'app' em um pacote Python.
    ├── main.py         # O Ponto de Entrada. Onde o FastAPI é instanciado e as rotas são acopladas.
    │
    └── api/            # Subpacote que organiza toda a lógica de roteamento (URLs).
        ├── __init__.py
        │
        └── v1/         # Versão 1 da sua API. Garante compatibilidade futura.
            ├── __init__.py
            ├── api.py  # Agregador de rotas. Ele importa os endpoints e cria um roteador único.
            │
            └── endpoints/ # A lógica de negócio real por trás de cada URL.
                ├── __init__.py
                ├── health-check.py # Rota simples para verificar se o servidor está vivo (UP/DOWN).
                ├── products.py     # Endpoints relacionados a produtos (GET, POST, etc).
                └── users.py        # Endpoints relacionados a usuários (Cadastro, Login).
```
---

🚀 Estrutura de Automação do Projeto (FastAPI)
Este projeto utiliza o taskipy para centralizar todos os comandos de desenvolvimento e produção, eliminando a necessidade de scripts complexos ou Makefiles dependentes de sistema operacional.

🛠️ Configuração do Arquivo pyproject.toml
O arquivo pyproject.toml deve estar na raiz do projeto com a seguinte estrutura:

--- 
Ini, TOML
[tool.taskipy.tasks]
# Instala as dependências que já estão na lista (requirements)
install = "pip install -r requirements.txt"

# Salva as novas bibliotecas que você instalou manualmente na lista
save = "pip freeze > requirements.txt"

# Roda o servidor com auto-reload para desenvolvimento
run = "python -m uvicorn app.main:app --reload"

# Roda o servidor em modo "produção" (sem reload, mais estável)
start = "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

# Roda os testes (quando você tiver a pasta /tests)
test = "pytest"
📖 Como utilizar os comandos
Certifique-se de que seu ambiente virtual (venv) está ativado antes de executar os comandos abaixo no Git Bash ou terminal do VS Code.

1. Iniciar o Servidor de Desenvolvimento
Roda a API com a função de Hot Reload (reinicia automaticamente ao salvar arquivos).

Bash
task run
2. Parar o Servidor
Para interromper a execução do servidor local em qualquer momento:

Pressione Ctrl + C no teclado.

3. Gerenciar Dependências
Ao instalar uma nova biblioteca via pip install <nome>, use o comando abaixo para atualizar seu arquivo requirements.txt:

Bash
task save
Para instalar todas as dependências do projeto (ao clonar o repositório, por exemplo):

Bash
task install
4. Rodar em Produção
Inicia o servidor de forma otimizada, permitindo conexões externas e sem o overhead do auto-reload.

Bash
task start
📁 Estrutura de Pastas Esperada
Para que o comando task run funcione corretamente, mantenha esta organização:

app/ -> Pasta raiz do código.

main.py -> Onde está a variável app = FastAPI().

api/ -> Onde ficam os arquivos de rotas.

pyproject.toml -> Arquivo de scripts (este documento).

requirements.txt -> Lista de dependências.