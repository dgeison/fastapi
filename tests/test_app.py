from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Asset


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'test_user_name',
            'password': 'password',
            'email': 'teste@teste.com',
        },
    )
    # Validar UserPublic

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'id': 1,
        'username': 'test_user_name',
        'email': 'teste@teste.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'test_user_name',
                'email': 'teste@teste.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'test_user_name_updated',
            'password': 'password',
            'email': 'teste@teste.com',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'test_user_name_updated',
        'email': 'teste@teste.com',
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'Usuário deletado com sucesso.'}
