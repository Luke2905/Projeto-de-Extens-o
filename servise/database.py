# database.py

import mysql.connector
from mysql.connector import Error
import os # Vamos usar para pegar as credenciais do ambiente
from contextlib import contextmanager

# Dica de Arquiteto: Use variáveis de ambiente!
# É mais seguro do que deixar a senha "chumbada" no código.
# Configure isso no seu sistema ou num arquivo .env
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'sgp_producao')
DB_USER = os.getenv('DB_USER', 'root')
#DB_PASS = os.getenv('DB_PASS', '1234')

@contextmanager
def get_conexao():

    conexao = None # Começa nula
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            #password=DB_PASS
        )

        yield conexao 
        
    except Error as e:
        print(f"Erro durante a conexão ou transação: {e}")
        # Se der erro, podemos forçar um rollback aqui
        if conexao:
            conexao.rollback()
    finally:
        # Quando o bloco 'with' termina (com sucesso ou erro),
        # o código volta para cá e o 'finally' é executado.
        if conexao and conexao.is_connected():
            conexao.close()
            # print("Conexão com o MySQL foi fechada.") # Opcional