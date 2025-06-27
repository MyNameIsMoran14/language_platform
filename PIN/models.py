from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import Enum

db = SQLAlchemy()


class UserRole(Enum):
    USER = 'user'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class SubscriptionPlan(Enum):
    NO_TARIFF = 'Без тарифа'
    FREE = 'Базовый'
    BASIC = 'Продвинутый'
    PREMIUM = 'Премиум'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.USER.value)
    subscription = db.Column(db.String(20), nullable=False, default=SubscriptionPlan.FREE.value)

    # Дополнительные поля для учителей
    teacher_qualification = db.Column(db.String(100), nullable=True)
    teacher_description = db.Column(db.Text, nullable=True)

    # Новые поля для прогресса и статистики
    progress = db.Column(db.Integer, default=0)  # Прогресс в процентах (0-100)
    tasks_completed = db.Column(db.Integer, default=0)  # Количество выполненных заданий
    points = db.Column(db.Integer, default=0)  # Очки/баллы пользователя

    def check_password(self, password):
        return self.password == password

    def is_admin(self):
        return self.role == UserRole.ADMIN.value

    def is_teacher(self):
        return self.role == UserRole.TEACHER.value

    def has_no_tariff(self):
        return self.subscription == SubscriptionPlan.NO_TARIFF.value

    def has_premium(self):
        return self.subscription == SubscriptionPlan.PREMIUM.value

    def has_basic(self):
        return self.subscription == SubscriptionPlan.BASIC.value