from sanic import Sanic


def load_api(app: Sanic):
    """Register application views.

    Args:
        app: Sanic application.

    """
    from service_api.resources.movies import MoviesView

    app.add_route(MoviesView.as_view(), "/movies", strict_slashes=False)
