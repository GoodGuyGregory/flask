from flaskr import create_app

def test_config():
    assert not create_app().testing
    # check for the lient testing 
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    # ensure the data returned is accurate
    assert response.data == b'Hello, World!'