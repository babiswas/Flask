from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
import boto3
import os

UPLOAD_FOLDER=os.path.dirname(__file__)+"/uploader"

def upload_to_s3(filepath,filename):
    s3=boto3.client('s3')
    return s3.upload_file(filepath,"bapan1888","src10/"+filename)

app=Flask('__name__')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


@app.route('/upload',methods=['GET','POST'])
def upload_file():
   if request.method=='POST':
      uploaded_file=request.files['file']
      if uploaded_file.filename!='':
         filepath=os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename)
         uploaded_file.save(filepath)
         upload_to_s3(filepath,uploaded_file.filename)
         os.remove(filepath)
   return render_template('index.html')

if __name__=="__main__":
   app.run(debug=True)
