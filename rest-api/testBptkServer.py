from application import bptk
from BPTK_Py.server import BptkServer
from flask import request, jsonify
import json
import requests
import pytest


@pytest.fixture
def app():
    flask_app = BptkServer(__name__, bptk)
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
        
def test_home_resource(app, client):
    response = client.get('/')
    assert response.status_code ==  200 
    assert response.data == b"<h1>BPTK-Py Simulation Service</h1>"
    
def test_run_resource(app, client):
    with open('tests_json_data/run.json') as json_file:
        json_data = json.load(json_file)
    response = client.post('/run', data=json.dumps(json_data), content_type = 'application/json')
    assert response.status_code == 200 # checking the status code
    
def test_scenarios_resource(app, client):
    response = client.get('/scenarios')
    assert response.status_code == 200 # checking the status code
    
def test_equations_resource(app, client):
    with open('tests_json_data/equations.json') as json_file:
        json_data = json.load(json_file)
    response = client.post('/equations', data=json.dumps(json_data), content_type = 'application/json')
    assert response.status_code == 200
    equations = [b"constants", b"converters", b"flows", b"points"]
    for equation in equations: # checking words in request data
        assert equation in response.data
    
def test_agents_resource(app, client):
    response = client.post('/agents', content_type = 'application/json')
    assert response.status_code == 400 # System dynmaics systems shouldn't have agents 
    
    
            
        
        

        
