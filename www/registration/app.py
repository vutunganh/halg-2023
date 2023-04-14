from bottle import Bottle, request, static_file, view
from argparse import ArgumentParser
from yoyo import get_backend, read_migrations
from smtplib import SMTP_SSL
import tomllib
import psycopg2
import logging
import datetime

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
    """,
    (participant.name, participant.surname, participant.email, participant.affiliation, participant.address, participant.city, participant.country, participant.zip_code, participant.vat_tax_no, participant.is_student
    ))

    db_conn.commit()

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
    return res


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

# TODO: Set this route to root.
#       See @app.get('/registration.html') for the reason.
@app.post('/registration.html')
@view('registration')
def register():
    errors = []

    def retrieve_field(field_name: str) -> str | None:
        field = request.forms.get(field_name).strip()
        return field or None

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

    print(name, surname, email, affiliation, address, city, country, zip_code, vat_tax_no, is_student)

    if len(errors) > 0:
        return dict(errors=errors)

    if check_existing_user(email):
        errors.append('A participant with email address "{}" is already registered.'.format(email))
        return dict(errors=errors)

    try:
        register_participant(ParticipantInfo(name, surname, email, affiliation, address, city, country, zip_code, vat_tax_no, is_student))
    except:
        errors.append('''
        An error has occurred  when registering the participant.
        Please, send a message to the organizers.
        ''')

        return dict(errors=errors)

    return dict(errors=[])

# TODO: Remove this.
#       This is only used to substitute a webserver during development.
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='../')

app.run(reloader=True, debug=True)
