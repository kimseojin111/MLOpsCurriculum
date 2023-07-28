from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from decouple import config 


app = Flask(__name__) 

# Health Check 
@app.route("/", methods=['GET']) 
def health_check():
    return jsonify({'status': 'OK'}), 200 


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config("DB_USERNAME")}:{config("DB_PASSWORD")}@localhost/mlops_user_db'
db = SQLAlchemy(app) 
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), unique=True)  
    age = db.Column(db.Integer, nullable=True)  
    
    def __repr__(self): 
        return f'<User name {self.name}>' 
    
    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'age': self.age, 
        }


# Get All Users 
@app.route("/users", methods=['GET']) 
def get_all_users():
    users = User.query.all() 
    all_user_dict = [user.to_dict() for user in users] 
    return all_user_dict, 200 

@app.route("/users/<id>", methods=['GET']) 
def get_user(id): 
    if not id.isdigit(): 
        return "Invalid user id.", 400 
    user = User.query.get(int(id))  
    if user is None: 
        return "The user is not found.", 404 
    return  user.to_dict(), 200 


@app.route("/users", methods=['POST']) 
def create_user(): 
    if not request.json or 'name' not in request.json: 
        return """“name” parameter is empty.""", 400 
    user_age = request.json.get('age')
    user_name = request.json.get('name') 
    existing_user = User.query.filter_by(name=user_name).first()

    if user_age != None and type(user_age)!=int: 
        return """“age” must be an integer.""", 400 
    if existing_user != None: 
        return "The user already exists.", 409 
    user = User(name=user_name, age=user_age) 
    db.session.add(user) 
    db.session.commit() 
    return user.to_dict(), 201 

@app.route("/users/<id>", methods=['PUT']) 
def update_user(id):
    if not id.isdigit():
        return "Invalid user id.", 400 

    user = User.query.get(int(id)) 
    
    if user is None: 
        return "The user is not found.", 404 
    
    if 'age' in request.json: 
        age = request.json['age'] 
        if type(age)!=int: 
            return """"age" must be an integer""", 400  
        user.age = age 
    
    if 'name' in request.json:
        name = request.json['name'] 
        if type(name)!=str: 
            return """"name" must be an str""", 400 
        if_exist_user = User.query.filter_by(name=name).first()  
        if if_exist_user is not None: 
            return "The user alreay exists", 409 
        user.name = name 
    
    db.session.commit() 
    
    return user.to_dict(), 200 

@app.route("/users/<id>", methods=['DELETE']) 
def delete_user(id):
    if not id.isdigit():
        return "Invalid user id.", 400 
    user = User.query.get(int(id)) 
    if user is None: 
        return "The user is not found.", 404 
    db.session.delete(user) 
    db.session.commit() 
    return user.to_dict(), 200 


if __name__ == "__main__": 
    app.run(debug=True)

