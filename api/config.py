import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///db.db",
    )
    # mysql+pymysql://root:EzOweSDyuxPGRixKQKQciKjTRVFEADdN@roundhouse.proxy.rlwy.net:13975/railway
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 25
    MAIL_USERNAME = "luismuhele"
    MAIL_PASSWORD = "lvzi vats oyqu vusf"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "1234567890")
