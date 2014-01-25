from bull import app, db
def get_app():
    """Return the application object."""
    return app

if __name__ == '__main__':
    app.config.from_object('config')
    with app.app_context():
        db.metadata.create_all(bind=db.engine)
    get_app().run(debug=True)
