from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import  os

app = Flask(__name__)

app.config['SECRET_KEY'] = '111'
# Убедимся, что папка instance существует
app.instance_path = os.path.join(os.getcwd(), 'instance')
os.makedirs(app.instance_path, exist_ok=True)
# Полный путь к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'  # Перенаправление на главную, если не авторизован

with app.app_context():
    db.create_all()

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

    user = User.query.filter_by(login=username).first()

# Проверяем пользователя и пароль
    if user and user.check_password(password):
        login_user(user)  # Авторизуем пользователя
        flash("Вы успешно вошли!", "success")
        print('Успешно вошли!')
        return redirect(url_for("home"))  # Перенаправляем на главную
    else:
        print("Пароль неверен")
        flash("Неверный логин или пароль", "danger")
        return redirect(url_for("home"))  # Возвращаем на главную с ошибкой


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Проверяем, существует ли пользователь с таким именем или email
        existing_user = User.query.filter((User.login == username) | (User.email == email)).first()
        if existing_user:
            flash("Пользователь с таким именем или email уже существует", "danger")
            return redirect(url_for("register"))

        # Создаем нового пользователя
        new_user = User(login=username, email=email, password=password)


        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
        return redirect(url_for("home"))

    return render_template("pages/reg_form.html")


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

@app.route("/profile")
@login_required
def profile():
    return render_template("pages/profile.html")  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)