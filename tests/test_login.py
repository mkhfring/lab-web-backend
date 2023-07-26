
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
        data=json.dumps({'email':'khajezade.mohamad@gmail.com', 'password':'Mkh10594'}),
        headers={'Content-Type': 'application/json'}
    )
    assert token_request.json['access_token'] is not None
    
def test_members_list(test_client):
    """
    GIVEN POST /api/v1/update/offline
    WHEN a zip file is attached
    THEN status shoud be 200
    """
    members_request = test_client.get(
        'apiv1/members',
        headers={'Content-Type': 'application/json'}
    )
    assert members_request.json is not None
    assert len(members_request.json) > 1
