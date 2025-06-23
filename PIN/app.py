from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import requests
import uuid
import json
import os

# Загрузка модели

app = Flask(__name__)


class Config:
    GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY",
                                 "NTBlNDkzNTktMjRkNC00Mjk1LThmMzAtMDQ0Nzk2ZDYwNDdhOmJmOGY4NjBhLWExMDItNDEyNy1iYWMwLTkyMTMxZjhiNjAwNw==")
    GIGACHAT_BASE_URL = "https://gigachat.devices.sberbank.ru/api/v1"
    AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


app.config.from_object(Config)

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


class GigaChatService:
    def __init__(self):
        self.access_token = None

    def get_access_token(self):
        """Получение токена доступа"""
        try:
            headers = {
                "Authorization": f"Basic {app.config['GIGACHAT_API_KEY']}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "RqUID": str(uuid.uuid4())
            }
            response = requests.post(
                app.config['AUTH_URL'],
                headers=headers,
                data={"scope": "GIGACHAT_API_PERS"},
                verify=False
            )
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
        except Exception as e:
            raise Exception(f"Ошибка аутентификации: {str(e)}")

    def generate_quest(self):
        """Генерация тура через GigaChat API"""
        if not self.access_token:
            self.get_access_token()

        prompt = """
        Создай 30 заданий для изучения китайского языка в строгом JSON-формате.
    Структура каждого задания:
    {
        "sentence": "предложение с пропуском ___",
        "options": ["вариант1", "вариант2", "вариант3", "вариант4"],
        "correct_answer": "правильный вариант"
    }

    Верни ТОЛЬКО валидный JSON-массив с заданиями в следующем формате:
    {
        "exercises": [
            { ... },  // первое задание
            { ... },  // второе задание
            { ... }   // третье задание
        ]


    Не добавляй никаких пояснений, комментариев или дополнительного текста.
    Начни ответ строго с { и закончи }.
        """

        try:
            response = requests.post(
                f"{app.config['GIGACHAT_BASE_URL']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "GigaChat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Ты разработчик онлайн образовательной платформы для китайского языка"
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "response_format": {"type": "json_object"}
                },
                verify=False
            )
            response.raise_for_status()

            # Получаем чистый JSON из ответа
            quest_result = response.json()["choices"][0]["message"]["content"]
            return json.loads(quest_result)

        except Exception as e:
            raise Exception(f"Ошибка API: {str(e)}")


@app.route('/btn')
def btn():
    return render_template('pages/btn.html')


@app.route('/api/generate-quest', methods=['POST'])
def api_generate_quest():
    # Генерация тура
    service = GigaChatService()
    result = service.generate_quest()
    print(jsonify(result))
    return jsonify(result)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")  # Получаем логин из формы
    password = request.form.get("password")  # Получаем пароль из формы

    user = User.query.filter_by(username=username).first()

    # Проверяем пользователя и пароль
    if user and user.check_password(password):
        login_user(user)  # Авторизуем пользователя
        flash("Вы успешно вошли!", "success")
        return redirect(url_for("home"))  # Перенаправляем на главную
    else:
        print("Пароль неверен")
        flash("Неверный логин или пароль", "danger")
        return redirect(url_for("home"))  # Возвращаем на главную с ошибкой


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Проверяем, существует ли уже пользователь с таким именем
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует", "danger")
            return redirect(url_for("register"))

        # Проверяем совпадение паролей
        if password != confirm_password:
            flash("Пароли не совпадают", "danger")
            return redirect(url_for("register"))

        # Создаем нового пользователя
        new_user = User(username=username)
        new_user.set_password(password)  # Хешируем пароль
        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
        return redirect(url_for("home"))

    return render_template("pages/register.html")


@app.route("/learning")
def learning():
    return render_template("pages/learning_page.html")


@app.route('/team')
def inteam():
    return render_template('pages/team.html')


@app.route('/contacts')
def contacts():
    return render_template('pages/contacts.html')


@app.route('/test/grammar')
def test():
    return render_template('pages/cards_game.html')

@app.route('/profile')
def profile():
    return render_template('pages/profile.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)