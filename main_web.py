from flask import Flask
from main import actualizar_productos

app = Flask(__name__)

@app.route('/')
def home():
    return "Amazon Alertas corriendo."

@app.route('/run')
def run_script():
    actualizar_productos()
    return "Script ejecutado correctamente."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
