Passo 1: Ativar seu ambiente virtual (venv)

O venv é a “caixa isolada” do seu projeto. Tudo que você instala dentro dele não afeta outros projetos nem o Python global.

No PowerShell, dentro da pasta do seu projeto:

.\venv\Scripts\Activate.ps1

Depois disso, o prompt vai mudar para algo como:

(venv) PS C:\Users\camil\OneDrive\Documentos\personal\commission-back>

⚠️ Importante: se você instalar qualquer biblioteca com o venv desativado, o pip vai instalar no Python global e seu projeto não vai enxergar.

Passo 2: Instalar a biblioteca

Suponha que você quer instalar pandas:

pip install pandas

O pip vai baixar e instalar a versão mais recente no venv ativo.

Você pode instalar múltiplas libs de uma vez:

pip install pandas python-multipart httpx
Passo 3: Testar se a biblioteca está instalada

Depois da instalação, teste:

python -c "import pandas; print(pandas.__version__)"

Se imprimir a versão, a biblioteca está instalada e funcionando no venv.

Faça isso sempre que instalar uma nova lib para garantir que o Python do venv está usando o pacote certo.

Passo 4: Atualizar o requirements.txt

O requirements.txt é a lista de bibliotecas do projeto. Quando alguém clonar seu projeto, ele só precisa rodar pip install -r requirements.txt para ter todas as dependências.

Depois de instalar novas libs:

pip freeze > requirements.txt

Isso sobrescreve o arquivo com todas as libs atuais do venv.

Agora pandas, python-multipart e todas as outras que você instalou estarão listadas.

Passo 5: Usar a biblioteca no código

No seu código Python, importe normalmente:

import pandas as pd
from fastapi import FastAPI, UploadFile, Form

Não precisa de caminho especial se estiver usando o venv.

Dicas importantes para não perder dependências

Sempre ative o venv antes de instalar qualquer lib.

Sempre use pip freeze > requirements.txt depois de instalar.

Evite instalar diretamente no Python global, isso confunde o projeto.

Se receber erro tipo ModuleNotFoundError, verifique:

O venv está ativo?

A lib está no requirements.txt?

Você está usando o Python correto?