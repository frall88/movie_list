from sanic import Sanic


def load_api(app: Sanic):
    from service_api.resources.movies import MoviesView

    app.add_route(MoviesView.as_view(), "/movies", strict_slashes=False)
