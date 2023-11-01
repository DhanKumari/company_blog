from flask import Flask
import os
from flask_restful import Resource, Api
# from secure_check import authenticate , identity
# from flask_jwt import JWT,jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
Migrate(app,db)


#connecting the app with API
api=Api(app)
# jwt=JWT(app,authenticate,identity)

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}
    
class Puppy(db.Model):

    name=db.Column(db.String(80),primary_key=True)

    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name':self.name}






puppies=[]

class PuppyNames(Resource):
    def get(self,name):

        pup= Puppy.query.filter_by(name=name).first()
        if pup:
            return pup.json()
        else:
            return {'name':None},404


        # for pup in puppies:
        #     if pup['name']== name:
        #         return pup
        #return {'name':None},404

    def post(self,name):

        pup = Puppy(name=name)
        db.session.add(pup)
        db.session.commit()
        
        return pup.json()




        # pup={'name':name}
        # puppies.append(pup)
        # return pup
    
    def delete(self,name):

        pup= Puppy.query.filter_by(name=name).first()
        db.session.delete(pup)
        db.session.commit()
        return{'note':'delete success'}

        # for i,pup in enumerate(puppies):
        #     if pup['name']==name:
        #         deleted_pup =puppies.pop(i)
        #         print(deleted_pup)
        #         return{'note':'delete success'}
        #     else:
        #         return f"pupy not present "
            

class AllNames(Resource):

    # @jwt_required()
    def get(self):
        puppies = Puppy.query.all()
        return [pup.json() for pup in puppies]

        # return {'puppies':puppies}
    




#urls
api.add_resource(HelloWorld,'/')
api.add_resource(PuppyNames,'/puppy/<string:name>')
api.add_resource(AllNames,'/allpup')








if __name__ =='__main__':
    app.run(debug=True)

