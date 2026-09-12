from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "chave_secreta"

# Simulação de dados
contas = []
user = {"user@mail.com": "123456"}

def gerar_token(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not validar_token(token):
            return jsonify({"error": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    if user.get(email) == senha:
        token = gerar_token(email)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Credenciais inválidas"}), 401

@app.route('/contas', methods=['POST'])
@token_required
def criar_conta():
    data = request.get_json()
    nome = data.get('nome')
    if any(c['nome'] == nome for c in contas):
        return jsonify({"error": "Conta já existe"}), 400
    nova_conta = {"id": len(contas) + 1, "nome": nome}
    contas.append(nova_conta)
    return jsonify(nova_conta), 201

@app.route('/contas', methods=['GET'])
@token_required
def listar_contas():
    return jsonify(contas), 200

@app.route('/contas/<int:id>', methods=['PUT'])
@token_required
def atualizar_conta(id):
    data = request.get_json()
    nome = data.get('nome')
    for conta in contas:
        if conta['id'] == id:
            conta['nome'] = nome
            return jsonify(conta), 200
    return jsonify({"error": "Conta não encontrada"}), 404

@app.route('/contas/<int:id>', methods=['DELETE'])
@token_required
def remover_conta(id):
    for conta in contas:
        if conta['id'] == id:
            contas.remove(conta)
            return '', 204
    return jsonify({"error": "Conta não encontrada"}), 404

@app.route('/reset', methods=['GET'])
@token_required
def resetar():
    contas.clear()
    return jsonify({"message": "Contas resetadas"}), 200

if __name__ == '__main__':
    app.run(debug=True)