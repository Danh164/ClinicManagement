from sqlalchemy import func
from quanlyphongmach import db
from quanlyphongmach.models import Registration, Medicine, Examination_Medicine, Examination


def load_patient_list(date=None):
    list_patient = db.session.query(Registration.id, Registration.name, Registration.sex, Registration.dob,
                                      Registration.address, Registration.phone, Registration.examination_date)\
                                        .filter(Registration.active.__eq__(True),
                                                Registration.tested.__eq__(False))
    if date:
        list_patient = load_patient_list_date(date=date)

    return list_patient.all()


def load_patient_list_date(date):
    return Registration.query.filter(Registration.examination_date.__eq__(date),
                                        Registration.active.__eq__(True),
                                        Registration.tested.__eq__(False))


def get_registration_by_id(id):
    return Registration.query.filter(Registration.id.__eq__(id))


def load_medicine():
    return Medicine.query.filter(Medicine.active.__eq__(True))


def add_examination(sympton, disease, registration_id):
    examination = Examination(sympton=sympton, disease_prediction=disease, registration_id=registration_id)
    db.session.add(examination)
    db.session.commit()


def get_id_examination(reg_id):
    return Examination.query.filter(Examination.registration_id.__eq__(reg_id))


def get_id_by_medicine_name(medicine):
    return Medicine.query.filter(Medicine.name.__eq__(medicine)).first()


def add_prescription(medicine_id, amount, using_method, examination_id):
    prescription = Examination_Medicine(amount=amount,
                                        using_method=using_method,
                                        medicine_id=medicine_id,
                                        examination_id=examination_id)
    db.session.add(prescription)
    db.session.commit()


def check_medicine(med_id, exam_id):
    exam_med = Examination_Medicine.query.filter(Examination_Medicine.medicine_id.__eq__(med_id),
                                                 Examination_Medicine.examination_id.__eq__(exam_id)).first()
    return exam_med


def update_medicine(med_id, exam_id, amount, using_method):
    exam_med = Examination_Medicine.query.filter(Examination_Medicine.medicine_id.__eq__(med_id),
                                                 Examination_Medicine.examination_id.__eq__(exam_id)).first()
    exam_med.amount = exam_med.amount + int(amount)
    exam_med.using_method = using_method
    db.session.commit()


def update_registration(reg_id):
    reg = get_registration_by_id(reg_id)
    reg[0].tested = True
    db.session.commit()


def get_info_patient(exam_id):
    info = db.session.query(Registration.name, Examination.created_date, Examination.sympton, Examination.disease_prediction).\
        join(Registration, Registration.id.__eq__(Examination.registration_id)).filter(Examination.id.__eq__(exam_id)).first()
    return info


def delete_medicine(medicine_id):
    medicine = Examination_Medicine.query.filter(Examination_Medicine.medicine_id.__eq__(medicine_id)).first()
    db.session.delete(medicine)
    db.session.commit()


def get_examination_medicine_by_exam_id(exam_id):
    exam_med = db.session.query(Medicine.id, Medicine.name, Medicine.medicine_unit, Examination_Medicine.amount,
                                Examination_Medicine.using_method).join(Medicine, Medicine.id.\
                                                                        __eq__(Examination_Medicine.medicine_id)).\
                            filter(Examination_Medicine.examination_id.__eq__(exam_id))
    return exam_med