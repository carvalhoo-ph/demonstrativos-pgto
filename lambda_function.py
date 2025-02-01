import json
import psycopg2
import os
import config

def lambda_handler(event, context):
    # Obter o CPF, ANO e MES dos parâmetros de consulta
    cpf = event.get('queryStringParameters', {}).get('cpf')
    ano = event.get('queryStringParameters', {}).get('ano')
    mes = event.get('queryStringParameters', {}).get('mes')
    
    print(f"CPF: {cpf}")
    print(f"ANO: {ano}")
    print(f"MES: {mes}")
    
    if not cpf or not ano or not mes:
        return {
            'statusCode': 400,
            'body': json.dumps('CPF, ANO ou MES não fornecido')
        }

    try:
        print(f"Tentando conectar ao banco de dados: {config.rds_host}")
        # Conexão com o banco de dados
        connection = psycopg2.connect(
            host=config.rds_host,
            user=config.db_username,
            password=config.db_password,
            dbname=config.db_name,
            connect_timeout=10  # Adicione um timeout para a conexão
        )
        print("Conexão com o banco de dados bem-sucedida")

        with connection.cursor() as cursor:
            # Buscar os dados na tabela demonstrativos_pagamento
            sql = """
                SELECT valor_total, arquivo_base64
                FROM demonstrativos_pagamento dp
                JOIN ex_funcionarios ef ON dp.ex_funcionario_id = ef.id
                WHERE ef.cpf = %s AND dp.ano = %s AND dp.mes = %s
            """
            cursor.execute(sql, (cpf, ano, mes))
            result = cursor.fetchone()

            if result:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'valor_total': result[0],
                        'arquivo_base64': result[1]
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps('Registro não encontrado')
                }
    except Exception as e:
        print(f'Erro no servidor: {str(e)}')  # Adicione este log para capturar a exceção
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro no servidor: {str(e)}')
        }
    finally:
        if 'connection' in locals():
            connection.close()
