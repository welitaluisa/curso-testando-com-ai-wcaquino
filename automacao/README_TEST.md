Teste de Login (Selenium)

Instalação:

```bash
python -m pip install -r automacao/requirements_test.txt
```

Antes de executar, crie um arquivo `.env` a partir do exemplo:

```bash
copy .env.example .env
```

Em seguida, ajuste os valores de:
- `TEST_LOGIN_URL`
- `TEST_LOGIN_EMAIL`
- `TEST_LOGIN_PASS`
- `BARRIGAREST_URL`
- `BARRIGAREST_EMAIL`
- `BARRIGAREST_PASS`

Nunca commite o arquivo `.env`.

Execução:

```bash
python -m pytest automacao/test_login.py -q
python -m pytest automacao/test_api.py -q
```

Saídas:
- Código de saída `0` -> teste aprovado
- Código de saída `1` -> teste falhou (login não efetuado)
- Código de saída `2` -> elementos da página não encontrados