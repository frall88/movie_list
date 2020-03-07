import logging
from typing import List, Dict

from sanic.response import json

from service_api.app import app
from service_api.config import Config
from service_api.resources import BaseView
from aiocache import cached
from aiocache.serializers import PickleSerializer


logger = logging.getLogger(__name__)


class MoviesView(BaseView):
    def __init__(self):
        self.host = app.config.MOVIE_HOST

    @cached(ttl=Config.CACHE_DEFAULT_TIMEOUT, key="movies", serializer=PickleSerializer())
    async def get(self, request):
        movies = await self._get_entity("films")
        people = await self._get_entity("people")
        movies_with_people = self._enrich_movies_by_people(movies, people)
        return json(movies_with_people)

    async def _get_entity(self, name: str):
        request_url = f"{self.host}/{name}"
        return await self.get_request(request_url)

    @staticmethod
    def _enrich_movies_by_people(movies: List[Dict], people: List[Dict]) -> List[Dict]:
        def add_people_key_to_movie(movie: Dict) -> Dict:
            movie["people"] = []
            return movie

        movies_id_map = {movie["id"]: add_people_key_to_movie(movie) for movie in movies}
        for person in people:
            film_ids = list(map(lambda film_uri: film_uri.split("/")[-1], person["films"]))
            for id in film_ids:
                if id in movies_id_map:
                    movies_id_map[id]["people"].append(person)

        return list(movies_id_map.values())
