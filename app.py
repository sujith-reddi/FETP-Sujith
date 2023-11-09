
# import json
# import os

# from flask import Flask, redirect, request, url_for
# from flask_login import (
#     LoginManager,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )
# from oauthlib.oauth2 import WebApplicationClient
# import requests


# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
# GOOGLE_DISCOVERY_URL = (
#     "https://accounts.google.com/.well-known/openid-configuration"
# )
# app = Flask(__name__)
# app.secret_key = 'SECRET_KEY'
# # app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# login_manager = LoginManager()
# login_manager.init_app(app)


# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.get(user_id)

# @app.route("/")
# def index():
#     if current_user.is_authenticated:
#         return (
#             "<p>Hello, {}! You're logged in! Email: {}</p>"
#             "<div><p>Google Profile Picture:</p>"
#             '<img src="{}" alt="Google profile pic"></img></div>'
#             '<a class="button" href="/logout">Logout</a>'.format(
#                 current_user.name, current_user.email, current_user.profile_pic
#             )
#         )
#     else:
#         return '<a class="button" href="/login">Google Login</a>'
    
# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

# @app.route("/login")
# def login():
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)

# @app.route("/login/callback")
# def callback():
#     code = request.args.get("code")

#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]

#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )

#     client.parse_request_body_response(json.dumps(token_response.json()))


#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)

#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("index"))

# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = 'your_secret_key'

google_bp = make_google_blueprint(client_id='802089722523-cfs669m9u89t45qq33j26a4f66nusv79.apps.googleusercontent.com',
                                  client_secret='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',
                                  redirect_to='google_login')
app.register_blueprint(google_bp, url_prefix='/google_login')

@app.route('/')
def home():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    data = resp.json()
    profile_picture = data['image']['url']
    return render_template('profile.html', profile_picture=profile_picture)

@app.route('/logout')
def logout():
    google_bp.backend.clear_credentials()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
