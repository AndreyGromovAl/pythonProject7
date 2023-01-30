from flask import Flask, render_template, request, g, abort, flash, url_for, redirect, jsonify
from FDataBase import FDataBase
import sqlite3
import os
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin


DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "fdgfh78@#5?>gfhf89dx,v06k"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))


login_manager = LoginManager(app)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(id_user):
    print("load_user")
    return UserLogin().fromDB(id_user, dbase)


@app.route("/NewUser")
@login_required
def NewUser():

    return render_template('NewUser.html')

@app.route("/index")
@login_required
def index():

    return render_template('calendar_events.html', menu=dbase.getMenu())

@app.route("/Admin")
@login_required
def Admin():

    return render_template('Admin.html', users=dbase.getUsers())





@app.route("/")
def home():
    return render_template('Login.html')

#Календарь
@app.route("/calendar-events")
@login_required
def calendar_events():
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect('flsite.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event")
        rows = cursor.fetchall()
        resp = jsonify({'success': 1, 'result': rows})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return render_template("calendar_events.html", menu=dbase.getMenu(), users=dbase.getUsers())






#Редактирование пользователя
@app.route("/update", methods=["POST","GET"])
@login_required
def update():
  if request.method == "POST":

      res = dbase.update(request.form['g'],request.form['p'],request.form['id_user'],request.form['a'],request.form['o'])
      if res:
          flash("Редактирование успешно", "success")
      else:
          flash("Ошибка при редактировании", "error")
  else:
      flash("Неверно заполнены поля", "error")

  return render_template("RedactUsers.html", menu = dbase.getMenu(),  users=dbase.getUsers())


#Для поиска пользователей
@app.route("/search", methods=["POST","GET"])
def getUsersFromSearch():
    if request.method == "POST":
       res = dbase.getUsersFromSearch(request.form['search'])
       Login = g
    else:
        flash("Что-то пошло не так", "error")

    return render_template("RedactUsers.html", user=res, Login=Login)





#Для регистрации
@app.route("/register", methods=["POST", "GET"])
@login_required
def register():
    if request.method == "POST":
        res = dbase.addUser(request.form['FullName'], request.form['Login'], request.form['Password'])
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('Admin'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    else:
        flash("Неверно заполнены поля", "error")

    return render_template('NewUser.html', menu = dbase.getMenu(), title="Регистрация")


@app.route("/register")
@login_required
def showUsers(id_user):
    FullName, Login, Password = dbase.getUserByReg(id_user)
    if not FullName or Login or Password:
        abort(404)

    return render_template('Admin.html', menu=dbase.getMenu(), FullName=FullName, Login=Login, Password=Password)


#для авторизации
@app.route("/", methods=["POST","GET"])
def Login():
    if request.method == "POST":
        user = dbase.getUserByLogin(request.form['Login'],request.form['Password'])
        if user:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('User'))

        flash("Неверный логин или пароль ", "error")

    return render_template("Login.html", menu=dbase.getMenu(), title="Авторизация")

#@app.route("/main", methods=["POST","GET"])
#@login_required
#def main():

#    return render_template("main.html",title="Главная страница")

@app.route("/User",methods=["POST","GET"])
def user():
    return render_template("main.html",classs=dbase.getClass())

@app.route("/AddLesson/<classname>")
def ShowLesson(classname):
    Lesson = dbase.getOffice(classname)


    return render_template("AddLesson.html", classs=dbase.getClass(), Lesson=Lesson, classname=classname)


@app.route("/AddLesson",methods=["POST","GET"])
@login_required
def Lesson():

    return render_template("AddLesson.html")



@app.route("/AddLesson/<classname>/AddField",methods=["POST","GET"])
@login_required
def AddField(classname):
    if request.method == "POST":
        res = dbase.Addf(request.form['timestart'], request.form['timestop'], request.form['teacher'],request.form['cabinet'])
        if res:
            flash("Поле успешно добавлено", "success")
            #return redirect(url_for('AddLesson'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    else:
        flash("Неверно заполнены поля", "error")

    return render_template("AddFieldSchedule.html",classs=dbase.getClass(),classname=classname)



@app.route("/AddLesson/<classname>", methods=["POST","GET"])
@login_required
def deloff(classname):
  if request.method == "POST":

      res = dbase.delof(request.form.get('s'),request.form.get('e'),request.form.get('d'))
      if res:
          flash("Редактирование успешно", "success")
      else:
          flash("Ошибка при редактировании", "error")
  else:
      flash("Неверно заполнены поля", "error")

  return render_template("AddLesson.html", menu = dbase.getMenu(), users=dbase.getUsers(),classname=classname)



#разрываю соединение
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)