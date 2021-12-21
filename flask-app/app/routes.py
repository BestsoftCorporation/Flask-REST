from flask import render_template,jsonify,request,make_response
from app import app 
from app.models import Users, arrangement
from flask_principal import Identity,identity_changed,identity_loaded,Principal, Permission, RoleNeed
from marshmallow import Schema,fields
import jwt
from werkzeug.security import safe_str_cmp,generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta



# load the extension
principals = Principal(app)
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
tourist_permission = Permission(RoleNeed('tourist'))
tavel_guide_permission = Permission(RoleNeed('travelguide'))


class userschema(Schema):
    id=fields.Integer()
    name=fields.String()
    last_name=fields.String()
    email=fields.String()
    username=fields.String()
    password=fields.String()
    acc_type=fields.Integer()

class arrangementschema(Schema):
    id_arrangement=fields.Integer()
    start_date= fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    end_date= fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    description=fields.String()
    destination=fields.String()
    capacity=fields.Integer()
    price=fields.Integer()


username_table = {u.username: u for u in Users.query.all()}
userid_table = {u.id: u for u in Users.query.all()}



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.get_json()

  
    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = Users.query\
        .filter_by(username = auth.get('username'))\
        .first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'id': str(user.id),
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, 'super-secret')
  
        return make_response(jsonify({'token' : token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
  

@token_required
@app.route('/users',methods=['GET'])
@admin_permission.require()
def get_all_users():
    users=Users.get_all()

    serializer=userschema(many=True)

    data=serializer.dump(users)

    return jsonify(
        data
    )


@app.route('/signup',methods=['POST'])
def create_a_user():
    data=request.get_json()

    new_user=Users(
        name=data.get('name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        username=data.get('username'),
        password=generate_password_hash(data.get('password')),
        acc_type=2
    )

    new_user.save()

    serializer=userschema()

    data=serializer.dump(new_user)

    return jsonify(
        data
    ),201

@token_required
@app.route('/arrangement',methods=['POST'])
def create_arrangement():
    data=request.get_json()

    new_arrangement=arrangement(
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        price=data.get('price'),
        capacity=data.get('capacity'),
        description=data.get('description')
    )

    new_arrangement.save()

    serializer=arrangementschema()

    data=serializer.dump(new_arrangement)

    return jsonify(
        data
    ),201

@token_required
@app.route('/user/<int:id>',methods=['GET'])
def get_user(id):
    user=user.get_by_id(id)

    serializer=userschema()

    data=serializer.dump(user)

    return jsonify(
        data
    ),200

@token_required
@admin_permission.require()
@app.route('/user/<int:id>',methods=['PUT'])
def update_user(id):
    user_to_update=user.get_by_id(id)

    data=request.get_json()

    user_to_update.name=data.get('name')
    user_to_update.description=data.get('description')

    db.session.commit()

    serializer=userschema()

    user_data=serializer.dump(user_to_update)

    return jsonify(user_data),200

@token_required
@admin_permission.require()
@app.route('/user/<int:id>',methods=['DELETE'])
def delete_user(id):
    user_to_delete=user.get_by_id(id)

    user_to_delete.delete()

    return jsonify({"message":"Deleted"}),204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}),500