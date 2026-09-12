from google import genai
from google.genai import types
import textwrap

GEMINI_API_KEY = '' # Insira sua chave da API aqui
MODEL = 'gemini-2.5-flash'

PROMPT_USUARIO = """
Crie casos de teste para a funcionalidade de cadastro de conta.


Título: Cadastro de conta

Como um usuário autenticado
Eu quero criar uma conta informando apenas o nome
Para organizar minhas informações na plataforma

Critérios de Aceitação:
- A interface exibe o campo “Nome da conta” e o botão “Salvar”.
- “Nome da conta” é obrigatório.
- Ao salvar com um nome válido, a conta é criada e vinculada ao usuário logado.
- Ao tentar salvar sem nome (ou só com espaços), o sistema exibe a mensagem “Nome da conta é obrigatório.”.
"""

CONTEXTO = """
Erros comuns:
- No such element: Geralmente causado quando o locator do elemento está errado (ou foi modificado)
- API 500 errors: geralmente devido a variáveis de ambiente mal configuradas.
Padrões de Teste:
- Siga o formato Gherkin para cenários E2E.
- Quando for necessário criar automações de UI, utilize Python+Selenium.
- Casos de testes possuem um identificador seguindo o padrão CT-001
- Quando criando casos de testes, sugira casos negativos também.
"""

def run_with_context(system_instruction: str, user_input: str) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    resp = client.models.generate_content(
        model=MODEL,
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    return resp.text

if __name__ == "__main__":
    try:
        out = run_with_context(CONTEXTO, PROMPT_USUARIO)
        output_filename = 'base_codigo_saida.txt'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent(out).strip())
        print(f"Saída salva em {output_filename}")
    except Exception as e:
        print(f"[ERRO] {e}")
