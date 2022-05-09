from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Enum, ForeignKey,Date
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
from quanlyphongmach import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


#role
class UserRole(UserEnum):
    ADMIN = 1
    NURSE = 2
    DOCTOR = 3
    USER = 4


#giới tính
class Sex(UserEnum):
    MALE = 0
    FEMALE = 1


#người dùng
class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    sex = Column(Enum(Sex), default=Sex.MALE)
    dob = Column(Date, default=datetime.date(datetime.now()))
    address = Column(String(500), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    phone = Column(String(10), nullable=False, unique=True)
    joined_date = Column(DateTime, default=datetime.date(datetime.now()))
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    #relationship
    registration_user = relationship('Registration_User', backref='user', lazy=True)
    bill_nurse = relationship('Bill', backref='user', lazy=True)

    def __str__(self):
        return self.name


#danh sách đăng ký khám
class ListRegistration(BaseModel):
    __tablename__ = 'list_registration'

    max_patient = Column(Integer, default=30)
    examination_date = Column(Date, default=datetime.date(datetime.now()))

    # relationship
    registration = relationship('Registration', backref='list_registration', lazy=True)


#phiếu đăng ký
class Registration(BaseModel):
    __tablename__ = 'registration'

    name = Column(String(50), nullable=False)
    sex = Column(Enum(Sex), default=Sex.MALE)
    phone = Column(String(10), nullable=False)
    dob = Column(Date, default=datetime.date(datetime.now()))
    address = Column(String(500), nullable=False)
    created_date = Column(DateTime, default=datetime.date(datetime.now()))
    examination_date = Column(Date, default=datetime.date(datetime.now()))
    active = Column(Boolean, default=False)
    tested = Column(Boolean, default=False)
    paided = Column(Boolean, default=False)

    # foreignkey
    list_registration_id = Column(Integer, ForeignKey(ListRegistration.id), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    # relationship
    registration_examination = relationship('Examination', backref='registration', lazy=True)

    def __str__(self):
        return self.name


class Registration_User(db.Model):
    # foreignkey
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    registration_id = Column(Integer, ForeignKey(Registration.id), nullable=False, primary_key=True)


class Medicine(BaseModel):
    __tablename__ = 'medicine'

    name = Column(String(50), nullable=False)
    description = Column(String(5000), nullable= False)
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)

    # foreignkey
    medicine_unit = Column(String(50), nullable=False)

    # relationship
    examination_medicine = relationship('Examination_Medicine', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class Examination(BaseModel):
    __tablename__ = 'examination'

    sympton = Column(String(500), nullable=True)
    disease_prediction = Column(String(500), nullable=True)
    created_date = Column(DateTime, default=datetime.date(datetime.now()))

    # foreignkey
    registration_id = Column(Integer, ForeignKey(Registration.id), nullable=False, primary_key=True)

    # relationship
    examination_medicine = relationship('Examination_Medicine', backref='examination', lazy=True)
    bill = relationship('Bill', backref='examination', lazy=True)


class Examination_Medicine(db.Model):
    amount = Column(Integer, default=0)
    using_method = Column(String(500), nullable=False)

    # foreignkey
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False, primary_key=True)
    examination_id = Column(Integer, ForeignKey(Examination.id), nullable=False, primary_key=True)


class Bill(BaseModel):
    __tablename__ = 'bill'

    examination_price = Column(Float, default= 100000 )
    medicine_price = Column(Float, default=0)
    total_price = Column(Float, default=0)
    create_date = Column(DateTime, default=datetime.date(datetime.now()))

    # foreignkey
    examination_id = Column(Integer, ForeignKey(Examination.id), nullable=False, primary_key=True)
    nurse_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)


class Rules(BaseModel):
    __tablename__ = 'rules'

    name = Column(String(100))
    amount = Column(Integer)


if __name__ == '__main__':
    db.create_all()
