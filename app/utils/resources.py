from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from utils.mqtt_calls import get_result, post_msg
import jwt
import uuid
from datetime import datetime, timedelta
from main import db, api
from utils.models import Auths, token_required
from config import logger, variables


reg_open = variables.REG_OPEN

if reg_open:
    logger.warning("Registrations are open")
    @api.route('/register', methods=['POST'])
    def signup_user():
        data = request.get_json()
        user = Auths.query.filter_by(name=data['name']).first()
        username = user.name if user else ""
        if username.lower() == data['name'].lower():
            return jsonify({'message': 'User already exists'})
        else:
            hashed_password = generate_password_hash(data['password'], method='scrypt')
            new_user = Auths(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"{data['name']} has been registered")
            return jsonify({'message': f"{data['name']} registered successfully"})


    @api.route('/change', methods=['POST'])
    def change_pwd():
        data = request.get_json()
        user = Auths.query.filter_by(name=data['name']).first()
        if user.name:
            hashed_password = generate_password_hash(data['password'], method='scrypt')
            user_id = Auths.query.filter_by(name=data['name']).first()
            user_id.password = hashed_password
            db.session.commit()
            logger.info(f"{user_id.name} password has been changed")
            return jsonify({'message': f"{user_id.name} password has been changed" })
        else:
            return jsonify({'message': 'User does not exist'})


@api.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        logger.error(f"{auth.username} provided wrong password")
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Auths.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        expiry = datetime.now() + timedelta(minutes=30)
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': expiry},
            variables.SECRET_KEY)
        logger.info(f"{auth.username} has been granted a token")
        return jsonify({'token': token, 'expiry': expiry.strftime("%d/%m/%YT%H:%M:%S")})
    logger.error(f"{auth.username} attempted a token request")
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@api.route('/test', methods=['Get'])
@token_required
def test(self):
    ip = request.headers['X-Real-IP'] or 'No IP'
    logger.info(f"{ip} used the test api")
    return jsonify({'message': 'test succeeded'})


@api.route('/sub', methods=['Get'])
@token_required
def get(self):
    content = request.json
    topic = content['mqtt-topic']
    # topic = request.headers['mqtt-topic']
    ip = request.headers['X-Real-IP'] or 'No IP'
    logger.info(f"{ip} requested data from {topic}")
    if topic != "":
        msg = get_result(topic)
        topic = ""
        return jsonify({"result": msg})
    else:
        topic = ""
        return jsonify({"result": "no data"})


@api.route('/pub', methods=['Post'])
@token_required
def post(self):
    content = request.json
    topic = content['mqtt-topic']
    mssg = str(content['mqtt-msg']).replace("'",'"')
    flag = content.get('mqtt-retain', "")
    rtn = True if flag.lower() in ("yes", "true", "t", "1") else False
    # print(rtn)
    ip = request.headers['X-Real-IP'] or 'No IP'
    stat = post_msg(topic, mssg, rtn)
    logger.info(f"{ip} posted {mssg} to {topic} with retain set as {rtn}")
    return jsonify({"result": stat})
