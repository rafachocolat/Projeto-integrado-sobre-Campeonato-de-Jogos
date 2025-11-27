from db_connector import executar_consulta
from auth import is_logged_in
from tabulate import tabulate

def listar_jogos():
    sql = "SELECT * FROM Jogos;"
    colunas_res, resultados = executar_consulta(sql)
    
    if resultados:
        print("\n--- Listagem de Jogos ---")
        sql_completo = "SELECT codigo_jogo, data_jogo, hora_jogo, equipe_casa, equipe_visitante FROM Jogos;"
        colunas_res_completo, resultados_completo = executar_consulta(sql_completo)
        
        if resultados_completo:
            print(tabulate(resultados_completo, headers=['ID', 'Data', 'Hora', 'Equipe Casa (ID)', 'Equipe Visitante (ID)'], tablefmt="fancy_grid"))
        else:
            print(tabulate(resultados, headers=colunas_res, tablefmt="fancy_grid"))
            
    elif resultados is not None:
        print("\nNenhum jogo encontrado.")

def inserir_jogo():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para inserir dados.")
        return
    data = input("Data do Jogo (AAAA-MM-DD): ")
    hora = input("Hora do Jogo (HH:MM:SS): ")
    casa = input("Código da Equipe da Casa (ID): ")
    visitante = input("Código da Equipe Visitante (ID): ")
    
    sql = "INSERT INTO Jogos (data_jogo, hora_jogo, equipe_casa, equipe_visitante) VALUES (%s, %s, %s, %s);"
    _, linhas_afetadas = executar_consulta(sql, (data, hora, casa, visitante), fetch=False)
    if linhas_afetadas is not None:
        print(f"\nJogo inserido com sucesso.")

def atualizar_jogo():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para atualizar dados.")
        return
    
    listar_jogos()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) do jogo a ser atualizado: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    sql_check = "SELECT data_jogo, hora_jogo, equipe_casa, equipe_visitante FROM Jogos WHERE codigo_jogo = %s;"
    _, jogo_atual = executar_consulta(sql_check, (codigo,), fetch=True)
    
    if not jogo_atual:
        print(f"Erro: Nenhum jogo encontrado com o ID {codigo}.")
        return

    data_atual, hora_atual, casa_atual, visitante_atual = jogo_atual[0]

    print(f"\n--- Atualizando Jogo ID: {codigo} ---")
    
    nova_data = input(f"Nova Data do Jogo (atual: {data_atual}, deixe em branco para manter): ")
    nova_hora = input(f"Nova Hora do Jogo (atual: {hora_atual}, deixe em branco para manter): ")
    nova_casa = input(f"Novo Código da Equipe da Casa (atual: {casa_atual}, deixe em branco para manter): ")
    nova_visitante = input(f"Novo Código da Equipe Visitante (atual: {visitante_atual}, deixe em branco para manter): ")

    updates = []
    params = []
    
    if nova_data:
        updates.append("data_jogo = %s")
        params.append(nova_data)
    
    if nova_hora:
        updates.append("hora_jogo = %s")
        params.append(nova_hora)
        
    if nova_casa:
        updates.append("equipe_casa = %s")
        params.append(nova_casa)
        
    if nova_visitante:
        updates.append("equipe_visitante = %s")
        params.append(nova_visitante)
        
    if not updates:
        print("Nenhuma alteração solicitada. Operação cancelada.")
        return

    sql = "UPDATE Jogos SET " + ", ".join(updates) + " WHERE codigo_jogo = %s;"
    params.append(codigo)
    
    _, linhas_afetadas = executar_consulta(sql, tuple(params), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nJogo com ID {codigo} atualizado com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nNenhuma alteração feita no jogo com ID {codigo}.")
    else:
        print("\nErro ao tentar atualizar o jogo.")

def excluir_jogo():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para excluir dados.")
        return
    
    listar_jogos()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) do jogo a ser excluído: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    confirmacao = input(f"Tem certeza que deseja excluir o jogo com ID {codigo}? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação de exclusão cancelada.")
        return

    sql = "DELETE FROM Jogos WHERE codigo_jogo = %s;"
    _, linhas_afetadas = executar_consulta(sql, (codigo,), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nJogo com ID {codigo} excluído com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nErro: Nenhum jogo encontrado com o ID {codigo}.")
    else:
        print("\nErro ao tentar excluir o jogo.")

