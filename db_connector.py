import psycopg2
from psycopg2 import Error

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "PAIN2015"
DB_PORT = "5432"

def executar_consulta(sql_query, params=None, fetch=True):
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT, client_encoding='utf8')
        cur = conn.cursor()
        cur.execute(sql_query, params)
        
        if fetch and sql_query.strip().upper().startswith("SELECT"):
            colunas = [desc[0] for desc in cur.description]
            resultados = cur.fetchall()
            return colunas, resultados
        
        conn.commit()
        return None, cur.rowcount

    except (Exception, Error) as error:
        print(f"\n--- ERRO ---")
        print(f"Erro ao executar a consulta: {error}")
        print("------------\n")
        return None, None
        
    finally:
        if conn:
            conn.close()
