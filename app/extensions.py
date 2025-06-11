# temp_code_mvp/app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flasgger import Flasgger
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Database ORM
db = SQLAlchemy()

# Object serialization/deserialization
ma = Marshmallow()

# JSON Web Token management
jwt = JWTManager()

# Password hashing
bcrypt = Bcrypt()

# API documentation generator
flasgger = Flasgger()

# Database migration engine
# This allows for version-controlled, non-destructive database schema updates.
migrate = Migrate()

# API rate limiter
# This protects the API from brute-force attacks and abuse.
# It uses the client's IP address to track requests.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)