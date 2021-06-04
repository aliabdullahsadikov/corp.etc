from flask import request

from app import app


def upload_file(request):
    pass


def validate_file(file):
    if file.filename == '' or allowed_file(file.filename) == False:
        return False
    return True

#
# ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_IMAGE_EXTENSIONS"]
