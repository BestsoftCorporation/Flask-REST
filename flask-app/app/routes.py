# routes.py

from flask import render_template
from app import app 
from app.models import Users
from flask_principal import Principal, Permission, RoleNeed
from marshmallow import Schema,fields


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

class userschema(Schema):
    id=fields.Integer()
    name=fields.String()
    last_name=fields.String()
    email=fields.String()
    username=fields.String()
    password=fields.String()
    acc_type=fields.Integer()

@app.route('/login', methods=['GET', 'POST'])
def login():
    identity_changed.send(current_app._get_current_object(),
                            identity=Identity(user.id))

    return redirect(request.args.get('next') or '/')

@admin_permission.require()
@app.route('/users',methods=['GET'])
def get_all_users():
    users=user.get_all()

    serializer=userschema(many=True)

    data=serializer.dump(users)

    return jsonify(
        data
    )


@app.route('/users',methods=['POST'])
def create_a_user():
    data=request.get_json()

    new_user=users(
        name=data.get('name')
    )

    new_user.save()

    serializer=userschema()

    data=serializer.dump(new_user)

    return jsonify(
        data
    ),201


@app.route('/user/<int:id>',methods=['GET'])
def get_user(id):
    user=user.get_by_id(id)

    serializer=userschema()

    data=serializer.dump(user)

    return jsonify(
        data
    ),200


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