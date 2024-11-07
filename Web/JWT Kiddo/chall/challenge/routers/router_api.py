from flask import Blueprint, jsonify, request, g
from datetime import datetime
from models import Comment
from uuid import uuid4
import string
import os

api = Blueprint("api", __name__)

comments = [
	Comment(
		'TotalusRetardus',
		datetime.now().timestamp() - 870,
		'3',
		'db2fd7ac-4e40-42f6-9172-b02104eb868d'
	),
	Comment(
		'LennyBarre',
		datetime.now().timestamp() - 765,
		'5',
		'3db19ccd-7c7a-4cf8-929e-ebaad7b3bf9a'
	),
	Comment(
		'PermaBagarre',
		datetime.now().timestamp() - 700,
		'6',
		'7dd2fb9b-24bd-444a-8d3b-4c4f778aab05'
	),
	Comment(
		'LennyBarre', 
		datetime.now().timestamp() - 650,
		'5',
		'5990636c-48be-493d-ac16-88fd14efbc73'
	),
	Comment(
		'TotalusRetardus',
		datetime.now().timestamp() - 400,
		'3',
		'690b53c4-28e6-4725-9bbe-e45ed302111d'
	),
	Comment(
		'LennyBarre', 
		datetime.now().timestamp() - 350,
		'5',
		'cd21f0e7-4acc-40a0-b018-a14f64728463'
	),
	Comment(
		'GrossoBelloBito',
		datetime.now().timestamp() - 200,
		'4',
		'1f4d818d-e0b4-4ab1-89b9-e863458784c0'
	),
	Comment(
		'PermaBagarre',
		datetime.now().timestamp() - 180,
		'6',
		'e4adfd4b-897b-46b9-9e3d-c76db3e63173'
	),
	Comment(
		'TotalusRetardus',
		datetime.now().timestamp() - 100,
		'3',
		'b763f55f-cda3-437a-8a00-b606fcfda6fc'
	),
	Comment(
		'PermaBagarre', 
		datetime.now().timestamp() - 5,
		'6',
		'98cda663-52cf-4450-8695-339c5236fc42'
	),
]

@api.route("/comments", methods=["GET"])
def get_comments():
	return jsonify([comment.serialize() for comment in comments])


@api.route("/comment", methods=["POST"])
def comment():
	charset = string.ascii_letters + string.digits + '-_'

	author = ''.join([c for c in g.auth['user'] if c in charset])
	date = datetime.now().timestamp()
	profile_picture = 'guest'
	content = request.json.get('content', None)

	if content is None:
		return "Requête invalide", 400
	
	content_id = str(uuid4())
	with open(f'public/data/{content_id}', 'w', encoding='utf-8') as f:
		f.write(content)
	comments.append(Comment(author, date, profile_picture, content_id))
	return "ok", 200

@api.route('/flag', methods=['GET'])
def get_flag():
	user = g.auth['user'] if 'user' in g.auth else None
	if user == 'admin':
		return os.environ.get('FLAG', 'Une erreur est survenue, contactez les admins sur discord.'), 200
	return "Seul l'utilistaur 'admin' à le droit de récupérer des flags gratuitement", 401
