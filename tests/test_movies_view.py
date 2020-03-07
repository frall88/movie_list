from http import HTTPStatus

from service_api.resources.movies import MoviesView
from tests import BaseTestCase
from asynctest import patch


MOVIES = [
    {
        "id": "1",
        "title": "Castle in the Sky"
    },
    {
        "id": "2",
        "title": "Grave of the Fireflies"
    },
    {
        "id": "3",
        "title": "Grave of the Fireflies"
    }
]

PEOPLE = [
    {
        "id": "1",
        "name": "Joe",
        "films": ["https://some-domain/films/1", "https://some-domain/films/2"]
    },
    {
        "id": "2",
        "name": "John",
        "films": ["https://some-domain/films/2"]
    },
    {
        "id": "3",
        "name": "John",
        "films": ["https://some-domain/films/4"]
    }
]

EXPECTED_MOVIES_WITH_PEOPLE = [
    {
        "id": "1",
        "title": "Castle in the Sky",
        "people": [
            {
                "id": "1",
                "name": "Joe",
                "films": ["https://some-domain/films/1", "https://some-domain/films/2"]
            }
        ],
    },
    {
        "id": "2",
        "title": "Grave of the Fireflies",
        "people": [
            {
                "id": "1",
                "name": "Joe",
                "films": ["https://some-domain/films/1", "https://some-domain/films/2"]
            },
            {
                "id": "2",
                "name": "John",
                "films": ["https://some-domain/films/2"]
            }
        ],
    },
    {
        "id": "3",
        "title": "Grave of the Fireflies",
        "people": [],
    }
]


class TestMoviesView(BaseTestCase):
    def test_enrich_movies_by_people(self):
        actual_movies_with_people = MoviesView._enrich_movies_by_people(MOVIES, PEOPLE)
        self.assertListEqual(EXPECTED_MOVIES_WITH_PEOPLE, actual_movies_with_people)

    @patch("service_api.resources.BaseView.get_request", side_effect=iter([MOVIES, PEOPLE]))
    def test_get(self, mock):
        _, response = self.app.test_client.get("/movies")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(EXPECTED_MOVIES_WITH_PEOPLE, response.json)
