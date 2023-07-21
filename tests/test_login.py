
import os
import zipfile
import json

from werkzeug.datastructures import FileStorage


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def test_login(test_client):
    """
    GIVEN POST /api/v1/update/offline
    WHEN a zip file is attached
    THEN status shoud be 200
    """
    token_request = test_client.post(
        'auth/login',
        data=json.dumps({'username':'example', 'password':'123456'}),
        headers={'Content-Type': 'application/json'}
    )
    assert token_request.json['access_token'] is not None
