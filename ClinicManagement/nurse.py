from sqlalchemy import func
from quanlyphongmach import db
import utils
from quanlyphongmach.models import User, Sex, Registration, UserRole, ListRegistration, Medicine, Examination_Medicine, \
    Examination, Rules, Bill
import hashlib


def registration(name, phone, address, dob, sex, booking_date):
    if sex.__eq__('Nam'):
        sex = Sex.MALE
    else:
        sex = Sex.FEMALE
    if utils.check_phone(phone=phone).__eq__(False):
        add_user(name=name, phone=phone, address=address, dob=dob, sex=sex)
    user_id = get_id_by_phone(phone)
    reg = Registration(name=name.strip(), phone=phone, address=address, dob=dob, sex=sex, examination_date=booking_date,
                       list_registration_id=load_list_by_date(booking_date).id, user_id=user_id)
    db.session.add(reg)
    db.session.commit()


def get_id_by_phone(phone):
    return db.session.query(User.id).filter(User.phone.__eq__(phone))


def add_user(name, phone, address, dob, sex):
    username = phone
    password = '123'
    if sex.__eq__('Nam'):
        sex = Sex.MALE
    else:
        sex = Sex.FEMALE
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                phone=phone,
                address=address,
                dob=dob,
                sex=sex)
    db.session.add(user)
    db.session.commit()


def get_doctor_by_name(name):
    return User.query.filter(User.user_role.__eq__(UserRole.DOCTOR),
                             User.name.__eq__(name)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def confirm_booking(booking_id):
    reg = Registration.query.filter(Registration.id.__eq__(booking_id)).first()
    reg.active = True
    db.session.commit()


def get_max_patient():
    rules = Rules.query.filter(Rules.id == 1).first()
    return rules.amount


def load_booking_list():
    return Registration.query.filter(Registration.active.__eq__(False)).all()


def count_register_in_queue():
    return db.session.query(Registration.active, func.count(Registration.id)) \
        .filter(Registration.active.__eq__(False)).group_by(Registration.active).all()


def get_date_by_booking_id(booking_id):
    reg = Registration.query.filter(Registration.id.__eq__(booking_id)).first()
    return reg.examination_date


def load_booking_list_date(date=None):
    patient_list = db.session.query(Registration.id, Registration.name, Registration.sex, Registration.dob,
                                      Registration.address, Registration.phone, Registration.examination_date)\
                                        .filter(Registration.active.__eq__(True),
                                                Registration.tested.__eq__(False))
    if date:
        patient_list = Registration.query.filter(Registration.examination_date.__eq__(date),
                                        Registration.active.__eq__(True),
                                        Registration.tested.__eq__(False))

    return patient_list.all()


def count_list(date):
    amount = db.session.query(Registration.examination_date, db.func.count(Registration.examination_date)).filter(
        Registration.examination_date.__eq__(date), Registration.active.__eq__(True)).group_by(
        Registration.examination_date).first()
    if amount:
        return amount[1]
    else:
        return 0


def load_list_by_date(examination_date):
    list = ListRegistration.query.filter(ListRegistration.examination_date.__eq__(examination_date)).first()
    if list:
        return list
    list = ListRegistration(examination_date=examination_date,
                            max_patient=get_max_patient())
    db.session.add(list)
    db.session.commit()
    return list


def get_registration(reg_id):
    return Registration.query.filter(Registration.id.__eq__(reg_id)).first()


def load_registration():
    list = Registration.query.filter(Registration.paided.__eq__(False), Registration.tested.__eq__(True))
    return list


def load_registration2(phone):
    list = Registration.query.filter(Registration.paided.__eq__(False), Registration.tested.__eq__(True),
                                     Registration.phone.__eq__(phone))
    return list


def get_examination(reg_id):
    exam = Examination.query.filter(Examination.registration_id.__eq__(reg_id)).first()
    return exam


def get_medicine_price(reg_id):
    exam = get_examination(reg_id=reg_id)
    exam_detail = db.session.query(Examination_Medicine.medicine_id,
                                   Examination_Medicine.amount,
                                   Examination_Medicine.examination_id,
                                   Medicine.price).filter(Medicine.id.__eq__(Examination_Medicine.medicine_id),
                                                          Examination_Medicine.examination_id.__eq__(exam.id))\
        .join(Medicine, Medicine.id == Examination_Medicine.medicine_id)
    return exam_detail


def get_examination_price():
    return Rules.query.filter(Rules.id.__eq__(2))


def update_registration(reg_id):
    reg = get_registration(reg_id=reg_id)
    reg.paided = True
    db.session.commit()


def add_bill(exam_id, examination_price, medicine_price, total, nurse_id):
    bill = Bill(examination_id=exam_id,
                examination_price=examination_price,
                medicine_price=medicine_price,
                total_price=total,
                nurse_id=nurse_id)
    db.session.add(bill)
    db.session.commit()
