from loudmouth.settings.base import ALLOWED_HOSTS

ALLOWED_HOSTS += [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "localhost",
    "127.0.0.1",
    "loud-mouth-bend-api.up.railway.app",
    "loudmouth-api.onrender.com",
]

DEBUG = True
