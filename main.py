import getpass
from db_connector import executar_consulta 
from auth import is_logged_in, login_admin, logout_admin
from equipes import excluir_equipe, atualizar_equipe
from jogadores import excluir_jogador, atualizar_jogador
from jogos import excluir_jogo, atualizar_jogo
from resultados import excluir_resultado, atualizar_resultado 






def get_equipe_id_by_name(nome_equipe): 
    query = "SELECT codigo_equipe FROM Equipes WHERE nome_equipe = %s;"
    colunas, resultado = executar_consulta(query, (nome_equipe,), fetch=True)
    if resultado:
        return resultado[0][0]
    return None

def cadastrar_equipe():
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
        
    print("\n--- CADASTRO DE EQUIPE ---")
    nome_equipe = input("Nome da Equipe: ")
    cidade = input("Cidade da Equipe: ")
    
    query = "INSERT INTO Equipes (nome_equipe, cidade) VALUES (%s, %s);"
    colunas, rowcount = executar_consulta(query, (nome_equipe, cidade), fetch=False)
    
    if rowcount and rowcount > 0:
        print(f"Equipe '{nome_equipe}' de {cidade} cadastrada com sucesso.")
    else:
        print(f"Erro ao cadastrar a equipe '{nome_equipe}' de {cidade}.")

def listar_jogadores():
    print("\n--- LISTA DE JOGADORES ---")
    
    query = """
        SELECT 
            J.nome_jogador, 
            J.idade, 
            J.posicao, 
            E.nome_equipe
        FROM Jogadores J
        JOIN Equipes E ON J.codigo_equipe = E.codigo_equipe
        ORDER BY E.nome_equipe, J.nome_jogador;
    """
    colunas, jogadores = executar_consulta(query, fetch=True)

    if jogadores:
        print(" | ".join(["Nome do Jogador", "Idade", "Posição", "Equipe"]))
        print("-" * 80)
        for jogador in jogadores:
            print(f"{jogador[0]:<20} | {jogador[1]:<5} | {jogador[2]:<15} | {jogador[3]}")
    else:
        print("Nenhum jogador cadastrado.")

def listar_equipes():
    print("\n--- LISTA DE EQUIPES ---")
    
    query = "SELECT nome_equipe, cidade FROM Equipes ORDER BY nome_equipe;"
    colunas, equipes = executar_consulta(query, fetch=True)

    if equipes:
        for i, equipe in enumerate(equipes, 1):
            print(f"{i}. {equipe[0]} ({equipe[1]})")
    else:
        print("Nenhuma equipe cadastrada.")

def cadastrar_jogo():
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
        
    print("\n--- CADASTRO DE JOGO ---")
    
 
    nome_equipe1 = input("Nome da Equipe Casa: ")
    nome_equipe2 = input("Nome da Equipe Visitante: ")
    data_jogo = input("Data do Jogo (AAAA-MM-DD): ")
    hora_jogo = input("Hora do Jogo (HH:MM): ")

 
    id_equipe1 = get_equipe_id_by_name(nome_equipe1)
    id_equipe2 = get_equipe_id_by_name(nome_equipe2)

    if not id_equipe1 or not id_equipe2:
        print("Erro: Uma ou ambas as equipes não foram encontradas no banco de dados. Certifique-se de que o nome está correto.")
        return


    query = "INSERT INTO Jogos (data_jogo, hora_jogo, equipe_casa, equipe_visitante) VALUES (%s, %s, %s, %s);"
    colunas, rowcount = executar_consulta(query, (data_jogo, hora_jogo, id_equipe1, id_equipe2), fetch=False)
    
    if rowcount and rowcount > 0:
        print(f"Jogo entre {nome_equipe1} e {nome_equipe2} cadastrado com sucesso.")
    else:
        print(f"Erro ao cadastrar o jogo.")
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
        
    print("\n--- CADASTRO DE JOGO ---")
    

    equipe1 = input("Nome da Equipe 1: ")
    equipe2 = input("Nome da Equipe 2: ")
    data_jogo = input("Data do Jogo (AAAA-MM-DD): ")
    
    query = "INSERT INTO JOGOS (equipe1, equipe2, data_jogo) VALUES (%s, %s, %s);"
    colunas, rowcount = executar_consulta(query, (equipe1, equipe2, data_jogo), fetch=False)
    
    if rowcount and rowcount > 0:
        print(f"Jogo entre {equipe1} e {equipe2} cadastrado com sucesso.")
    else:
        print(f"Erro ao cadastrar o jogo.")

def listar_resultados():
    print("\n--- LISTA DE RESULTADOS ---")
    
    query = """
        SELECT 
            R.codigo_resultado,
            J.data_jogo, 
            E_CASA.nome_equipe AS equipe_casa, 
            E_VISITANTE.nome_equipe AS equipe_visitante,
            R.placar_equipe_casa,
            R.placar_equipe_visitante,
            E_VENCEDOR.nome_equipe AS vencedor
        FROM Resultados R
        JOIN Jogos J ON R.codigo_jogo = J.codigo_jogo
        JOIN Equipes E_CASA ON J.equipe_casa = E_CASA.codigo_equipe
        JOIN Equipes E_VISITANTE ON J.equipe_visitante = E_VISITANTE.codigo_equipe
        LEFT JOIN Equipes E_VENCEDOR ON R.equipe_vencedora = E_VENCEDOR.codigo_equipe
        ORDER BY J.data_jogo DESC;
    """
    colunas, resultados = executar_consulta(query, fetch=True)

    if resultados:
        print(" | ".join(["ID", "Data", "Jogo", "Placar", "Vencedor"]))
        print("-" * 80)
        for res in resultados:
            id_res, data, casa, visitante, placar_casa, placar_visitante, vencedor = res
            jogo_str = f"{casa} vs {visitante}"
            placar_str = f"{placar_casa} x {placar_visitante}"
            vencedor_str = vencedor if vencedor else "Empate"
            print(f"{id_res:<2} | {data} | {jogo_str:<30} | {placar_str:<10} | {vencedor_str}")
    else:
        print("Nenhum resultado cadastrado.")

def listar_jogos():
    print("\n--- LISTA DE JOGOS ---")
    
    query = """
        SELECT 
            J.data_jogo, 
            J.hora_jogo, 
            E1.nome_equipe AS equipe_casa, 
            E2.nome_equipe AS equipe_visitante
        FROM Jogos J
        JOIN Equipes E1 ON J.equipe_casa = E1.codigo_equipe
        JOIN Equipes E2 ON J.equipe_visitante = E2.codigo_equipe
        ORDER BY J.data_jogo, J.hora_jogo;
    """
    colunas, jogos = executar_consulta(query, fetch=True)

    if jogos:
        for i, jogo in enumerate(jogos, 1):
            print(f"{i}. {jogo[2]} (Casa) vs {jogo[3]} (Visitante) em {jogo[0]} às {jogo[1]}")
    else:
        print("Nenhum jogo cadastrado.")


def inserir_novo_jogador():
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
    
    print("\n--- INSERIR NOVO JOGADOR (ADMIN) ---")
    nome_jogador = input("Nome do Jogador: ")
    idade = input("Idade: ")
    posicao = input("Posição: ")
    nome_equipe = input("Nome da Equipe: ")

    id_equipe = get_equipe_id_by_name(nome_equipe)

    if not id_equipe:
        print(f"Erro: Equipe '{nome_equipe}' não encontrada. Certifique-se de que o nome está correto.")
        return

    query = "INSERT INTO Jogadores (nome_jogador, idade, posicao, codigo_equipe) VALUES (%s, %s, %s, %s);"
    colunas, rowcount = executar_consulta(query, (nome_jogador, idade, posicao, id_equipe), fetch=False)

    if rowcount and rowcount > 0:
        print(f"Jogador '{nome_jogador}' cadastrado com sucesso na equipe '{nome_equipe}'.")
    else:
        print(f"Erro ao cadastrar o jogador.")
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
    print("\n--- INSERIR NOVO JOGADOR (ADMIN) ---")

def inserir_novo_resultado():
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
    
    print("\n--- INSERIR NOVO RESULTADO (ADMIN) ---")
    
    codigo_jogo = input("Código do Jogo (ID): ")
    placar_casa = input("Placar da Equipe Casa: ")
    placar_visitante = input("Placar da Equipe Visitante: ")

    query_jogo = "SELECT equipe_casa, equipe_visitante FROM Jogos WHERE codigo_jogo = %s;"
    colunas, resultado_jogo = executar_consulta(query_jogo, (codigo_jogo,), fetch=True)

    if not resultado_jogo:
        print(f"Erro: Jogo com código {codigo_jogo} não encontrado.")
        return

    id_casa = resultado_jogo[0][0]
    id_visitante = resultado_jogo[0][1]

    vencedor_id = None
    perdedor_id = None
    if int(placar_casa) > int(placar_visitante):
        vencedor_id = id_casa
        perdedor_id = id_visitante
    elif int(placar_visitante) > int(placar_casa):
        vencedor_id = id_visitante
        perdedor_id = id_casa
    query = """
        INSERT INTO Resultados (
            codigo_jogo, equipe_vencedora, equipe_perdedora, 
            placar_equipe_casa, placar_equipe_visitante
        ) VALUES (%s, %s, %s, %s, %s);
    """
    params = (codigo_jogo, vencedor_id, perdedor_id, placar_casa, placar_visitante)
    colunas, rowcount = executar_consulta(query, params, fetch=False)

    if rowcount and rowcount > 0:
        print(f"Resultado para o Jogo {codigo_jogo} cadastrado com sucesso.")
    else:
        print(f"Erro ao cadastrar o resultado.")
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para inserir dados.")
        return
    print("\n--- INSERIR NOVO RESULTADO (ADMIN) ---")


def executar_consulta_sql():
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para executar consultas.")
        return
    print("\n--- EXECUTAR CONSULTA SQL (ADMIN) ---")
    consulta = input("Digite a consulta SQL (SELECT): ")
    colunas, resultados = executar_consulta(consulta, fetch=True)
    
    if resultados:
        print("\n--- RESULTADOS ---")
        print(" | ".join(colunas))
        print("-" * (sum(len(c) for c in colunas) + len(colunas) * 3))
        for linha in resultados:
            print(" | ".join(str(item) for item in linha))
    elif colunas is not None:
        print("Consulta executada com sucesso. Nenhuma linha retornada.")
    else:
        print("Erro na execução da consulta.")
    if not is_logged_in():
        print("Acesso negado. Faça login como administrador para executar consultas.")
        return
    print("\n--- EXECUTAR CONSULTA SQL (ADMIN) ---")


def menu_principal():
    """Menu principal do sistema de gerenciamento de campeonato."""
    while True:
        print("\n==========================================================")
        print("MINI-SISTEMA DE GERENCIAMENTO ESPORTIVO")
        
        if is_logged_in():
            print("(ACESSO ADMINISTRATIVO COMPLETO)")
        else:
            print("(ACESSO RESTRITO - FAÇA LOGIN)")
            
        print("==========================================================")
        print("1. Listar Equipes")
        print("2. Listar Jogadores")
        print("3. Listar Jogos")
        print("4. Listar Resultados")
        print("5. Cadastrar Nova Equipe (Admin)")
        print("6. Cadastrar Novo Jogo (Admin)")
        print("7. Inserir Novo Jogador (Admin)")
        print("8. Inserir Novo Resultado (Admin)")
        print("9. Atualizar Equipe (Admin)")
        print("10. Atualizar Jogador (Admin)")
        print("11. Atualizar Jogo (Admin)")
        print("12. Atualizar Resultado (Admin)")
        print("13. Excluir Equipe (Admin)")
        print("14. Excluir Jogador (Admin)")
        print("15. Excluir Jogo (Admin)")
        print("16. Excluir Resultado (Admin)")
        
        if is_logged_in():
            print("A. Logout de Administrador")
        else:
            print("A. Login de Administrador")
            
        print("0. Sair")
        print("----------------------------------------------------------")
        
        escolha = input("Escolha uma opção: ").upper()
        
        if escolha == '1':
            listar_equipes()
        elif escolha == '2':
            listar_jogadores()
        elif escolha == '3':
            listar_jogos()
        elif escolha == '4':
            listar_resultados()
        elif escolha == '5':
            cadastrar_equipe() 
        elif escolha == '6':
            cadastrar_jogo() 
        elif escolha == '7':
            inserir_novo_jogador()
        elif escolha == '8':
            inserir_novo_resultado() 
        elif escolha == '9':
            atualizar_equipe() 
        elif escolha == '10':
            atualizar_jogador() 
        elif escolha == '11':
            atualizar_jogo() 
        elif escolha == '12':
            atualizar_resultado() 
        elif escolha == '13':
            excluir_equipe() 
        elif escolha == '14':
            excluir_jogador() 
        elif escolha == '15':
            excluir_jogo() 
        elif escolha == '16':
            executar_consulta_sql() 
        elif escolha == 'A':
            if is_logged_in():
                logout_admin()
            else:
                login_admin()
        elif escolha == '0':
            print("\nSaindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


def iniciar_sistema():
    menu_principal()

if __name__ == "__main__":
    iniciar_sistema()


