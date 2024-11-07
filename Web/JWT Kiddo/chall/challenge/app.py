import mimetypes
from flask import Flask, render_template
from routers import web, api
from middlewares.auth import handle_auth, response_auth

# Register mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

# Setup Flask app
app = Flask(__name__, static_url_path="/public", static_folder="public")
app.register_blueprint(web, url_prefix="/")
app.register_blueprint(api, url_prefix="/api/")

@app.before_request
def before_request():
    return handle_auth()

@app.after_request
def after_request(response):
    response_auth(response)
    return response

@app.errorhandler(Exception)
def handle_error(error):
    message = error.description if hasattr(error, "description") else [str(x) for x in error.args]
    response = {
        "error": {
            "type": error.__class__.__name__,
            "message": message
        }
    }
    return response, error.code if hasattr(error, "code") else 500

# Running Flask app
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8001, threaded=True, debug=True)
