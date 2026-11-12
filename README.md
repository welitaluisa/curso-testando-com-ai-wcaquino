# Material do Curso Testando com AI

Projeto com exemplos e exercícios de automação de testes e inteligência artificial, incluindo geração de casos de teste com contexto, testes de API e interface, e testes visuais.

O material foi desenvolvido durante o curso **Testando com AI**, ministrado por **Francisco Wagner Costa Aquino**, com carga horária total de **6 horas**.

Aplicação usada nos testes de API: [BarrigaRest](https://barrigarest.wcaquino.me/)

Repositório do curso: [curso-testando-com-ai-wcaquino](https://github.com/welitaluisa/curso-testando-com-ai-wcaquino)

## Conteúdo

- `assistente-simples/`: exemplos de assistentes com Gemini e uso de contexto em prompts.
- `assistente-complexo/`: API para consulta e envio de arquivos de contexto.
- `automacao/`: testes de interface com Selenium, testes de API e cenários em Gherkin.
- `casos-de-teste/`: histórias de usuário e exemplos de casos de teste.
- `copilot/`: exemplos de testes de API, interface e testes unitários.
- `self-healing/`: exemplo de automação com Healenium e serviços auxiliares via Docker.
- `visual/`: scripts e páginas para experimentos com testes visuais.

## Tecnologias

- Python
- Pytest
- Selenium e WebDriver Manager
- Eyes-Selenium
- Flask e PyJWT
- Google GenAI
- python-dotenv
- Docker e Healenium

## Requisitos

- Python instalado
- Git
- Docker, para executar os exemplos de self-healing
- Credenciais de teste para as aplicações externas
- Chave da API Gemini para executar os exemplos que usam o modelo

## Instalação

Na raiz do projeto, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Configure as variáveis de ambiente dos testes de automação. No Windows:

```powershell
copy .env.example .env
```

No macOS ou Linux:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com os dados de acesso necessários:

```env
TEST_LOGIN_URL=https://seubarriga.wcaquino.me/
TEST_LOGIN_EMAIL=seu_email
TEST_LOGIN_PASS=sua_senha
BARRIGAREST_URL=https://barrigarest.wcaquino.me
BARRIGAREST_EMAIL=seu_email
BARRIGAREST_PASS=sua_senha
```

Não compartilhe nem faça commit do arquivo `.env` ou de chaves de API.

## Executar os testes de automação

A partir da raiz do projeto:

```bash
python -m pytest automacao/test_login.py -q
python -m pytest automacao/test_api.py -q
```

Para mais detalhes sobre os testes, consulte [`automacao/README_TEST.md`](automacao/README_TEST.md).

O repositório também contém exemplos e exercícios adicionais. Consulte os arquivos de cada pasta para conhecer suas configurações e instruções específicas.

## Uso da API Gemini

Os exemplos em `assistente-simples/` usam a biblioteca Google GenAI para enviar prompts com instruções de contexto. Configure uma chave válida antes de executar os scripts e mantenha-a fora do controle de versão. Verifique a configuração de cada exemplo antes da execução.

## Segurança

- Nunca faça commit de arquivos `.env`, senhas ou chaves de API.
- Use credenciais de teste, não senhas pessoais.
- Os testes dependem da disponibilidade das aplicações externas e podem precisar de ajustes caso suas interfaces ou APIs mudem.
