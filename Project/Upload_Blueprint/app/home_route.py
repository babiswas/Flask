from . import blueprintutil
from flask import request
from flask import render_template
from flask import current_app
import os

@blueprintutil.app1.route("/home",methods=['GET'])
def home():
   return "<h1>Home</h1>"

@blueprintutil.app1.route("/upload",methods=["POST","GET"])
def upload():
   print(current_app.config['UPLOAD_FOLDER'])
   print(current_app.config['BUCKET_NAME'])
   current_app.config['UPLOAD_FOLDER']=os.path.dirname(__file__)+"/uploader"
   if request.method=='POST':
      uploaded_file=request.files['file']
      if uploaded_file.filename!='':
         filepath=os.path.join(current_app.config['UPLOAD_FOLDER'],uploaded_file.filename)
         uploaded_file.save(filepath)
   return render_template('index.html')





   

