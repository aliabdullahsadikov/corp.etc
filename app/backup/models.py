import os
import os.path as op
import json, array

from flask import url_for, redirect, request
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, current_user
from sqlalchemy.event import listens_for
from jinja2 import Markup
from flask_admin.contrib import sqla
from wtforms import SelectField
from flask_user import UserManager, SQLAlchemyAdapter
from flask_sqlalchemy import SQLAlchemy



from app import config
from app import app, login_manager

# For database initialization
db = SQLAlchemy(app)

# For migration
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create directory for file fields to use
# path for doc files
image_path = op.join(op.dirname(__file__), 'static/images/docs/')
file_path = op.join(op.dirname(__file__), 'static/files/docs/')

# path for news images
news_image_path = op.join(op.dirname(__file__), 'static/images/news/')

try:
    os.mkdir(image_path)
    os.mkdir(file_path)
    os.mkdir(news_image_path)
except OSError:
    pass


# MyModelView class
class MyModelView(ModelView):
    # checking user is authenticated
    def is_accessible(self):
        return ((current_user.is_authenticated) and (current_user.id == 7 or current_user.id == 10))

    # redirection
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


# MODELS
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    info = db.relationship("Userinfo", uselist=False, back_populates="user")

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.password}', '{self.active}', '{self.info}')"


class Userinfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="info")

    firstname = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)
    department = db.Column(db.String(80), nullable=True)
    position = db.Column(db.String(80), nullable=True)
    photo = db.Column(db.String(100), default='user_default.png', nullable=False)
    phone = db.Column(db.String(9), nullable=True)
    phone_verification = db.Column(db.Boolean(), server_default='0')
    email = db.Column(db.String(120), nullable=True)
    email_verification = db.Column(db.Boolean(), server_default='0')
    facebook = db.Column(db.String(80), nullable=True)
    instagram = db.Column(db.String(80), nullable=True)
    telegram = db.Column(db.String(80), nullable=True)

    DEFAULT_IMAGE = 'user_default.png'

    def __repr__(self):
        return f"User('{self.user_id}', '{self.firstname}', '{self.lastname}', '{self.department}', '{self.position}', '{self.photo}', '{self.phone}', '{self.email}')"

    department_list = ['Отдел корпоративного планирования', 'Бухгалтерия', 'Отдел контрактов', 'Склад',
                       'Отдел по маркетингу',
                       'Отдел по маркетинговому анализу и стратегии (Intelligence)', 'Отдел по персоналу',
                       'Юридический отдел', 'Отдел по общим вопросам', 'Группа планирования проектов',
                       'Группа поддержки собственной сети',
                       'Отдел по информационной безопасности и поддержкe собственной сети',
                       'Отдел биллинга', 'Отдел Информационно- коммуникационных технологий',
                       'Группа рыночных продаж', 'Группа планирования ИКТ', 'Контакт-центр',
                       'Отдел Дата-центра', 'Отдел бизнес платформ', 'Отдел планирования сети',
                       'Отдел строительство сети',
                       'Отдел управление сетями', 'Отдел управления беспроводными сетями LTE',
                       'Отдел эксплуатации сети', 'Региональный отдел эксплуатации сети',
                       'Абонентский отдел', 'Отдел по  продажам', 'Call - центр', 'Региональный отдел']

    def append_employees(self):
        userinfo = Userinfo.query.all()
        data = {}
        data['users'] = []
        for name in userinfo:
            data['users'].append({
                'id': name.id,
                'firstname': name.firstname,
                'lastname': name.lastname,
                'department': name.department,
                'position': name.position,
                'phone': name.phone,
                'email': name.email,
                'photo': name.photo,
                'facebook': name.facebook,
                'instagram': name.instagram,
                'telegram': name.telegram
            })
        with open(os.path.join(os.path.dirname(__file__), "static/js/", "employees.json"), "w") as outfile:
            json.dump(data, outfile)

    # def get_department(self):
    #     return self.__department_list

# db_adapter = SQLAlchemyAdapter(db, User)
# user_manager = UserManager(db_adapter, app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # company = db.Column(db.String(100), nullable=False, default="ETC|TPS|EVO")
    image = db.Column(db.String(100), default='default-news.jpg', nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='news', lazy=True)

    def __repr__(self):
        return f"News('{self.title}', '{self.slug}', '{self.desc}', '{self.image}', '{self.created_at}')"


class NewsView(MyModelView):
    # form_choices = {
    #     'image': [
    #         ('TPS', 'Tps'),
    #         ('ETC', 'Etc'),
    #         ('EVO', 'Evo'),
    #         ('ALL', 'All')
    #     ]
    # }


    # def __init__(self):
    #     super(NewsView, self).__init__(News, db.session)

    # for image column
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup('<img src="%s" style="width:100px;">' % url_for('static', filename="/images/news/" + model.image))
        # return Markup('<img src="%s">' % url_for('static', filename=form.thumbgen_filename(model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    # form_extra_fields - for the add column to form
    form_extra_fields = {
        'image': form.ImageUploadField('Image', base_path=news_image_path)
    }

    # end

    # for file column
    form_overrides = {
        'file': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    # form_args = {
    #     'file': {
    #         'label': 'image',
    #         'base_path': file_path,
    #         'allow_overwrite': False
    #     }
    # }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.user_id}', '{self.news_id}', '{self.message}', '{self.created_at}')"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # company = db.Column(db.String(100), nullable=False, default="ETC|TPS|EVO")
    image = db.Column(db.String(100), default='default-notifi.jpg', nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Notification('{self.title}', '{self.slug}','{self.desc}', '{self.content}', '{self.image}', '{self.created_at}')"


class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    file = db.Column(db.String(100), nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Docs('{self.title}', '{self.slug}', '{self.content}', '{self.image}', '{self.created_at}', '{self.isActive}')"


class DocView(MyModelView):

    # for image column
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup('<img src="%s" style="width:100px;">' % url_for('static', filename="/images/docs/" +model.image))
        # return Markup('<img src="%s">' % url_for('static', filename=form.thumbgen_filename(model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    # form_extra_fields - for the add column to form
    form_extra_fields = {
        'image': form.ImageUploadField('Image', base_path=image_path),
        'file': form.FileUploadField('File', base_path=file_path)
    }

    # end

    # for file column
    form_overrides = {
        'file': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'file': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }


# ADMIN PANEL
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Userinfo, db.session))
admin.add_view(NewsView(News, db.session))
admin.add_view(MyModelView(Notification, db.session))
admin.add_view(DocView(Doc, db.session))


# db.create_all()
# manager.run()