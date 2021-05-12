import os
import random
import string

from flask import render_template, request, redirect, url_for, current_app, flash, abort
from datetime import datetime
from flask_admin.helpers import is_safe_url
from flask_login import login_user, logout_user, current_user, login_required
# from flask_user import login_required
from flask_bcrypt import Bcrypt
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from sqlalchemy.sql import text

from app import app
from app.models import News, Notification, Doc, User, Userinfo, db, Comment
from app.forms import LoginForm, RegistrationForm, UserInfoForm
import json, array


# login_manager.setup_app(current_app)



bcrypt = Bcrypt(app)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if  current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            # Invalid parameters: Login or Password is incorrect
            flash("Логин или пароль введены неверно")
            return redirect(url_for('login'))
        # allow to user login
        login_user(user)
        # get next url
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


# for exceptions
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    userInfo = Userinfo.query.filter_by(user_id=current_user.id).first()
    form = UserInfoForm()

    if form.validate_on_submit():
        # handle selected file
        file = form.photo.data

        # if Userinfo new
        if not userInfo:
            data = {
                'user_id': current_user.id,
                'firstname': form.firstname.data,
                'lastname': form.lastname.data,
                'department': form.department.data,
                'position': form.position.data,
                'phone': form.phone.data,
                'email': form.email.data,
                'facebook': form.facebook.data,
                'instagram': form.instagram.data,
                'telegram': form.telegram.data,
                # 'photo': ''
            }

            # if file don't selected
            if not file:
                data['photo'] = Userinfo.DEFAULT_IMAGE
                flash('Вы не выбрали фото для профиля')

            # has file
            elif file and allowed_file(file.filename):
                hashed_filename = secure_filename(file.filename)
                if file.save(os.path.join(app.config['UPLOAD_FOLDER'], hashed_filename)):
                    data['photo'] = hashed_filename

            # if someone else
            else:
                data['photo'] = Userinfo.DEFAULT_IMAGE
                flash('Фотография не была сохранена по какой-то причине')

            # save
            newInfo = Userinfo(**data)
            db.session.add(newInfo)
            db.session.commit()
            newInfo.append_employees()
            flash('Ваша информация сохранена')
            return redirect('/profile')

        # if userInfo exist
        else:
            if not file:
                photo_name = Userinfo.DEFAULT_IMAGE
                flash('Вы не выбрали фото для профиля')

            elif file and allowed_file(file.filename):
                letters = string.ascii_lowercase
                random_str = ''.join(random.choice(letters) for i in range(10))
                hashed_filename = (random_str + file.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                file.save(os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'], hashed_filename))
                photo_name = hashed_filename
                # print(hashed_filename)

            else:
                photo_name = Userinfo.DEFAULT_IMAGE
                flash('Фотография не была сохранена по какой-то причине')

            # update Userinfo model
            userInfo.firstname = form.firstname.data
            userInfo.lastname = form.lastname.data
            userInfo.department = form.department.data
            userInfo.position = form.position.data
            userInfo.phone = form.phone.data,
            userInfo.email = form.email.data
            userInfo.facebook = form.facebook.data
            userInfo.instagram = form.instagram.data
            userInfo.telegram = form.telegram.data
            userInfo.photo = str(photo_name)
            db.session.commit()
            userInfo.append_employees()
            flash('Ваша информация обновлена')

            return redirect('/profile')
    # else:
    #     print(form)

    if userInfo:
        form.firstname.data = userInfo.firstname
        form.lastname.data = userInfo.lastname
        form.department.data = userInfo.department
        form.position.data = userInfo.position
        form.phone.data = userInfo.phone
        form.email.data = userInfo.email
        form.facebook.data = userInfo.facebook
        form.instagram.data = userInfo.instagram
        form.telegram.data = userInfo.telegram
        form.photo.data = userInfo.photo or Userinfo.DEFAULT_IMAGE

    # image = base64.b64encode(file_data.DATA).decode('ascii')
    return render_template('profile.html', form=form, userInfo=userInfo)


# def append_employees():
#     userinfo = Userinfo.query.all()
#     data = {}
#     data['users'] = []
#     for name in userinfo:
#         data['users'].append({
#             'id': name.id,
#             'firstname': name.firstname,
#             'lastname': name.lastname,
#             'department': name.department,
#             'position': name.position,
#             'phone': name.phone,
#             'email': name.email,
#             'photo': name.photo,
#             'facebook': name.facebook,
#             'instagram': name.instagram,
#             'telegram': name.telegram
#         })
#     with open(os.path.join(os.path.dirname(__file__), "static/js/", "employees.json"), "w") as outfile:
#         json.dump(data, outfile)



@app.route('/update-profile', methods=['POST', 'GET'])
@login_required
def update_profile():
    form = UserInfoForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        pass


@app.route('/')
@app.route('/index')
def index():
    news = News.query.order_by(News.id.desc()).all()
    notifies = Notification.query.order_by(Notification.id.desc()).all()
    docs = Doc.query.filter_by(isActive=True).all()

    return render_template('index.html', user=current_user, news=news, documents=docs, notifies=notifies, datetime=datetime.utcnow())


@app.route('/comment', methods=['POST'])
def comment():
    if request.method == 'POST':
        post = request.form.to_dict()
        data = {
            "user_id": current_user.__getattr__("id"),
            "news_id": post["news_id"],
            "parent_id": post["parent_id"],
            "message": post['message'],
            "created_at": datetime.utcnow()
        }
        comment = Comment(**data)
        db.session.add(comment)
        db.session.commit()


    #
    # print(post)
    # print(data)
    return post



@app.route('/news/<id>')
# @login_required
def news_details(id):
    news_details = News.query.filter_by(id=id).first()
    similar_posts = News.query.filter(News.id!=id).order_by(News.id.desc()).all()
    return render_template('news_details.html', news_details=news_details, similar_posts=similar_posts)


@app.route('/doc/<id>')
def doc_details(id):
    doc_model = Doc.query.filter_by(id=id).first()
    return render_template('doc_details.html', doc=doc_model)


@app.route('/docs/')
def docs():
    docs = Doc.query.filter_by(isActive=True).all()
    return render_template('docs.html', docs=docs)


@app.route('/users/')
@login_required
def users():
    userInfo = Userinfo.query.filter_by(user_id=current_user.id).first()
    form = UserInfoForm()
    return render_template('users.html', userInfo=userInfo, form=form)


# @app.route('/append-employee')
# def append_employee():
    # Get searching employee
    # userInfo = Userinfo.query.all()
    # data = {}
    # data['users'] = []
    # for name in userInfo:
    #     data['users'].append({
    #         'firstname': name.firstname,
    #         'lastname': name.lastname,
    #         'department': name.department,
    #         'phone': name.phone,
    #         'email': name.email,
    #         'photo': name.photo
    #     })
    # with open(os.path.join(os.path.dirname(__file__), "static/js/", "employees.json"), "w") as outfile:
    #     json.dump(data, outfile)
    #
    # type(outfile)
    # return redirect('/users')


# @app.route('/search-employee', methods=['GET'])
# def search_employee():
#     # Get searching employee
#     fio = request.args.get('fio')
#     # sql = text("SELECT * FROM userinfo WHERE firstname LIKE '%fio%'")
#     # userInfo = db.engine.execute(sql)
#     like = "%{}%".format(fio)
#     with open('app/employees.json', 'r') as file:
#         text = file.read()
#         jsonData = json.loads(text)
#         for user in jsonData['users']:
#             # print(type(user))
#             firstname = user['firstname']
#             lastname = user['lastname']
#             if  fio in firstname.lower():
#                 print(user)
#     # userInfo = Userinfo.query.filter(Userinfo.firstname.like(like)).array().all()
#     # print(userInfo)
#     # i = json.dumps(userInfo)
#     return ''
#


