from flask import Flask

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_muito_forte'