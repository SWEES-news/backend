

# tests if users can be fetched
def test_fetch():
    import db.db as data
    assert "tigers" in data.fetch_pets()
