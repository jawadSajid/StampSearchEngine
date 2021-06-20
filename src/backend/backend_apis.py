from flask import Flask, request, jsonify
from flask import Flask,render_template,request,redirect
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login, JobModel, StampModel, CatalogModel, ImageModel
import time
# import requests
import cv2
import numpy as np
from elasticsearch import Elasticsearch
import lib_file

app = Flask(__name__)
app.secret_key = 'xyz'
DIR_FOR_IMAGES = '/home/jawad/Desktop/StampSearchEngine/src/backend/ImagesFromUser/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stampSearchEngine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'

es = Elasticsearch([{'host':'localhost','port':9200}])
ses = lib_file.SignatureES(es)

@app.before_first_request
def create_all():
    db.create_all()

@app.route('/checkAuth' ,methods=['GET'])
def checkAuth():
    if current_user.is_authenticated:
        return {'return': 'already authenticated'}
    else:
        return {'return': 'not authenticated'}

@app.route('/register', methods=['POST'])
def register():

    if request.method == 'POST':

        data = request.get_json()

        email = data['email']
        firstName = data['firstName']
        lastName = data['lastName']
        password = data['password']

        if UserModel.query.filter_by(email=email).first():
            return {'return':'email already present'}

        user = UserModel(email=email, firstName=firstName, lastName=lastName)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        uid = user.id

        dtime = time.asctime(time.localtime(time.time()))

        job = JobModel(datetime=str(dtime), jobtype='Register', uid=uid)
        db.session.add(job)
        db.session.commit()

        return {'return': 'registered'}

@app.route('/login', methods = ['POST'])
def login():
    if current_user.is_authenticated:
        return {'return': 'already authenticated'}
    
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = UserModel.query.filter_by(email = email).first()
            
        if user is not None and user.check_password(password):

            login_user(user)
            
            uid = user.id

            obj = UserModel.query.filter_by(id=int(uid)).one()
            firstName = obj.firstName

            dtime = time.asctime(time.localtime(time.time()))

            job = JobModel(datetime=str(dtime), jobtype='Login', uid=uid)
            db.session.add(job)
            db.session.commit()

            return {'return': 'logged in', 'firstName': firstName}
        else:
            return {'return': 'not logged in'}

@app.route('/logout' ,methods=['GET'])
@login_required
def logout():

    uid = current_user.id

    dtime = time.asctime(time.localtime(time.time()))

    job = JobModel(datetime=str(dtime), jobtype='Logout', uid=uid)
    db.session.add(job)
    db.session.commit()

    logout_user()

    return {'return': 'logged out'}

@app.route('/addStampFile', methods=['POST', 'GET'])
def addStampFile():

    if request.method == 'GET':
        return {'return': 'hello'}
    else:

        filestr = request.files['myFile'].read()
        filename = request.form.get('filename')
        fieldName = request.form.get('fieldName')
        uid = current_user.id

        image = ImageModel(image_name=filename, image_type=fieldName)
        db.session.add(image)
        db.session.commit()

        obj = ImageModel.query.filter_by(image_name=filename).one()
        imageid = obj.iid

        title = request.form.get('title')
        country = request.form.get('country')
        year = request.form.get('year')
        stampNumber = request.form.get('stampNumber')
        faceValue = request.form.get('faceValue')
        info = request.form.get('info')

        stamp = StampModel(title=title, country=country, year=year, stamp_number=stampNumber, face_value=faceValue, info=info, uid=uid, iid=imageid)
        db.session.add(stamp)
        db.session.commit()

        catalogName = request.form.get('catalogName')
        catalogNumber = request.form.get('catalogNumber')
        catalogYear = request.form.get('catalogYear')
        price = request.form.get('price')
        scottNumber = request.form.get('scottNumber')
        verientNumber = request.form.get('verientNumber')

        catalog = CatalogModel(name=catalogName, number=catalogNumber, year=catalogYear, price=price, scott_number=scottNumber, verient_number=verientNumber, uid=uid, iid=imageid)
        db.session.add(catalog)
        db.session.commit()

        dtime = time.asctime(time.localtime(time.time()))

        job = JobModel(datetime=str(dtime), jobtype='Stamp Added', uid=uid)
        db.session.add(job)
        db.session.commit()

        npimg = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        cv2.imwrite(DIR_FOR_IMAGES+ filename, img)

        ses.add_image(DIR_FOR_IMAGES + filename)
        # print(es.indices.exists(DIR_FOR_IMAGES + filename))
        # print(es.indices.exists([filename]))
        images = [filename]
        print(es.indices.exists('images'))

        return {'return': 'stamp added'}

@app.route('/test', methods=['GET'])
def test():
    return {'return': 'test'}

app.run(host='0.0.0.0', port=5000)