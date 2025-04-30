from settings import Settings


def test_settins_init():
    settings = Settings()
    assert settings != None


def test_settins_get_db_url():
    settings = Settings()
    assert settings.db_url != None
    assert isinstance(settings.db_url, str) is True
    assert len(settings.db_url) > 5
