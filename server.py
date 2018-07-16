from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from DB import DB
import json


app = Flask(__name__)
db = DB()

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Developer mode",
	"specs": [
        {
            "endpoint": '',
            "route": '/json',
    }]

}

swagger = Swagger(app)

test = {}

def read_json():
	global test
	
	folder = "swagger_data/"

	fd = {
			'update': 'update.json',
			'delete': 'delete.json',
			'add': 'add.json',
			'get_user': 'get_user.json',
			'users': 'users.json',
			'default': 'default.json',
		}
#	fd = {'update': 'update.json'}

	for k, f in fd.items():
		with open(folder+f) as fp:
			test[k] = json.loads(fp.read())

read_json()

@app.route('/')
@swag_from(test['default'])
def index():
	"""
	Will acknowledge whether the application is running properly or not

    """
	
	return jsonify("YUP, Working")


@app.route('/users')
@swag_from(test['users'])
def get_users():
	"""
	Return all users stored in the database
	
	"""

	return jsonify(db.get_users())


@app.route('/user/<int:user_id>', methods = ['GET'])
@swag_from(test['get_user'], validation=False)
def get_user_by_id(user_id):
	"""
	Return user by id.

	"""
	try:
		user_id = int(user_id)
	except Exception as e:
		return "Please enter id in a integet form."

	data = db.get_users()

	if user_id in data.keys():
		return jsonify({user_id:data[user_id]})

	return jsonify({})
	

@app.route('/user/add', methods = ['POST'])
@swag_from(test['add'], validation=True)
def add_user():
	"""
	Add user to the database, Accepts a json object and save to database
	
	"""
	content = request.get_json()
	if not isinstance(content, dict):
		return "Wrong input, please send json"

	f, msg = db.add_user(content)
	if not f:
		return msg
	
	return get_user_by_id(msg)
			
@app.route('/user/update/<string:username>', methods = ['PUT'])
@swag_from(test['update'], validation=True)
def update_user(username):
	"""
	Update existing user, Accept username and new data to update in the form of json

	"""
	content = request.get_json()
	if not isinstance(content, dict):
		return "Wrong input, please send json"
	
	return jsonify(db.update_user(username, content)[1])


@app.route('/user/delete/<string:username>', methods = ['DELETE'])
@swag_from(test['delete'], validation=False)
def delete_user(username):
	"""
	Delete existing user from database

	"""
	return jsonify(db.delete_user(username)[1])

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
