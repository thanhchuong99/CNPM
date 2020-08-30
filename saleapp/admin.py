from flask_admin import BaseView, expose
from flask_admin.model import BaseModelView
from flask_login import logout_user, current_user
from wtforms import SelectField
from wtforms.validators import DataRequired, Length, ValidationError

from saleapp import admin, db, models
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Flight, Airport, User, Transit, Reservation
from flask import redirect, render_template


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.get_id() == "1"


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class FlightModelView(ModelView):
    form_extra_fields = {
        'departure': SelectField('Departure',
                                 choices=[(c.airport_id, c.airport_name) for c in models.Airport.query.all()]),
        'arrival': SelectField('Arrival',
                               choices=[(c.airport_id, c.airport_name) for c in models.Airport.query.all()]),
    }

    column_list = ('id', 'departure', 'arrival','time','departure_time','empty')
    can_view_details = True
    column_display_pk = True
    def min_time(form, time):
        if time.data < 10 :
            raise ValidationError('time must be > 30')
    form_args = dict(
        time=dict(label='Time', validators=[min_time])
    )
    def is_accessible(self):
        return current_user.is_authenticated


class TransitModelView(ModelView):
    column_display_pk = True
    form_extra_fields = {
        'flight_id': SelectField('Flight Id',
                                 choices=[(c.id, c.id) for c in models.Flight.query.all()]),
        'airport_id': SelectField('Airport Id',
                               choices=[(c.id, c.airport_name) for c in models.Airport.query.all()]),
    }
    column_list = ('id','flight_id','airport_id','description')
    def is_accessible(self):
        return current_user.is_authenticated


class AirportModelView(ModelView):
    can_create = True
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(AuthenticatedView(Reservation, db.session))
admin.add_view(TransitModelView(Transit, db.session))
admin.add_view(FlightModelView(Flight, db.session))
admin.add_view(AirportModelView(Airport, db.session))
admin.add_view(AuthenticatedView(User, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))
