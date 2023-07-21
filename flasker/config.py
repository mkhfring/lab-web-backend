import os
from datetime import timedelta


class Config(object):
    """
    Default Configuration
    """
    base_url = 'http://localhost:5000/assets'
    TEMP_PATH = '/tmp/sqlalchemy-media'



class DevelopmentConfig(Config):
    """
    Development Configuration
    """
    DEBUG = True


class DeploymentConfig(Config):
    """
    Deployment Confugartion
    """
    DEBUG = False

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    TESTING = True
    DEBUG = True

