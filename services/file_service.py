import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED = {"png","jpg","jpeg","gif","mp4","mov","pdf","svg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED

def save_local(file_storage, subfolder=""):
    folder = current_app.config["UPLOAD_FOLDER"]
    if subfolder:
        folder = os.path.join(folder, subfolder)
    os.makedirs(folder, exist_ok=True)
    filename = secure_filename(file_storage.filename)
    path = os.path.join(folder, filename)
    file_storage.save(path)
    # return path relative to app root
    return path