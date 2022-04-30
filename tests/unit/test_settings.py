import urllib

from app.settings import Settings


def test_settings_url_generate():
    mongo_host = "0.0.0.0"
    mongo_port = 2020
    mongo_user = "test"
    mongo_password = "testpass"
    settings = Settings(
        host="str",
        port=1,
        service_name="sbf-challenge",
        workers_count=1,
        reload=True,
        currency_api_url="str",
        mongo_host=mongo_host,
        mongo_port=mongo_port,
        mongo_user=mongo_user,
        mongo_password=mongo_password,
        mongo_max_connections_count=1,
        mongo_min_connections_count=1,
    )
    assert (
        settings.mongo_url()
        == f"mongodb://{mongo_user}:\
            {urllib.parse.quote(mongo_password)}\
                @{mongo_host}:\
                    {mongo_port}/sbf_challenge"
    )
