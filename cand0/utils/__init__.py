#file upload/download
from werkzeug import secure_filename
from flask import send_from_directory

import os



def test():
	upload_folder = '/cand0/cand0/files'
	admin.config['upload_folder'] = upload_folder
	return send_from_directory(directory = app.config['upload_folder'],filename = filename)
