from pathlib import Path

# Special function to configure the Flask app : Use a default, if custom provided use that, if test_config provided use that.
def configure_app(app, test_config):
    INSTANCE_PATH = Path(app.instance_path)
    
    # Create instance folder and ignore if already present
    INSTANCE_PATH.mkdir(mode=777, exist_ok=True)
    
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{INSTANCE_PATH}/khanapina_db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SEND_FILE_MAX_AGE_DEFAULT = 360
    )
    
    if test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    return app
