import os
from uuid import uuid4

from dotenv import load_dotenv
import pytest
import requests

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(
            f"Variável de ambiente {name} não definida. "
            "Copie .env.example para .env e ajuste os valores antes de executar os testes."
        )
    return value


BASE_URL = os.getenv("BARRIGAREST_URL", "https://barrigarest.wcaquino.me")
EMAIL = _require_env("BARRIGAREST_EMAIL")
SENHA = _require_env("BARRIGAREST_PASS")


def validar_status(response, status_code, mensagem="Falha na requisição"):
    """Valida o status code e exibe a resposta em caso de erro."""
    assert response.status_code == status_code, (
        f"{mensagem}: esperado {status_code}, "
        f"retornado {response.status_code}: {response.text}"
    )


def criar_conta(token, nome=None):
    """Cria uma conta e retorna a resposta."""
    nome = nome or f"Conta Teste {uuid4()}"

    return requests.post(
        f"{BASE_URL}/contas",
        headers=token,
        json={"nome": nome}
    )


def excluir_conta(token, conta_id):
    """Exclui uma conta pelo ID."""
    return requests.delete(
        f"{BASE_URL}/contas/{conta_id}",
        headers=token
    )


@pytest.fixture(scope="session")
def token():
    """Autentica o usuário e retorna o header com JWT."""

    response = requests.post(
        f"{BASE_URL}/signin",
        json={
            "email": EMAIL,
            "senha": SENHA
        }
    )

    validar_status(
        response,
        200,
        "Falha na autenticação"
    )

    jwt_token = response.json()["token"]

    return {
        "Authorization": f"JWT {jwt_token}"
    }


@pytest.fixture
def conta_criada(token):
    """
    Cria uma conta para o teste e remove a conta
    automaticamente ao final do teste.
    """

    response = criar_conta(token)

    validar_status(
        response,
        201,
        "Falha ao criar conta"
    )

    conta = response.json()

    yield conta

    excluir_conta(token, conta["id"])


def test_login(token):
    """CT01 - Autenticação do usuário."""

    assert "Authorization" in token


def test_criar_conta(token):
    """CT02 - Criar uma conta."""

    nome = f"Conta Criada {uuid4()}"

    response = criar_conta(token, nome)

    validar_status(
        response,
        201,
        "Falha ao criar conta"
    )

    body = response.json()

    assert "id" in body
    assert "nome" in body
    assert isinstance(body["id"], int)
    assert body["nome"] == nome

    excluir_conta(token, body["id"])


def test_criar_conta_duplicada(token, conta_criada):
    """
    CT03 - Tentar criar uma conta que já existe.

    Esperado: HTTP 400.
    """

    response = criar_conta(
        token,
        conta_criada["nome"]
    )

    validar_status(
        response,
        400,
        "Erro ao criar conta duplicada"
    )

    body = response.json()

    assert "error" in body
    assert body["error"] != ""


def test_listar_contas(token):
    """CT04 - Listar contas."""

    response = requests.get(
        f"{BASE_URL}/contas",
        headers=token
    )

    validar_status(
        response,
        200,
        "Falha ao listar contas"
    )

    assert isinstance(response.json(), list)


def test_atualizar_conta(token, conta_criada):
    """
    CT05 - Atualizar uma conta.

    A fixture cria a conta antes do teste.
    """

    conta_id = conta_criada["id"]
    novo_nome = f"Conta Atualizada {uuid4()}"

    response = requests.put(
        f"{BASE_URL}/contas/{conta_id}",
        headers=token,
        json={"nome": novo_nome}
    )

    validar_status(
        response,
        200,
        "Falha ao atualizar conta"
    )

    body = response.json()

    assert body["id"] == conta_id
    assert body["nome"] == novo_nome


def test_excluir_conta(token, conta_criada):
    """
    CT06 - Excluir uma conta.

    A fixture cria a conta antes do teste.
    """

    conta_id = conta_criada["id"]

    response = excluir_conta(
        token,
        conta_id
    )

    validar_status(
        response,
        204,
        "Falha ao excluir conta"
    )

