import psycopg2
import config

def test_connection():
    try:
        connection = psycopg2.connect(
            host=config.rds_host,
            user=config.db_username,
            password=config.db_password,
            dbname=config.db_name,
            connect_timeout=10  # Adicione um timeout para a conexão
        )
        print("Conexão bem-sucedida!")
        connection.close()
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    test_connection()
