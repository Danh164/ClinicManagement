from sqlalchemy import func
from sqlalchemy.sql import extract
from quanlyphongmach import db
from quanlyphongmach.models import User, Sex, Registration, UserRole, ListRegistration \
    , Registration_User, Medicine, Examination_Medicine, Examination, Rules, Bill
import hashlib


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                phone=kwargs.get('phone'),
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def get_user_by_username(username):
    user = User.query.filter(User.username.__eq__(username)).first()
    return user


def get_user_by_phone(phone):
    user = User.query.filter(User.phone.__eq__(phone)).first()
    return user


def check_phone(phone):
    phone = User.query.filter(User.phone.__eq__(phone)).first()
    if phone:
        return True
    else:
        return False


def check_login(username, password, role=None):
    if role:
        if username and password:
            password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

            return User.query.filter(User.username.__eq__(username.strip()),
                                     User.password.__eq__(password),
                                     User.user_role.__eq__(role)).first()
    else:
        if username and password:
            password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

            return User.query.filter(User.username.__eq__(username.strip()),
                                     User.password.__eq__(password)).first()


def update_in4(id, name, sex, address, phone, dob, avatar):
    user = get_user_by_id(id)
    if user:
        if name:
            user.name = name
        if sex and sex.__eq__('Nam'):
            user.sex = Sex.MALE
        else:
            user.sex = Sex.FEMALE
        if address:
            user.address = address
        if phone:
            user.phone = phone
        if dob:
            user.dob = dob
        if avatar:
            user.avatar = avatar
        db.session.commit()


def delete_booking(booking_id):
    linked = Registration_User.query.filter(Registration_User.registration_id_id.__eq__(booking_id)).all()
    for link in linked:
        db.session.delete(link)
        db.session.commit()
    registration = Registration.query.filter(Registration.id.__eq__(booking_id)).first()
    db.session.delete(registration)
    db.session.commit()


def load_doctors():
    return User.query.filter(User.user_role.__eq__(UserRole.DOCTOR)).all()


def get_booking_by_id(booking_id):
    return Registration.query.filter(Registration.id.__eq__(booking_id)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# lấy danh sách hoá đơn trong tháng và năm
def stats_bill_month(month, year):
    stats = Bill.query.filter((extract('month', Bill.create_date) == month),
                              (extract('year', Bill.create_date) == year)). \
        add_columns(func.count(Bill.create_date), func.sum(Bill.total_price)).group_by(Bill.create_date).all()
    return stats


#lấy danh sách sử dụng thuốc theo tháng và năm
def stats_medicine_by_month(year, month):
    stats = db.session.query(Examination_Medicine.medicine_id, Medicine.name, Medicine.medicine_unit,
                             func.sum(Examination_Medicine.amount).label('so_luong'),
                             func.count(Examination_Medicine.medicine_id).label('so_lan'))\
        .join(Examination, Examination.id == Examination_Medicine.examination_id).group_by(Examination_Medicine.medicine_id).\
        join(Medicine, Medicine.id == Examination_Medicine.medicine_id).filter((extract('month', Examination.created_date) == month),
                                                                               (extract('year', Examination.created_date) == year)).all()
    return stats
