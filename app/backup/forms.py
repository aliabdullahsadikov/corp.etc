from wtforms import StringField, BooleanField, PasswordField, SubmitField, validators, ValidationError, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


from app import models


class LoginForm(FlaskForm):
    username = StringField('Имя', [validators.DataRequired(), validators.Length(min=3, max=35)])
    password = PasswordField('Пароль', [validators.DataRequired(), validators.Length(min=6, max=200)])
    submit = SubmitField('Войти сейчас')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.DataRequired(), validators.Length(min=3, max=50)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Пароли должны совпадать'),
        validators.Length(min=3, max=20, message="Поле должно содержать от 3 до 20 символов.")
    ])
    confirm_password = PasswordField('Подтвердить Пароль')
    submit = SubmitField('Создать')

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Данное имя пользователя уже занято :(')

# images = UploadSet('images', IMAGES) # UploadSet class allow to use image extentions like jpg, png.


class UserInfoForm(FlaskForm):

    firstname = StringField(u'Имя', [validators.DataRequired()])
    lastname = StringField(u'Фамилия', [validators.DataRequired()])
    department = SelectField(u'Отдел', choices=models.Userinfo.department_list)
    position = StringField(u'Должность')
    photo = FileField(u'Фото', [ # validators.regexp(u'^[^/\\]\.jpg$'),
                                FileAllowed(['jpg', 'png'], message="Фото должно быть (.jpg .png .gif)  формате.") # we can use manual set image extentions without UploadSet class, like this ['jpg', 'png']
                                ])
    phone = StringField(u'Телефон номер', [validators.Length(min=9, max=12)])
    email = StringField(u'Емайл', [validators.Email()])
    facebook = StringField(u'Facebook')
    instagram = StringField(u'Instagram')
    telegram = StringField(u'Telegram')
    submit = SubmitField()


    # def validate_photo(form, field):
    #     if field.data:
    #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

