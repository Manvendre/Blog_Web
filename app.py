import datetime
from flask import Flask, render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage



app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://blogweb_user:CzrjOpbtv5wh0TQiBixm6LcX2yCbCla1@dpg-clstgedcm5oc73bbrfjg-a.oregon-postgres.render.com/blogweb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\777ma\\OneDrive\\Desktop\\BLOG\\static\\assets\\img'

db=SQLAlchemy(app)

class Contacts(db.Model):
    __tablename__='contacts'
    sno = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    phnno = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    __tablename__='posts'
    sno = db.Column(db.Integer, primary_key=True,autoincrement=True)
    tital = db.Column(db.String(80), nullable=False)
    subhead = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(80), nullable=False)
    contant = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    

    


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    return render_template('index.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if "user" in session and session['user']=="Manav":
        posts = Posts.query.all()
        return render_template("dashboard.html", posts=posts)

    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username=='Manav'and userpass=="Manav":
            # set the session variable
            session['user']=username
            posts = Posts.query.all()
            return render_template("dashboard.html", posts=posts)
    
    return render_template("login.html")
        

@app.route("/post/<string:tital>", methods=['GET'])
def post_route(tital):
    post=Posts.query.filter_by(tital=tital).first()
    return render_template('post.html',post=post)


@app.route("/add", methods = ['GET', 'POST'])
def add():
    if "user" in session and session['user']=="Manav":
          if(request.method=='POST'):
               '''Add entry to the database'''
               tital = request.form.get('tital')
               subhead=request.form.get('subhead')
               contant = request.form.get('content')
               f = request.files['file1']
               img_url=f.filename
               f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
               entry = Posts(tital=tital,subhead=subhead,img_url=img_url,contant = contant, date= datetime.datetime.now() )
               db.session.add(entry)
               db.session.commit()

               return redirect('/dashboard')
          return render_template('add.html')


@app.route("/edit/<string:sno>/", methods=['GET','POST'])
def edit(sno):
    if "user" in session and session['user']=="Manav":
        if request.method=="POST":
            box_title = request.form.get('tital')
            #tline = request.form.get('tline')
            contant = request.form.get('content')
            #img_file = request.form.get('img_file')
            date = datetime.datetime.now()
        
            if sno==None:
               post = Posts(tital=box_title,contant=contant,date=date)
               db.session.add(post)
               db.session.commit()
            else: 
               post = Posts.query.filter_by(sno=sno).first()
               post.tital = box_title
               #post.tline = tline
               post.contant = contant
               #post.img_file = img_file
               post.date = date
               db.session.commit()
               return redirect('/edit/'+sno)

    post = Posts.query.filter_by(sno=sno).first()
    return render_template('edit.html',post=post)

@app.route("/delete/<string:sno>" , methods=['GET', 'POST'])
def delete(sno):
    if "user" in session and session['user']=="Manav":
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phnno = phone, message = message, date= datetime.datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')



