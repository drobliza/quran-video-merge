from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "موقع دمج كرومات القرآن جاهز 🚀"
