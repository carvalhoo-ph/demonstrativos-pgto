import json
import pytest
from lambda_function import lambda_handler

def test_lambda_handler_success(mocker):
    event = {
        'queryStringParameters': {
            'cpf': '12345678900',
            'ANO': '2023',
            'MES': '10'
        }
    }
    
    mocker.patch('pymysql.connect')
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = (1000.00, 'base64string')
    mock_connection.cursor.return_value = mock_cursor
    pymysql.connect.return_value = mock_connection

    response = lambda_handler(event, None)
    body = json.loads(response['body'])

    assert response['statusCode'] == 200
    assert body['valor_total'] == 1000.00
    assert body['arquivo_base64'] == 'base64string'

def test_lambda_handler_no_record(mocker):
    event = {
        'queryStringParameters': {
            'cpf': '12345678900',
            'ANO': '2023',
            'MES': '10'
        }
    }
    
    mocker.patch('pymysql.connect')
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = None
    mock_connection.cursor.return_value = mock_cursor
    pymysql.connect.return_value = mock_connection

    response = lambda_handler(event, None)
    body = json.loads(response['body'])

    assert response['statusCode'] == 404
    assert body == 'Registro não encontrado'

def test_lambda_handler_missing_parameters():
    event = {
        'queryStringParameters': {
            'cpf': '12345678900'
        }
    }

    response = lambda_handler(event, None)
    body = json.loads(response['body'])

    assert response['statusCode'] == 400
    assert body == 'CPF, ANO ou MES não fornecido'
