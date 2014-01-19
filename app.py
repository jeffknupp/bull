from bull import app
def get_app():
    """Return the application object."""
    return app

if __name__ == '__main__':
    app.config.from_object('config')
    from bull import bull
    get_app().run(debug=True)
