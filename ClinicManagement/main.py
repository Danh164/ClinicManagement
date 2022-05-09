from quanlyphongmach import app, login, client
from flask import render_template, request, redirect, url_for, session
from admin import *
from flask_login import login_user, logout_user
from quanlyphongmach.models import UserRole
import utils
import doctor
import nurse
import cloudinary.uploader


@app.route("/")
def home():
    return render_template('/client/home.html')


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        try:
            name = request.form.get('name')
            username = request.form.get('username')
            if utils.get_user_by_username(username=username):
                err_msg = 'Username đã tồn tại!!'
                return render_template('/client/register.html', err_msg=err_msg)
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            phone = request.form.get('phone')
            if utils.get_user_by_phone(phone=phone):
                err_msg = 'Số điện thoại đã được sử dụng!!'
                return render_template('/client/register.html', err_msg=err_msg)
            avatar_path = None
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, phone=phone, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = 'Xác nhận mật khẩu không đúng!!!!'
        except Exception as ex:
            err_msg = str(ex)
    return render_template('/client/register.html', err_msg=err_msg)


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username, password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = 'Username hoặc password không chính xác!!!'
    return render_template('/client/login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']
    user = utils.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/user-update', methods=['get', 'post'])
def user_update():
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        sex = request.form.get('sex')
        address = request.form.get('address')
        phone = request.form.get('phone')
        dob = request.form.get('birth')
        avatar = request.files.get('avatar')
        avatar_path = None
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            avatar_path = res['secure_url']
        utils.update_in4(id=session.get('_user_id'), name=name, sex=sex, address=address, phone=phone, dob=dob, avatar=avatar_path)
        return redirect(url_for('user_update'))
    else:
        return render_template('user/user_update.html')


@app.route('/user-booking', methods=['get', 'post'])
def user_booking():
    doctors = utils.load_doctors()
    err_msg = ''
    msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('tel')
        address = request.form.get('address')
        dob = request.form.get('birth')
        sex = request.form.get('sex')
        date = request.form.get('date')
        if int(nurse.count_list(date=date)) == nurse.get_max_patient():
            err_msg = 'Ngày chọn khám đã đầy, mời bạn chọn ngày khác!!!'
        else:
            if utils.check_phone(phone).__eq__(True):
                err_msg = 'số diện thoại này đã được đăng kí'
            else:
                msg = 'Đăng kí thành công!'
                nurse.registration(name=name, phone=phone, address=address, dob=dob, sex=sex,
                                   booking_date=date)
                return render_template('/nurse/registration.html', msg=msg)
    return render_template('/client/user_booking.html', err_msg=err_msg)


# nurse_work
@app.route('/nurse_registration',  methods=['get', 'post'])
def nurse_registration():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('tel')
        address = request.form.get('address')
        dob = request.form.get('birth')
        sex = request.form.get('sex')
        date = request.form.get('date')
        if int(nurse.count_list(date=date)) == nurse.get_max_patient():
            err_msg = 'Ngày chọn khám đã đầy, mời bạn chọn ngày khác!!!'
        else:
            if utils.check_phone(phone).__eq__(True):
                err_msg = 'số diện thoại này đã được đăng kí'
            else:
                msg = 'Đăng kí thành công!'
                nurse.registration(name=name, phone=phone, address=address, dob=dob, sex=sex,
                                   booking_date=date)
                return render_template('/nurse/registration.html', msg=msg)
    return render_template('/nurse/registration.html', err_msg=err_msg)


@app.route('/booking-list', methods=['get', 'post'])
def booking_list():
    date = request.form.get('date-exam')
    book_list = nurse.load_booking_list_date(date=date)
    return render_template('nurse/list_patient.html', book_list=book_list, date=date)


@app.route('/delete-booking')
def delete_booking():
    booking_id = request.args.get('booking_id')
    utils.delete_booking(booking_id=booking_id)
    client.messages.create(
        from_="+16203159042",
        to="+84799507086",
        body="message"
    )
    return redirect(url_for('booking_list'))


@app.route('/update-list')
def update_date():
    return redirect(url_for('booking_list'))


@app.route('/confirm-booking', methods=['get', 'post'])
def confirm_booking():
    book_list = nurse.load_booking_list()
    return render_template('nurse/confirm_register.html', book_list=book_list)


@app.route('/accept-booking')
def accept_booking():
    booking_id = request.args.get('booking_id')
    nurse.confirm_booking(booking_id=booking_id)
    client.messages.create(
        from_="+16203159042",
        to="+84799507086",
        body="message"
    )
    return redirect(url_for('confirm_booking'))


@app.route('/reject-booking')
def reject_booking():
    booking_id = request.args.get('booking_id')
    utils.delete_booking(booking_id=booking_id)
    client.messages.create(
        from_="+16203159042",
        to="+84799507086",
        body="message"
    )
    return redirect(url_for('confirm_booking'))


@app.route('/patient-bill', methods=['post', 'get'])
def patient_bill():
    phone = request.form.get('tel')
    if phone:
        list = nurse.load_registration2(phone=phone)
    else:
        list = nurse.load_registration()
    return render_template('nurse/patient-bill.html', list=list)


@app.route('/pay-bill')
def pay_bill():
    reg_id = request.args.get('reg_id')
    exam_id = request.args.get('exam_id')
    nurse_id = request.args.get('nurse_id')
    exam_price = request.args.get('exam_price')
    med_price = request.args.get('med_price')
    total = request.args.get('total')
    nurse.update_registration(reg_id=reg_id)
    nurse.add_bill(examination_price=exam_price, medicine_price=med_price, total=total, nurse_id=nurse_id, exam_id=exam_id)
    return redirect(url_for('patient_bill'))


@app.route('/bill')
def bill():
    reg_id = request.args.get('reg_id')
    exam = nurse.get_examination(reg_id=reg_id)
    reg = nurse.get_registration(reg_id=reg_id)
    exam_price = nurse.get_examination_price()
    med_price = nurse.get_medicine_price(reg_id=reg_id)
    price = 0
    for m in med_price:
        price = price + m.amount*m.price
    total = price + exam_price[0].amount
    return render_template('nurse/bill.html', reg=reg,  exam_id=exam.id, exam_price=exam_price[0].amount, price=price, total=total)


@app.route('/update-patient-list')
def update_patient_date():
    return redirect(url_for('patient_list'))


# doctor_work
@app.route('/patient-list', methods=['get', 'post'])
def patient_list():
    date = request.form.get('date-exam')
    list = doctor.load_patient_list(date=date)
    return render_template('doctor/patient_list.html', patient_list=list, date=date)


@app.route('/create-examination', methods=['get', 'post'])
def create_examination():
    reg = doctor.get_registration_by_id(request.args.get('patient_id'))
    if request.method.__eq__('POST'):
        disease = request.form.get('disease')
        sympton = request.form.get('sympton')
        if disease and sympton:
            doctor.add_examination(sympton=sympton,
                                   disease=disease,
                                   registration_id=reg[0].id)
            doctor.update_registration(reg[0].id)
            exam = doctor.get_id_examination(reg_id=reg[0].id)
            return render_template('doctor/add_prescription.html', exam_id=exam[0].id, medicine=doctor.load_medicine(),
                                   info=doctor.get_info_patient(exam[0].id))
        else:
            exam = doctor.get_id_examination(reg_id=reg[0].id)
            exam_med = doctor.get_examination_medicine_by_exam_id(exam_id=exam[0].id)
            medicine = doctor.get_id_by_medicine_name(medicine=request.form.get('medicine'))
            amount = request.form.get('amount')
            using_method = request.form.get('using_method')
            check = doctor.check_medicine(exam_id=exam[0].id, med_id=medicine.id)
            if check:
                doctor.update_medicine(exam_id=exam[0].id, med_id=medicine.id, amount=amount, using_method=using_method)
            else:
                doctor.add_prescription(medicine_id=medicine.id,
                                        amount=amount,
                                        examination_id=exam[0].id,
                                        using_method=using_method)

            return render_template('doctor/add_prescription.html', exam_id=exam[0].id, medicine=doctor.load_medicine(),
                                   exam_med=exam_med, info=doctor.get_info_patient(exam[0].id))
    return render_template('doctor/examination.html', registration=reg)


@app.route("/add-prescription", methods=['get', 'post'])
def add_prescription():
    if request.method.__eq__('POST'):
        medicine = doctor.get_id_by_medicine_name(medicine=request.form.get('medicine'))
        amount = request.form.get('amount')
        using_method = request.form.get('using_method')
        examination_id = request.form.get('exam_id')
        doctor.add_prescription(medicine_id=medicine[0].id,
                                amount=amount,
                                examination_id=examination_id,
                                using_method=using_method)
        return redirect(url_for('doctor/add_prescription.html'))
    return render_template('doctor/add_prescription.html')


if __name__ == '__main__':
    app.run(debug=True)
