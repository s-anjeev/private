# extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize the limiter
limiter = Limiter(
    key_func=get_remote_address  # Use remote IP for rate limiting
)
