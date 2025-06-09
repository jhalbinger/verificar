from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import json

# 🔐 Leer el JSON de credenciales desde variable de entorno
firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise Exception("❌ Falta la variable de entorno FIREBASE_CREDENTIALS")

cred_dict = json.loads(firebase_json)

# 🔄 Convertir los \\n a saltos de línea reales
cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

# 🔗 Inicializar Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://usuarios-5be49-default-rtdb.firebaseio.com/'
})

# 🚀 Crear app Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Microservicio de verificación activo."

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.get_json()
    numero = data.get("numero")

    if not numero:
        return jsonify({"error": "Falta el número"}), 400

    ref = db.reference("/usuarios")
    nombre = ref.child(numero).get()

    if nombre:
        return jsonify({"conocido": True, "nombre": nombre})
    else:
        return jsonify({"conocido": False})

# ⚙️ Configurar host y puerto para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
