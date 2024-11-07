from flask import Flask, session
import mimetypes
from os import urandom
from routers.web import router as router_web
from routers.api import router as router_api

# Register mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

# Setup Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = urandom(32)
app.register_blueprint(router_web, url_prefix="/")
app.register_blueprint(router_api, url_prefix="/api/")


@app.before_request
def before_request():
    if 'flag' not in session:
        session['flag'] = False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
