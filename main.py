from flask import Flask
from flask_restful import Resource,Api
from flask import jsonify

app=Flask(__name__)
api=Api(app)

class HelloWorld(Resource):
   def get(self):
       return jsonify({"user1":"users"})
   def post(self):
       return jsonify({"user2":"users"})

class Hello(Resource):
   def get(self,name):
       return jsonify({"data":name})

api.add_resource(HelloWorld,"/hello")
api.add_resource(Hello,"/hello1/<string:name>")

if __name__=="__main__":
  app.run(debug=True)