from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from botocore.exceptions import ClientError
from requests import get,post
import boto3
import os


UPLOAD_FOLDER=os.path.dirname(__file__)+"/uploader"

app=Flask('__name__')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def create_url(bucket_name,object_name,fields=None,conditions=None,expiration=3600):
    try:
       s3_client=boto3.client('s3')
       response=s3_client.generate_presigned_post(bucket_name,object_name,Fields=fields,Conditions=conditions,ExpiresIn=expiration)
    except ClientError as e:
       logging.error(e)
       return None
    return response

def create_presigned_url(bucketname,object_name):
    s3_client=boto3.client('s3')
    params={'Bucket':bucketname,'Key':object_name}
    response=s3_client.generate_presigned_url('get_object',Params=params,ExpiresIn=3600*24*3)
    return response

    
@app.route('/upload',methods=['GET','POST'])
def upload_file():
   if request.method=='POST':
      uploaded_file=request.files['file']
      if uploaded_file.filename!='':
         filepath=os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename)
         response=create_url("bapan1888","src10/"+uploaded_file.filename)
         object_name="src10/"+uploaded_file.filename
         uploaded_file.save(filepath)
         with open(filepath,'rb') as file:
             files={'file':(object_name,file)}
             post(response['url'],data=response['fields'],files=files)
             response=create_presigned_url("bapan1888","src10/"+uploaded_file.filename)
             print(response)
   return render_template("index.html")

if __name__=="__main__":
   app.run(debug=True)
