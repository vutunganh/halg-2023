from bottle import Bottle, LocalRequest, request, view, abort, static_file
from argparse import ArgumentParser
from yoyo import get_backend, read_migrations
from gpwebpay import gpwebpay
from gpwebpay.config import configuration as gpWebpayConfig
from time import localtime, strftime
import urllib.parse
import tomllib
import psycopg2
import logging
import datetime
import base64

from email_utils.email_utils import Emailer, EmailTemplate

# App code overview.
# - define cli arguments
# - load configuration
# - perform database migrations
# - connect to the database
#   - this is a separate step because I don't have time to discover how to reuse
#     the connection from the previous step
# - run the web server

# CLI arguments

cli_arg_parser = ArgumentParser(
    prog='HALG registration',
    description='App for registration of HALG 2023 participants.',
    epilog='Contact tung@kam.mff.cuni.cz in case of any issues.'
)
cli_arg_parser.add_argument(
    '-c',
    '--config',
    default='config.example.toml',
    help='Location of a configuration file.'
)

cli_args = cli_arg_parser.parse_args()
config_file_path = cli_args.config
logging.debug('Reading configuration file "{}"'.format(config_file_path))

# Load configuration
app_config = dict()
with open(config_file_path, "rb") as f:
    app_config = tomllib.load(f)

# Database functions
## Perform database migrations
logging.info("[Migrations] Starting")
db_backend = get_backend('postgresql://{}:{}@{}/{}?port={}'.format(
    app_config['Database']['user'],
    app_config['Database']['password'],
    app_config['Database']['host'],
    app_config['Database']['dbname'],
    app_config['Database']['port'],
))
logging.info("[Migrations] Connected")
migrations = read_migrations(app_config['Database']['migrations']['path'])
logging.info("[Migrations] Read")
with db_backend.lock():
    db_backend.apply_migrations(db_backend.to_apply(migrations))
    logging.info("[Migrations] Applied")

## Connect to the database
db_conn = psycopg2.connect(
    host=app_config['Database']['host'],
    port=app_config['Database']['port'],
    user=app_config['Database']['user'],
    password=app_config['Database']['password'],
    dbname=app_config['Database']['dbname'],
)

class ParticipantInfo:
    name: str
    surname: str | None
    email: str
    affiliation: str | None
    address: str
    city: str
    country: str
    zip_code: str | None
    vat_tax_no: str | None
    is_student: bool

    def __init__(
        self,
        name: str,
        surname: str | None,
        email: str,
        affiliation: str | None,
        address: str,
        city: str,
        country: str,
        zip_code: str | None,
        vat_tax_no: str | None,
        is_student: bool,
    ):
        # TODO: get field name using metaprogramming
        def verify_nonempty(s: str, field_name: str) -> str:
            if len(s) > 0:
                return s

            raise ValueError('"Participant.{}" should not be empty.'.format(field_name))
        # TODO: verify nonemptiness like a human
        self.name = verify_nonempty(name, 'name')
        self.surname = surname
        self.email = verify_nonempty(email, 'email')
        self.affiliation = affiliation
        self.address = verify_nonempty(address, 'address')
        self.city = verify_nonempty(city, 'city')
        self.country = verify_nonempty(country, 'country')
        self.zip_code = zip_code
        self.vat_tax_no = vat_tax_no
        self.is_student = is_student

class Participant(ParticipantInfo):
    id: int
    date_registered: datetime.datetime

    def __init__(
        self,
        id: int,
        name: str,
        surname: str | None,
        email: str,
        affiliation: str | None,
        address: str,
        city: str,
        country: str,
        zip_code: str | None,
        vat_tax_no: str | None,
        is_student: bool,
        date_registered: datetime.datetime
    ):

        super().__init__(name, surname, email, affiliation, address, city, country, zip_code, vat_tax_no, is_student)
        self.id = id
        self.date_registered = date_registered

## Database utils
def register_participant(participant: ParticipantInfo):
    cursor = db_conn.cursor()

    cursor.execute("""
    INSERT INTO
    participant (name, surname, email, affiliation, address, city, country, zip_code, vat_tax_no, is_student)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """,
    (participant.name, participant.surname, participant.email, participant.affiliation, participant.address, participant.city, participant.country, participant.zip_code, participant.vat_tax_no, participant.is_student
    ))
    id = cursor.fetchone()[0]
    db_conn.commit()
    cursor.close()
    return id


def check_existing_user(email: str) -> bool:
    cursor = db_conn.cursor()

    cursor.execute("""
    SELECT EXISTS(
        SELECT 1
        FROM participant
        WHERE email = %s
    );
    """, (email, ))

    res = cursor.fetchone()[0]
    db_conn.commit()
    cursor.close()
    return res

def set_participant_payment_url(participant_id: int, payment_url: str):
    cursor = db_conn.cursor()
    cursor.execute("""
    UPDATE participant
    SET payment_url = %s
    WHERE id = %s
    """, (payment_url, participant_id,))

    db_conn.commit()
    cursor.close()

# `order_number` is participant's id in our case.
# Yes, if their payment fails, somebody will have to manually intervene and,
# e.g., remove that participant from the database, and make them register again
# to get a new `payment_url`. There is no time :(
def retrieve_payment_url(order_number: int) -> str:
    cursor = db_conn.cursor()
    cursor.execute("""
    SELECT payment_url
    FROM participant
    WHERE id = %s
    """, (order_number,))

    res = cursor.fetchone()
    if res is None:
        logging.error('Could not find an existing participant with id "{order_number}". They should exist because they managed to pay.')
        abort(500, 'Could not confirm payment. Please contact the organizers.')

    cursor.close()
    return res[0]

def record_successful_payment(order_number: int) -> None:
    cursor = db_conn.cursor()
    cursor.execute("""
    UPDATE participant
    SET has_paid = true
    WHERE id = %s
    """, (order_number,))
    db_conn.commit()
    cursor.close()

def get_participant(id: int) -> ParticipantInfo:
    cursor = db_conn.cursor()

    cursor.execute("""
    SELECT name, surname, email, affiliation, address, city, country, zip_code, vat_tax_no, is_student
    FROM participant
    WHERE id = %s
    """, (id, ))

    return ParticipantInfo(*cursor.fetchone())


# Initialize mailer class
mailer = Emailer(
    app_config['Email']['server'],
    app_config['Email'].get('port', 0),
    app_config['Email'].get('username', None),
    app_config['Email'].get('password', None),
    app_config['Email']['from'],
    app_config['Email']['content']['subject_prefix'],
    app_config['Email']['enabled'],
)

# Run web server

app = Bottle()

# TODO: Set this route to root.
#       This is for development purposes only. In production, route
#       'registration' in the server will be handled by the app, while the rest
#       should be served as static files.
@app.get('/registration.html')
@view('registration')
def show_registration_form():
    return dict()

# Web server utils

def retrieve_form_field(request: LocalRequest, field_name: str) -> str | None:
    field = request.forms.get(field_name)
    if field is None:
        return None

    return field.strip()

# TODO: Set this route to root.
#       See @app.get('/registration.html') for the reason.
@app.post('/registration.html')
@view('registration')
def register():
    errors = []

    def retrieve_field(field_name: str) -> str | None:
        return retrieve_form_field(request, field_name)

    def retrieve_nonempty_field(field_name: str) -> str:
        res = retrieve_field(field_name) or ''
        if len(res) < 1:
            errors.append("Field '{}' must not be empty".format(field_name))

        return res

    # retrieve name
    name = retrieve_nonempty_field('name')

    # retrieve surname
    surname = retrieve_field('surname')

    # retrieve email address
    email = retrieve_nonempty_field('email')

    # retrieve affiliation
    affiliation = retrieve_field('affiliation')

    # retrieve address
    address = retrieve_nonempty_field('address')

    # retrieve city
    city = retrieve_nonempty_field('city')

    # retrieve city
    country = retrieve_nonempty_field('country')

    # retrieve zip code
    zip_code = retrieve_field('zipCode')

    # retrieve zip code
    vat_tax_no = retrieve_field('vatTaxNo')

    # retrieve whether they are a student
    is_student_field = retrieve_field('isStudent')
    # html form sends value "on" for checked checkboxes
    # we have to convert them to a string here
    is_student = True if is_student_field == "on" else False

    if len(errors) > 0:
        return dict(errors=errors)

    if check_existing_user(email):
        errors.append('A participant with email address "{}" is already registered.'.format(email))
        return dict(errors=errors)

    # Write participant to the db
    try:
        new_participant_id = register_participant(ParticipantInfo(name, surname, email, affiliation, address, city, country, zip_code, vat_tax_no, is_student))
    except:
        errors.append('''
        An error has occurred  when registering the participant.
        Please, send a message to the organizers.
        ''')
        logging.error('Could not register participant with email "{}"'.format(email))
        
        return dict(errors=errors)

    # Prepare an email template
    email_template_to_use = EmailTemplate.REGISTRATION_WITHOUT_PAYMENT_LINK

    # Request payment
    # inspired by
    #   https://github.com/filias/gpwebpay_demoshop/blob/master/app.py#L32
    #   https://github.com/filias/gpwebpay
    gw = gpwebpay.GpwebpayClient()
    key_bytes = base64.b64decode(gpWebpayConfig.GPWEBPAY_MERCHANT_PRIVATE_KEY)
    payment_amount = app_config['Payment']['adult_price']
    if is_student:
        payment_amount = app_config['Payment']['student_price']
    payment_amount = int(payment_amount) * int(app_config['Payment']['haler_multiplier'])

    try:
        payment_gate_resp = gw.request_payment(
            amount=payment_amount,
            key=key_bytes,
            order_number=str(new_participant_id),
        )
        if not payment_gate_resp.ok:
            logging.error(
                f'Could not create payment for "{email}".'
                f' Status code: "{payment_gate_resp.status_code}".'
                f' Reason: "{payment_gate_resp.reason}".'
                f' Content: "{payment_gate_resp.content}".'
                f' URL: "{payment_gate_resp.url}".'
            )
            raise Exception()
        set_participant_payment_url(new_participant_id, payment_gate_resp.url)
    except:
        errors.append('Could not create payment URL. Please contact the organizers.')
        return dict(errors=errors)

    # now we know that the registration link exists
    email_template_to_use = EmailTemplate.REGISTRATION

    # Notify the participant that we know about them
    mailer.send_email_from_template(
        email,
        name,
        surname or '',
        email_template_to_use,
        {'payment_link': payment_gate_resp.url or ''},
    )

    return dict(errors=[], payment_url=payment_gate_resp.url)

@app.route('/registration/payment_callback')
@view('payment_callback')
def payment_callback():
    gw = gpwebpay.GpwebpayClient()
    key_bytes = base64.b64decode(gpWebpayConfig.GPWEBPAY_PUBLIC_KEY)

    url_qs = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
    order_no = url_qs['ORDERNUMBER'][0]
    if order_no is None:
        logging.error('Did not receive an order number while verifying a payment.')
        return dict(payment_successful=False)

    payment_verification_result = gw.get_payment_result(request.url, key_bytes)
    if payment_verification_result == {'RESULT': 'The payment communication was compromised.'}:
        logging.error(f'Received compromised message when verifying payment for participant "{order_no}".')
        return dict(payment_successful=False)

    if payment_verification_result['PRCODE'] != '0':
        logging.error(f'Seems like payment for user "{order_no}" did not end successfully.')
        print(payment_verification_result)
        return dict(payment_successful=False)

    try:
        record_successful_payment(order_no)
    except:
        logging.error(f'Payment for "{order_no}" seems to be successful but we could not record it.')
        return dict(payment_successful=False)

    participant_info = get_participant(order_no)
    payment_amount = app_config['Payment']['adult_price']
    if participant_info.is_student:
        payment_amount = app_config['Payment']['student_price']
    mailer.send_email_from_template(
        participant_info.email,
        participant_info.name,
        participant_info.surname or '',
        EmailTemplate.RECEIPT,
        {
            'affiliation': participant_info.affiliation or '',
            'address': participant_info.address,
            'city': participant_info.city,
            'country': participant_info.country,
            'zip_code': participant_info.zip_code or '',
            'vat_tax_no': participant_info.vat_tax_no or '',
            'date': strftime("%Y/%m/%d", localtime()),
            'price': payment_amount,
        }
    )

    return dict(payment_successful=True)

# TODO: Remove this.
#       This is only used to substitute a webserver during development.
# @app.route('/<filename:path>')
# def send_static(filename):
#     return static_file(filename, root='../')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
