import os

class Config:
    '''
    Represents the configuration settings for the application.
    
    Attributes:
        SECRET_KEY (str): The secret key for the application, defaults to 'your-secret-key' if not provided in the environment.
        SQLALCHEMY_DATABASE_URI (str): The URI for the SQLite database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Indicates whether to track modifications in SQLAlchemy.
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False