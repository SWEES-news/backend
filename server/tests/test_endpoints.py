
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

# tests if the hello world endpoint, which indicates if server is running at all
def test_hello():
    resp = TEST_CLIENT.get('/hello')
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert 'hello' in resp_json

# checks the users
def test_list_users():
    resp = TEST_CLIENT.get('/users')
    resp_json = resp.get_json()
    assert isinstance(resp_json, str)
    assert len(resp_json) > 0