

import bcrypt
from getpass import getpass
from db_connector import executar_consulta  


LOGGED_IN = False

def hash_password(password: str) -> str:
   
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def login_admin() -> bool:
   
    global LOGGED_IN
    print("=== LOGIN DO ADMINISTRADOR ===")
    usuario = input("Usuário: ")
    senha = getpass("Senha: ")

    sql = "SELECT senha FROM LOGINBD WHERE usuario = %s;"

    try:
        colunas, resultado = executar_consulta(sql, (usuario,), fetch=True)
        print(f"[DEBUG] Resultado da consulta: {resultado}")  # DEBUG
    except Exception as e:
        print(f"ERRO: Falha ao acessar o banco de dados. Detalhes: {e}")
        return False

    if not resultado:
        print("\n[DEBUG] Nenhum usuário encontrado no banco.\n")
        print("Credenciais inválidas. Acesso negado.\n")
        return False

    senha_hash_do_bd = resultado[0][0]
    print(f"[DEBUG] Hash do banco: {senha_hash_do_bd}")  # DEBUG

    if check_password(senha, senha_hash_do_bd):
        LOGGED_IN = True
        print("\nLogin realizado com sucesso! Acesso de administrador liberado.\n")
        return True

    print("\n[DEBUG] Senha digitada não confere com o hash.\n")
    print("Credenciais inválidas. Acesso negado.\n")
    return False

def logout_admin() -> None:
    """Realiza logout do administrador."""
    global LOGGED_IN
    LOGGED_IN = False
    print("Logout realizado com sucesso.")

def is_logged_in() -> bool:
    """Retorna status de login."""
    return LOGGED_IN


if __name__ == "__main__":
    login_admin()

