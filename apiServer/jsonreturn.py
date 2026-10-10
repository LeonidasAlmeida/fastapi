import datetime
import pytest
from fastapi.encoders import jsonable_encoder
import json

@pytest.fixture #prepara os dados para serem testados
def data():
    return datetime.datetime.now() #data hora

def test_json_dump(data):
    with pytest.raises(Exception):
        _= json.dumps(data)
        
def test_encoder(data):
    out = jsonable_encoder(data)
    assert out
    json_out = json.dumps(out)
    assert json_out
