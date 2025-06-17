from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User

app = Flask(__name__)

app.config['SECRETKEY'] = '111'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'pages/index.html'  # Перенаправление на главную, если не авторизован

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("pages/index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")  # Получаем логин из формы
    password = request.form.get("password")  # Получаем пароль из формы

    user = User.query.filter_by(username=username).first()

# Проверяем пользователя и пароль
    if user and user.check_password(password):
        login_user(user)  # Авторизуем пользователя
        flash("Вы успешно вошли!", "success")
        return redirect(url_for("pages/index.html"))  # Перенаправляем на главную
    else:
        flash("Неверный логин или пароль", "danger")
        return redirect(url_for("pages/index.html"))  # Возвращаем на главную с ошибкой


@app.route("/learning")
def learning():
    return render_template("pages/learning_page.html") 

@app.route('/team')
def inteam():
    return render_template('pages/team.html')

@app.route('/contacts')
def contacts():
    return render_template('pages/contacts.html')

@app.route('/test')
def test():
    return render_template('pages/test_chinese.html')

if __name__ == "__main__":
    app.run(debug=True)


