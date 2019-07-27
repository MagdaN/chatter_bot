import pytest

from django.urls import reverse


@pytest.mark.parametrize('url_name', ['chat:home'])
def test_views(url_name, client):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == 200
