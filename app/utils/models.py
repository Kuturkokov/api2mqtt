from main import api, db
from config import logger, variables
from flask import request, jsonify
from functools import wraps
import jwt


class Auths(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.name)

with api.app_context():
    db.create_all()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, variables.SECRET_KEY, algorithms=['HS256'])
            current_user = Auths.query.filter_by(public_id=data['public_id']).first()
        except Exception as e:
            logger.error(str(e))
            return jsonify({'message': 'Auth error'})

        return f(current_user, *args, **kwargs)

    return decorator
