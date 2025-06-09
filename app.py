# verificador-nombre/app.py

from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

# Inicializamos la app de Firebase solo una vez
cred = credentials.Certificate("usuarios-5be49-firebase-adminsdk-fbsvc-644630ef9d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://usuarios-5be49-default-rtdb.firebaseio.com/'
})

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

if __name__ == "__main__":
    app.run(debug=True)
