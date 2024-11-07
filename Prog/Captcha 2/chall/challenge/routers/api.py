from flask import Blueprint, jsonify, request, session
from time import time
from utils import captcha
from conf import DURATION, TO_SOLVE

router = Blueprint("api", __name__)

@router.route("/captcha")
def generate_captcha():
    passphrase, image = captcha.generate()
    session['captcha'] = passphrase
    session['exp'] = time() + DURATION
    return image

@router.post("/captcha")
def verify_captcha():
    if 'captcha' not in session:
        return jsonify({'message': 'Vous n\'avez pas de captcha en attente', 'error': 0}), 401
    if session['exp'] < time():
        return jsonify({'message': 'Le captcha a expiré', 'error': 1}), 410
    if request.json['code'] != session['captcha']:
        return jsonify({'message': 'Code invalide', 'error': 2}), 400
    
    solved = session.get('solved') or []
    solved_at = time()
    solved = [*solved, solved_at]
    solved = [t for t in solved if solved_at - t < DURATION]
    if len(solved) == TO_SOLVE:
        session['flag'] = True
    session['solved'] = solved
    return jsonify({'message': 'Captcha validé', 'flag': session['flag']}), 200
