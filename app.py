from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib

app = Flask(name)
CORS(app)  # Permite que o frontend em JavaScript acesse a API

usuarios = []

def criptografar_senha(senha):
return hashlib.sha256(senha.encode()).hexdigest()

#Rota principal

@app.route('/')
def home():
return jsonify({"mensagem": "API de Usuários Adote+ está online"})

#Rota para listar usuários

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
lista_publica = [{"id": u["id"], "nome": u["nome"], "email": u["email"]} for u in usuarios]
return jsonify(lista_publica)

#Rota para cadastrar novo usuário

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
dados = request.get_json()

if not dados.get("nome") or not dados.get("email") or not dados.get("senha"):  
    return jsonify({"erro": "Campos nome, email e senha são obrigatórios."}), 400  

for u in usuarios:  
    if u["email"] == dados["email"]:  
        return jsonify({"erro": "Email já cadastrado!"}), 400  

novo_usuario = {  
    "id": len(usuarios) + 1,  
    "nome": dados["nome"],  
    "email": dados["email"],  
    "senha": criptografar_senha(dados["senha"])   
}  

usuarios.append(novo_usuario)  
return jsonify({  
    "mensagem": "Usuário cadastrado com sucesso!",  
    "usuario": {  
        "id": novo_usuario["id"],  
        "nome": novo_usuario["nome"],  
        "email": novo_usuario["email"]  
    }  
}), 201

#Rota para login (verificação de usuário)

@app.route('/login', methods=['POST'])
def login():
dados = request.get_json()
email = dados.get("email")
senha = dados.get("senha")

if not email or not senha:  
    return jsonify({"erro": "Informe email e senha!"}), 400  

senha_hash = criptografar_senha(senha)  
for u in usuarios:  
    if u["email"] == email and u["senha"] == senha_hash:  
        return jsonify({"mensagem": f"Bem-vindo(a), {u['nome']}!"}), 200  

return jsonify({"erro": "Email ou senha incorretos!"}), 401

#Executar servidor

if name == 'main':
app.run(debug=True)
