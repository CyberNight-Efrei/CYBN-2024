from conf import DURATION, TO_SOLVE
from flask import Blueprint, render_template, session
import os

router = Blueprint("web", __name__)


@router.get('/')
def index():
    if session['flag']:
        return render_template('flag.html', flag=os.environ.get('FLAG', 'Une erreur est survenue, contactez les admins sur discord.'))
    else:
        return render_template('captcha.html', duration=DURATION, to_solve=TO_SOLVE)

