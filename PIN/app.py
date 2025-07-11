from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, UserRole, SubscriptionPlan, Lesson
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
app.config['SQLALCHEMY_BINDS'] = {
    'lessons': f'sqlite:///{os.path.join(app.instance_path, "lessons.db")}'  # БД для уроков
}
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

        if not self.access_token:
            self.get_access_token()

        prompt = """
        Создай 10 заданий для изучения китайского языка в строгом JSON-формате.
        Игра: появляется предложение с пропуском вместо одного слова, также дается 4 варианта ответов (4 слова только одно из которых подходит на место пропуска), пользователь должен выбрать правильный вариант
        Должны быть только предложения с пропуском, исключи вопросы, сделай ответы односложными
        Тщательно подбирай варианты ответов и хорошо тасуй их, обязательно должен быть 1 правильный ответ
        Вариантами ответов должны быть СЛОВА! НИКАКИХ ЦИФР и ЧИСЕЛ. Используй только китайский
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
                            "content": "Ты составитель тестов онлайн образовательной платформы для китайского языка"
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
    service = GigaChatService()
    result = service.generate_quest()
    print(jsonify(result))
    return jsonify(result)


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
        role = request.form.get("role", UserRole.USER.value)  # По умолчанию обычный пользователь
        subscription = request.form.get("subscription", SubscriptionPlan.NO_TARIFF.value)  # По умолчанию бесплатный

        # Проверяем, существует ли пользователь с таким именем или email
        existing_user = User.query.filter((User.login == username) | (User.email == email)).first()
        if existing_user:
            flash("Пользователь с таким именем или email уже существует", "danger")
            return redirect(url_for("register"))

        # Создаем нового пользователя
        new_user = User(
            login=username,
            email=email,
            password=password,
            role=role,
            subscription=subscription
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
        return redirect(url_for("home"))

    # Для GET-запроса передаем возможные роли и тарифы в шаблон
    return render_template("pages/reg_form.html",
                           roles=UserRole,
                           subscriptions=SubscriptionPlan)


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


@app.route('/chinese_course')
def chinese_course():
    return render_template('pages/china_course.html')


@app.route('/chinese_course_lessons', methods=["POST"])
def chinese_course_lessons():
    data = request.get_json()

    lesson_header = data.get("header")
    lesson_description = data.get("description")

    new_lesson = Lesson(title=lesson_header, description=lesson_description)
    db.session.add(new_lesson)
    db.session.commit()

    lessons = Lesson.query.all()
    lessons_list = [{"id": l.id, "title": l.title, "description": l.description} for l in lessons]
    return jsonify(lessons_list)


@app.route('/get_chinese_lessons', methods=["GET"])
def get_chinese_lessons():
    lessons = Lesson.query.all()
    lessons_list = [{"id": l.id, "title": l.title, "description": l.description} for l in lessons]
    return jsonify(lessons_list)

@app.route('/get_user_role' , methods=["GET"])
def get_user_role():
    if current_user.is_authenticated:
        return jsonify({"role" : current_user.role})
    return jsonify({"role":None})

@app.route('/set_tariff', methods=["GET"])
def set_tariff():
    data = request.get_json()
    current_user.subscription = data.tariff
    return jsonify({'tariff' : current_user.tariff})

@app.route('/delete_lesson', methods=["GET", "POST"])
def delete_lesson():
    data = request.get_json()
    lesson = Lesson.query.get(data["id"])
    if 'id' in data:
        lesson.title = ""
        lesson.description = ""
    db.session.commit()

    lessons = Lesson.query.all()
    lessons_list = [{"id": l.id, "title": l.title, "description": l.description} for l in lessons]

    return jsonify(lessons_list)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)