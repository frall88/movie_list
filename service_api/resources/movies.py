import logging
from typing import List, Dict

from sanic.request import Request
from sanic.response import json

from service_api.config import Config, runtime_config
from service_api.resources import BaseView
from aiocache import cached
from aiocache.serializers import PickleSerializer


logger = logging.getLogger(__name__)


class MoviesView(BaseView):
    """Representation of movie list with people appearing in them.

    GET /movies

    """

    FILMS_KEY = "films"
    PEOPLE_KEY = "people"

    def __init__(self):
        self.base_url = runtime_config().MOVIE_HOST

    @cached(ttl=Config.CACHE_DEFAULT_TIMEOUT, key="movies", serializer=PickleSerializer())
    async def get(self, request: Request) -> str:
        """Makes json object with movies data.

        Args:
            request: Request object.

        Returns:
             Movies with people data.

        """
        movies = await self._get_entity(self.FILMS_KEY)
        people = await self._get_entity(self.PEOPLE_KEY)
        movies_with_people = self._enrich_movies_by_people(movies, people)
        return json(movies_with_people)

    async def _get_entity(self, entity_name: str) -> List[Dict]:
        """Makes http request by source entity name.

        Args:
            entity_name: resource name.

        Returns:
             Response data.

        """
        logging.info(f"Getting movie entity: {entity_name}")
        request_url = f"{self.base_url}/{entity_name}"
        return await self.make_get_request(request_url)

    @classmethod
    def _enrich_movies_by_people(cls, movies: List[Dict], people: List[Dict]) -> List[Dict]:
        """Adds people list to movie object.

        Args:
            movies: list of movie objects.
            people: list of movie characters.

        Returns:
             List of movies enriched by people appearing in them.

        """

        def add_people_key_to_movie(movie: Dict) -> Dict:
            movie[cls.PEOPLE_KEY] = []
            return movie

        movies_id_map = {movie["id"]: add_people_key_to_movie(movie) for movie in movies}
        for person in people:
            film_ids = list(map(lambda film_uri: film_uri.split("/")[-1], person[cls.FILMS_KEY]))
            for id in film_ids:
                if id in movies_id_map:
                    movies_id_map[id][cls.PEOPLE_KEY].append(person)

        return list(movies_id_map.values())
