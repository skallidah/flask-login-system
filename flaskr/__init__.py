import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    @app.route("/")
    def index():
        return "Flask login App is live!!"

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    db_path = os.path.join(app.instance_path, 'flaskr.sqlite')
    if not os.path.exists(db_path):
        with app.app_context():
            db.init_db()  # creates tables if they don't exist

    if 'hello' not in app.view_functions:
        # Simple page
        @app.route('/hello')
        def hello():
            return 'Hello, world'
    
    from . import auth
    app.register_blueprint(auth.bp)

    return app
