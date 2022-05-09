from quanlyphongmach import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from quanlyphongmach.models import User, Medicine, UserRole, Rules, Bill
from flask_login import current_user, logout_user
from flask import redirect, request
import utils


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class UserView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_filters = ['name', 'username', 'phone', 'sex', 'address', 'user_role', 'joined_date', 'dob']
    column_searchable_list = ['name', 'username', 'phone', 'sex', 'address', 'user_role', 'joined_date', 'dob']
    column_labels = {
        'name': 'Tên',
        'sex': 'Giới tính',
        'dob': 'Năm sinh',
        'address': 'Địa chỉ',
        'phone': 'Số điện thoại',
        'joined_date': 'Ngày đăng kí',
        'user_role': 'Vai trò',
        'avatar': 'Ảnh đại diện'
    }


class MedicineView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_filters = ['name', 'description', 'medicine_unit', 'price']
    column_searchable_list = ['name', 'description', 'medicine_unit', 'price']
    column_labels = {
        'name': 'Tên thuốc',
        'description': 'Mô tả',
        'medicine_unit': 'Đơn vị thuốc',
        'price': 'Giá'
    }


class RuleView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_labels = {
        'name': 'Tên quy định',
        'amout': 'Số lượng'
    }


class BillView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_labels = {
        'examination_price': 'Tiền khám',
        'medicine_price': 'Tiền thuốc',
        'total_price': 'Tổng tiền',
        'create_date': 'Ngày tạo'
    }


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/home.html')


# thống kê doanh thu theo tháng
class StatsBillView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        year = request.args.get('year')
        stats = utils.stats_bill_month(month=month, year=year)
        total = 0
        for s in stats:
            total = total + s[2]
        return self.render('admin/stats_bill.html', stats=stats, total=total, year=year, month=month)


# thống kê tần suất sử dụng thuốc
class StatsMedicineView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        year = request.args.get('year')
        stats = utils.stats_medicine_by_month(month=month, year=year)
        return self.render('admin/stats_medicine.html', year=year, stats=stats, month=month)


admin = Admin(app=app, name="Phòng Mạch DS", template_mode='bootstrap4', index_view=MyAdminIndex())

admin.add_view(UserView(User, db.session, name='Quản lí user'))
admin.add_view(MedicineView(Medicine, db.session, name='Quản lí thuốc'))
admin.add_view(RuleView(Rules, db.session, name='Quy định'))
admin.add_view(BillView(Bill, db.session, name='Hoá đơn'))
admin.add_view(StatsBillView(name='Thống kê doanh thu'))
admin.add_view(StatsMedicineView(name='Tần suất sử dụng thuốc'))
admin.add_view(LogoutView(name='Đăng xuất'))
