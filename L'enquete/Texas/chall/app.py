from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template_string, request, render_template, make_response

app = Flask(__name__)

COOKIE = 'user_connection_session'
creds = {'username': 'admin', 'password': '36070dbabf840cc76b1c88a18a4b6e06a9c4a871c5f9e63adadbb31d2181953c'}
messages_page_content = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8"/>
    <title>Private Chat</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>

    <link href="static/messages-style.css" rel="stylesheet"/>

    <script src="static/script.js" type="text/javascript">
    
    </script>
</head>

<body onload="CheckLocation();">
    <div class="page_wrap">
       <div class="page_header">
        <div class="content">
         <div class="text bold">
           Somier
         </div>
        </div>
       </div>
       <div class="page_body chat_page">
            <div class="history">

                <h3>CYBN{La_TR0nch3_Du_C0oKie}</h3>

                 <div class="message service" id="message-1">
                  <div class="body details">
                   07 juillet 2024
                  </div>
                 </div>

                <div class="message default clearfix" id="message789">
                  <div class="pull_left userpic_wrap">
                   <div class="userpic userpic2" style="width: 42px; height: 42px">
                    <div class="initials" style="line-height: 42px">
                     S
                    </div>
                   </div>
                  </div>
                  <div class="body">
                   <div class="pull_right date details">
                    16:55
                   </div>
                   <div class="from_name">
                    Somier
                   </div>
                   <div class="text">
                    Tu as bien pu installer le laptop ?
                   </div>
                  </div>
                 </div>

                <div class="message default clearfix" id="message790">
                  <div class="pull_left userpic_wrap">
                   <div class="userpic userpic5" style="width: 42px; height: 42px">
                    <div class="initials" style="line-height: 42px">
                    T
                    </div>
                   </div>
                  </div>
                  <div class="body">
                   <div class="pull_right date details">
                    16:56
                   </div>
                   <div class="from_name">
                    Texas
                   </div>
                   <div class="text">
                       Oui tout va bien
                   </div>
                  </div>
                 </div>

            <div class="message default clearfix" id="message791">
              <div class="pull_left userpic_wrap">
               <div class="userpic userpic2" style="width: 42px; height: 42px">
                <div class="initials" style="line-height: 42px">
                S
                </div>
               </div>
              </div>
              <div class="body">
               <div class="pull_right date details">
                16:58
               </div>
               <div class="from_name">
                Somier
               </div>
               <div class="text">
                Pense à récupérer le Doro dans ta boite aux lettres. Il te sera utile.
               </div>
              </div>
             </div>
             <div class="message default clearfix" id="message798">
             <div class="pull_left userpic_wrap">
               <div class="userpic userpic2" style="width: 42px; height: 42px">
                <div class="initials" style="line-height: 42px">
                S
                </div>
               </div>
              </div>
             <div class="body">
               <div class="pull_right date details">
                17:04
               </div>
               <div class="from_name">
                Somier
               </div>
               <div class="text">
                Il faudrait d'ailleurs que tu passes au ciné, celui dont je t'ai parlé. Une place à 5€, pour la séance prochaine, salle 19.
               </div>
              </div>
             </div>

                <div class="message default clearfix" id="message790">
                  <div class="pull_left userpic_wrap">
                   <div class="userpic userpic5" style="width: 42px; height: 42px">
                    <div class="initials" style="line-height: 42px">
                    T
                    </div>
                   </div>
                  </div>
                  <div class="body">
                   <div class="pull_right date details">
                    17:04
                   </div>
                   <div class="from_name">
                    Texas
                   </div>
                   <div class="text">
                       C est noté.
                   </div>
                  </div>
                 </div>

                <div class="message service" id="message-3">
                    <div class="body details">
                        21 juillet 2024
                    </div>
                </div>

                <div class="message default clearfix" id="message794">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic2" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                S
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            14:28
                        </div>
                        <div class="from_name">
                            Somier
                        </div>
                        <div class="text">
                            On se refait un ciné. Pas la séance prochaine, la suivante, salle 17. Tu pourras prendre 4 popcorn à 7€.
                        </div>
                    </div>
                </div>

                <div class="message default clearfix" id="message795">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic5" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                T
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            15:03
                        </div>
                        <div class="from_name">
                            Texas
                        </div>
                        <div class="text">
                            Pas de soucis, j y serai
                        </div>
                    </div>
                </div>


                <div class="message service" id="message-4">
                    <div class="body details">
                        05 août 2024
                    </div>
                </div>

                <div class="message default clearfix" id="message796">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic2" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                S
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            12:12
                        </div>
                        <div class="from_name">
                            Somier
                        </div>
                        <div class="text">
                            T'as bien noté les noms la dernière fois ?
                        </div>
                    </div>
                </div>

                <div class="message default clearfix" id="message796">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic5" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                T
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            13:04
                        </div>
                        <div class="from_name">
                            Texas
                        </div>
                        <div class="text">
                            Oui, pourquoi ?
                        </div>
                    </div>
                </div>

                <div class="message default clearfix" id="message796">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic2" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                S
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            13:05
                        </div>
                        <div class="from_name">
                            Texas
                        </div>
                        <div class="text">
                            La Batte devrait t'appeler. Note bien le numéro.
                        </div>
                    </div>
                </div>

                <div class="message default clearfix" id="message796">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic5" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                T
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            13:05
                        </div>
                        <div class="from_name">
                            Texas
                        </div>
                        <div class="text">
                            OK
                        </div>
                    </div>
                </div>


                <div class="message service" id="message-4">
                    <div class="body details">
                        09 septembre 2024
                    </div>
                </div>

                <div class="message default clearfix" id="message796">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic2" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                S
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            22:38
                        </div>
                        <div class="from_name">
                            Somier
                        </div>
                        <div class="text">
                            On doit voir le nouveau film. Les prix ont augmenté, 3 popcorn à 8€, salle 11. Prochaine séance.
                        </div>
                    </div>
                </div>

                <div class="message default clearfix" id="message797">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic5" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                T
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            22:41
                        </div>
                        <div class="from_name">
                            Texas
                        </div>
                        <div class="text">
                            ça roule
                        </div>
                    </div>
                </div>


                <div class="message service" id="message-5">
                    <div class="body details">
                        10 octobre 2024
                    </div>
                </div>

                <div class="message default clearfix" id="message798">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic2" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                S
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            19:35
                        </div>
                        <div class="from_name">
                            Somier
                        </div>
                        <div class="text">
                            Nouvelle séance de film, la suivante. Même ciné, salle 18, rang 30. Prends moi la bouteille à 3€.
                        </div>
                    </div>
                </div>

                <div class="message default clearfix" id="message799">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic5" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                T
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            21:16
                        </div>
                        <div class="from_name">
                            Texas
                        </div>
                        <div class="text">
                            Parfait
                        </div>
                    </div>
                </div>

                <div class="message service" id="message-5">
                    <div class="body details">
                        25 octobre 2024
                    </div>
                </div>

                <div class="message default clearfix" id="message798">
                    <div class="pull_left userpic_wrap">
                        <div class="userpic userpic2" style="width: 42px; height: 42px">
                            <div class="initials" style="line-height: 42px">
                                S
                            </div>
                        </div>
                    </div>
                    <div class="body">
                        <div class="pull_right date details">
                            15:36
                        </div>
                        <div class="from_name">
                            Somier
                        </div>
                        <div class="text">
                            On a un nouveau film à se voir. La bouteille à 6€33 sera parfait pour nous. C'est salle 14, range 15. Prochaine séance.
                        </div>
                    </div>
                </div>

            </div>
       </div>
    </div>
</body>
</html>
"""

def any_in_str(lst, string):
    return any(s in lst for s in string)


def create_cookie(user):
    time = datetime.timestamp(datetime.now() + timedelta(minutes=30))
    u = ''.join([str(ord(s)) for s in user.upper()])
    cookie = str(time)[:10] + u
    return cookie, time


def check_credentials(form):
    if form["username"] == creds["username"] and hashlib.sha256(form["password"].encode()).hexdigest() == creds[
        "password"]:
        return True
    else:
        return False


def check_auth(request):
    cookie = request.cookies.get(COOKIE)
    if not cookie:
        return None

    time = datetime.fromtimestamp(int(cookie[:10]))
    if datetime.now() + timedelta(hours=1) < time:
        return "Session too long!"
    elif time < datetime.now():
        return "Session expired!"
    elif datetime.now() + timedelta(hours=1) > time > datetime.now():
        u = cookie[10:]
        user = ''
        for i in range(0, len(u), 2):
            user += chr(int(u[i:i + 2]))
        return user.lower()
    else:
        return None


def render_page(request, title, content):
    import os
    username = check_auth(request)

    list = os.listdir("static")
    menu = ""
    for file in [l for l in list if l.endswith('.html')]:
        file = file.split('.')[0]
        menu += f"<li><a href='blog?page={file}'>{file}</a></li>"
    if username == creds['username']:
        menu += "<li><a id='secret' href='messages'>messages</a></li>"

    if username:
        button = "<a href='/logout'>Déconnexion</a>"
    else:
        button = "<a href='/login'>Connexion</a>"

    return render_template_string(template.format(menu, title, content, username or "guest", button))


def get_file_content(file):
    with open(file, "r") as f:
        content = f.read()
    return content


template = get_file_content("templates/base.html")


@app.route('/', methods=['GET'])
def home():
    content = get_file_content("templates/index.html")

    return render_page(request, "Mon <span class='gray'>Blog</span>", content)


@app.route('/blog', methods=['GET'])
def show_blog():
    args = request.args
    page = args.get('page')
    if not page:
        return 'Welcome to my blog'
    hack_chars = ['_', '[', '.', 'self', 'py', 'sudo']
    if any_in_str(hack_chars, page):
        return "HACKING DETECTED!!"
    page = page.replace("{{", "").replace("}}", "")
    try:
        t = get_file_content(f"static/{page}.html")
    except:
        t = ""

    return render_page(request, page, t)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if user := check_auth(request):
        return render_page(request, "Login", f"Logged in as {user}")
    else:
        if request.method == 'POST':
            is_login = check_credentials(request.form)
            if is_login:
                resp = make_response(render_page(request, f"Connecté {request.form['username']} !", "<p>Retour <a href='/'>maison</a></p>"))
                cookie, expire = create_cookie(request.form['username'])
                resp.set_cookie(COOKIE, cookie, expires=expire)
                return resp
            else:
                return render_page(request, "Login", "Credentials error")
        elif request.method == 'GET':
            content = get_file_content("templates/login.html")
            return render_page(request, "Login", content)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    resp = make_response(render_page(request, "Déconnecté !", "<p>Retour <a href='/'>maison</a></p>"))
    resp.delete_cookie(COOKIE)
    return resp


@app.route('/messages', methods=['GET'])
def secret_page():
    user = check_auth(request)
    print(user)
    if user == 'admin':
        return messages_page_content
    elif not user:
        return "Not logged in"
    else:
        return "Not admin"


@app.errorhandler(404)
def page_not_found(e):
    return render_page(request, "Pas trouvé", "<p>Retour <a href='/'>maison</a></p>")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
