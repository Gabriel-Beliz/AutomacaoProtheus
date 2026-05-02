# Automacao Protheus (Procedures)

1 - Descrição

Este projeto consiste em uma ferramenta de automação desenvolvida em Python utilizando Playwright e Tkinter, com o objetivo de facilitar o processo de:

- Consulta de procedures no Protheus
- Identificação de procedures não instaladas ou desatualizadas
- Download automático de pacotes de atualização via portal TOTVS
- Auxílio na instalação dessas procedures

A aplicação possui uma interface gráfica simples para entrada de credenciais e diretório de download.

---_---

2 - Tecnologias utilizadas

- Playwright (automação web)
- Tkinter (interface gráfica)
- OS / FileSystem (manipulação de arquivos)
- PyInstaller (geração de executável)

---_---

3 - Funcionalidades

- Login automático no Protheus (SIGACFG)
- Navegação até o dicionário de dados
- Identificação de procedures:
  - Não instaladas → download automático (via portal da totvs)
  - Desatualizadas → separação para instalação manual (pelo própria pagina
  
---_---

4 -  Fluxo da aplicação

1. Usuário preenche:

   - Credenciais do Protheus
   - Credenciais do portal TOTVS
   - Pasta de download

2. O sistema:

   - Abre o WebAgent
   - Realiza login no Protheus
   - Navega até Stored Procedures, dentro do protheus
   - Analisa o grid de procedures

3. Para cada procedure:

   - Se "Não instalado":
     - Busca atualização (no portal da totvs)
     - Faz download automático
     
   - Se "Desatualizado":
     - Adiciona à lista de instalação manual
     - Faz a instalação


 5 - Como executar

1 - Opção 1: Executar via Python

1. Instale as dependências:

- No seu terminal:
  pip install playwright
  playwright install

2. Execute o script:
  python main.py


2 - Opção 2: Executar via executável (.exe)

Caso você não queira depender de Python instalado na máquina, é possível gerar um executável utilizando o PyInstaller.

- Gerando o executável

1. Instale o PyInstaller:

- No seu terminal:
  pip install pyinstaller


2. Gere o executável:

- No seu terminal:
pyinstaller --onefile --noconsole main.py


3. O arquivo será gerado em:

- No seu terminal:
dist/main.exe
