from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Привет, это мой первый Flask-проект!"

if __name__ == "__main__":
    app.run(debug=True)  # Запуск сервера в режиме отладки
