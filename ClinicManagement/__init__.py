from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from twilio.rest import Client


app = Flask(__name__)

app.secret_key = 'DBW83972$^&*%$^&GH%&VHJKJJT&%$((0)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/clinicmanagement?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name = 'dqifjhxxg',
    api_key= '785733736631163',
    api_secret ='S6q88hiFzmq88oGl79I18fCZ608'
)


login = LoginManager(app=app)


account_sid = 'AC4275ed153ec6bbb8b3f7fb764f4a86c7'
auth_token = '5abff5fdbcaf2b18f4efca9f30fcac64'
client = Client(account_sid, auth_token)