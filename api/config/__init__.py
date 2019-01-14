import os

def load_config():
    mode = os.environ.get('MODE')
    try:
        if mode == 'PRODUCTION':
            from api.config.production import ProductionConfig
            return ProductionConfig
        elif mode == 'TESTING':
            from api.config.testing import TestConfig
            return TestConfig
        else:
            from api.config.development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError as e:
        raise e
