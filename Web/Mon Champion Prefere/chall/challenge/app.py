from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/patch-the-champ', methods=['POST', 'PATCH'])
def patch_the_champ():
    if request.method == 'POST':
        flag = None
        return render_template('home.html', flag=flag)
    elif request.method == 'PATCH':
        flag = os.environ.get('FLAG', 'Une erreur est survenue, contactez les admins sur discord.')
        return flag


if __name__ == '__main__':
    app.run()
