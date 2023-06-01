import pytest
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "marcos",
            "last_name": "jr",
            "cpf": "400.077.560-03",
            "email": "teste",
            "birth_date": "1998-07-04"
          }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "marcos",
            "last_name": "jr",
            "cpf": "400.077.560-06",
            "email": "teste",
            "birth_date": "1998-07-04"
          }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"criado" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"CPF INVALID" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get('/user/%s' % valid_user["cpf"])
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "marcos"
        assert response.json[0]["last_name"] == "jr"
        assert response.json[0]["cpf"] == "400.077.560-03"
        assert response.json[0]["email"] == "teste"

        birth_date = response.json[0]["birth_date"]["$date"]
        assert birth_date == "1998-07-04T00:00:00Z"

        response = client.get('/user/%s' % invalid_user["cpf"])
        assert response.status_code == 400
        assert b"Usuario nao existe na base" in response.data
