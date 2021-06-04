from app import app
from werkzeug.utils import secure_filename

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u0721127_flask_corp_user:131313ali@localhost:3306/u0721127_flask_corp_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/corp_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corp.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:131313ali@localhost:5432/corp-pg.db'
# SQLALCHEMY_BINDS = {
#     'users':        'mysqldb://localhost/users',
#     'docs':      'sqlite:///corp.db'
# }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'dskflkfaiiethahuveikrlafnsdvoijktk'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False
app.config['FLASK_APP'] = 'run.py'
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


# config for upload file for users
UPLOAD_FOLDER = './static/images/profile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POST_UPLOAD_FOLDER'] = './static/images/post'

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ['jpg', 'png', 'jpeg', 'gif']
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

