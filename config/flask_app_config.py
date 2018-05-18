
# DB URI
# example DB URI:
# mysql+oursql://scott:tiger@localhost/mydatabase
# postgresql+psycopg2://scott:tiger@localhost/mydatabase
SQLALCHEMY_DATABASE_URI = 'mysql+oursql://<userid>:<password>@<servername>/<db_name>'
# example
# SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:root@localhost/feedback'

# Debug from SQLAlchemy
# Turn this to False on production
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

# List of allowed origins for CORS
ALLOWED_ORIGINS = "['*']"

# List of allowed IPs
WHITELIST_IPS = ["127.0.0.1"]

# Configure your log paths
LOG_FILE_DIRECTORY = 'logs'
LOG_FILE = 'feedback.log'

# Log level for the application
#10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL",
LOG_LEVEL = 10

#Configure the versions of generic feedback forms
GENERIC_FEEDBACK_VERSION = 'generic-feedback-v2.0'
GENERIC_LAB_FEEDBACK_VERSION = 'generic-lab-feedback-v2.0'
GENERIC_EXP_FEEDBACK_VERSION = 'generic-exp-feedback-v2.0'

ELASTIC_DB_URL = "http://10.100.0.15:9200"
FOOTER_URL = "http://footer.base1.vlabs.ac.in/footer"
