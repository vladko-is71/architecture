from DataValidator import DataValidator
from PasswordHasher import PasswordHasher
from flask import Flask, render_template, request
from decimal import Decimal


class Entrant(object):
    __slots__ = ['surname', 'name', 'patronymic',
                 'zno', 'certificate', 'extra',
                 'free_applications', 'sent_applications', 'eligible']

    def __init__(self, surname, name, patronymic, zno, certificate, extra):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.eligible = True  # eligible only if all ZNO grades are above 100
        self.zno = [0 for i in range(3)]
        for i in range(3):
            try:
                if 100 <= zno[i] <= 200:
                    self.zno[i] = zno[i]
                else:
                    self.eligible = False
            except IndexError:
                self.eligible = False
        if 1 <= certificate <= 12:
            self.certificate = certificate
        else:
            self.certificate = 1

        self.extra = extra
        self.free_applications = [True for i in range(3)]
        self.sent_applications = [None for i in range(3)]

    # Returns the rating of the student in 200-point scale
    def rating(self):
        if not self.eligible:
            return 0

        # initial ratings and subject coefficients
        total = Decimal('0')
        coefficients = [Decimal('0.2'), Decimal('0.5'), Decimal('0.25')]

        # part of rating that comes from ZNO ratings
        for i in range(3):
            total += self.zno[i] * coefficients[i]

        # part of rating that comes from certificate ratings
        certif = (self.certificate * 10) + 80 if self.certificate >= 2 else 100
        total = certif * Decimal('0.05')

        # part of rating that comes from extra achievements
        total += self.extra

        # the rating can't be above 200
        return total if total <= 200 else 200

    # Sends application for speciality
    def send_application(self, speciality, priority):
        application = Application(self, speciality, priority)
        if not self.free_applications[priority-1]:
            return
        else:
            self.free_applications[priority-1] = False
            self.sent_applications[priority-1] = application
            speciality.applications.append(application)


class Application(object):
    __slots__ = ['applicant', 'speciality', 'priority']

    def __init__(self, applicant, speciality, priority):
        self.applicant = applicant
        self.speciality = speciality
        self.priority = priority


class Speciality(object):
    __slots__ = ['code', 'name', 'faculty',
                 'budget_license', 'total_license', 'applications']

    def __init__(self, code, name, faculty, budget_license, total_license):
        self.code = code
        self.name = name
        self.budget_license = budget_license
        self.total_license = total_license
        self.applications = []
        faculty.specialities.append(self)


class Faculty(object):
    __slots__ = ['full_name', 'short_name', 'specialities',
                 'list_service', 'admitting_service']

    def __init__(self, full_name, short_name, specialities):
        self.full_name = full_name
        self.short_name = short_name
        self.specialities = specialities
        self.list_service = ListService()
        self.admitting_service = AdmittingService()


class ListService(object):
    def __init__(self):
        pass


class AdmittingService(object):
    def __init__(self):
        pass


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('main.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_handler', methods=['POST'])
def signup_handler():
    surname = request.form['surname']
    name = request.form['name']
    patronymic = request.form['patronymic']
    zno_ukr = Decimal(request.form['ukr'])
    zno_math = Decimal(request.form['math'])
    zno_third = Decimal(request.form['third'])
    certificate = Decimal(request.form['certificate'])
    extra = Decimal(request.form['extra'])
    person = Entrant(surname, name, patronymic,
                     [zno_ukr, zno_math, zno_third], certificate, extra)
    email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password1']
    if password1 != password2 or\
            not DataValidator.email_validation(email) or\
            not DataValidator.password_validation(password1):
        return render_template('signup_failure.html')
    hashed_password = PasswordHasher.password_hashing(password1)
    # pushing to database will be here
    return render_template('signup_success.html')


if __name__ == '__main__':
    app.run(port=443)
