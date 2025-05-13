# api/routes/__init__.py
def register_routes(app):
    from .games import games_blueprint
    from .users import users_blueprint
    from .files import files_blueprint

    app.register_blueprint(games_blueprint, url_prefix="/games")
    app.register_blueprint(users_blueprint, url_prefix="/users")
    app.register_blueprint(files_blueprint, url_prefix="/files")
