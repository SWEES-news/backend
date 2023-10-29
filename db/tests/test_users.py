import db.db as data

# tests if users can be fetched
def test_fetch():
    assert "tigers" in data.fetch_pets()
