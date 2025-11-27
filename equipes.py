from db_connector import executar_consulta
from auth import is_logged_in
from tabulate import tabulate

def listar_equipes():
    sql = "SELECT * FROM Equipes;"
    colunas_res, resultados = executar_consulta(sql)
    
    if resultados:
        print("\n--- Listagem de Equipes ---")
        print(tabulate(resultados, headers=colunas_res, tablefmt="fancy_grid"))
    elif resultados is not None:
        print("\nNenhuma equipe encontrada.")

def inserir_equipe():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para inserir dados.")
        return
    nome = input("Nome da Equipe: ")
    cidade = input("Cidade: ")
    sql = "INSERT INTO Equipes (nome_equipe, cidade) VALUES (%s, %s);"
    _, linhas_afetadas = executar_consulta(sql, (nome, cidade), fetch=False)
    if linhas_afetadas is not None:
        print(f"\nEquipe '{nome}' inserida com sucesso.")

def atualizar_equipe():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para atualizar dados.")
        return
    
    listar_equipes()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) da equipe a ser atualizada: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

  
    sql_check = "SELECT nome_equipe, cidade FROM Equipes WHERE codigo_equipe = %s;"
    _, equipe_atual = executar_consulta(sql_check, (codigo,), fetch=True)
    
    if not equipe_atual:
        print(f"Erro: Nenhuma equipe encontrada com o ID {codigo}.")
        return

    print(f"\n--- Atualizando Equipe ID: {codigo} ---")
    print(f"Nome atual: {equipe_atual[0][0]}")
    novo_nome = input(f"Novo Nome da Equipe (deixe em branco para manter '{equipe_atual[0][0]}'): ")
    print(f"Cidade atual: {equipe_atual[0][1]}")
    nova_cidade = input(f"Nova Cidade (deixe em branco para manter '{equipe_atual[0][1]}'): ")

    
    updates = []
    params = []
    
    if novo_nome:
        updates.append("nome_equipe = %s")
        params.append(novo_nome)
    
    if nova_cidade:
        updates.append("cidade = %s")
        params.append(nova_cidade)
        
    if not updates:
        print("Nenhuma alteração solicitada. Operação cancelada.")
        return

    sql = "UPDATE Equipes SET " + ", ".join(updates) + " WHERE codigo_equipe = %s;"
    params.append(codigo)
    
    _, linhas_afetadas = executar_consulta(sql, tuple(params), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nEquipe com ID {codigo} atualizada com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nNenhuma alteração feita na equipe com ID {codigo}.")
    else:
        print("\nErro ao tentar atualizar a equipe.")

def excluir_equipe():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para excluir dados.")
        return
    
    listar_equipes()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) da equipe a ser excluída: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

  
    confirmacao = input(f"Tem certeza que deseja excluir a equipe com ID {codigo}? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação de exclusão cancelada.")
        return

    sql = "DELETE FROM Equipes WHERE codigo_equipe = %s;"
    _, linhas_afetadas = executar_consulta(sql, (codigo,), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nEquipe com ID {codigo} excluída com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nErro: Nenhuma equipe encontrada com o ID {codigo}.")
    else:
        print("\nErro ao tentar excluir a equipe.")

