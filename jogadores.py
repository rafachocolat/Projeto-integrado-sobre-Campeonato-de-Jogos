from db_connector import executar_consulta
from auth import is_logged_in
from tabulate import tabulate

def listar_jogadores():
    sql = "SELECT * FROM Jogadores;"
    colunas_res, resultados = executar_consulta(sql)
    
    if resultados:
        print("\n--- Listagem de Jogadores ---")
        # Adicionando o código do jogador para facilitar a exclusão/atualização
        sql_completo = "SELECT codigo_jogador, nome_jogador, idade, posicao, codigo_equipe FROM Jogadores;"
        colunas_res_completo, resultados_completo = executar_consulta(sql_completo)
        
        if resultados_completo:
            print(tabulate(resultados_completo, headers=['ID', 'Nome', 'Idade', 'Posição', 'ID Equipe'], tablefmt="fancy_grid"))
        else:
            print(tabulate(resultados, headers=colunas_res, tablefmt="fancy_grid"))
            
    elif resultados is not None:
        print("\nNenhum jogador encontrado.")

def inserir_jogador():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para inserir dados.")
        return
    nome = input("Nome do Jogador: ")
    idade = input("Idade: ")
    posicao = input("Posição: ")
    codigo_equipe = input("Código da Equipe (ID): ")
    
    sql = "INSERT INTO Jogadores (nome_jogador, idade, posicao, codigo_equipe) VALUES (%s, %s, %s, %s);"
    _, linhas_afetadas = executar_consulta(sql, (nome, idade, posicao, codigo_equipe), fetch=False)
    if linhas_afetadas is not None:
        print(f"\nJogador '{nome}' inserido com sucesso.")

def atualizar_jogador():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para atualizar dados.")
        return
    
    listar_jogadores()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) do jogador a ser atualizado: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    # Verifica se o jogador existe e pega os dados atuais
    sql_check = "SELECT nome_jogador, idade, posicao, codigo_equipe FROM Jogadores WHERE codigo_jogador = %s;"
    _, jogador_atual = executar_consulta(sql_check, (codigo,), fetch=True)
    
    if not jogador_atual:
        print(f"Erro: Nenhum jogador encontrado com o ID {codigo}.")
        return

    nome_atual, idade_atual, posicao_atual, equipe_atual = jogador_atual[0]

    print(f"\n--- Atualizando Jogador ID: {codigo} ---")
    
    novo_nome = input(f"Novo Nome do Jogador (atual: {nome_atual}, deixe em branco para manter): ")
    nova_idade = input(f"Nova Idade (atual: {idade_atual}, deixe em branco para manter): ")
    nova_posicao = input(f"Nova Posição (atual: {posicao_atual}, deixe em branco para manter): ")
    novo_codigo_equipe = input(f"Novo Código da Equipe (atual: {equipe_atual}, deixe em branco para manter): ")

    # Prepara a query de atualização
    updates = []
    params = []
    
    if novo_nome:
        updates.append("nome_jogador = %s")
        params.append(novo_nome)
    
    if nova_idade:
        updates.append("idade = %s")
        params.append(nova_idade)
        
    if nova_posicao:
        updates.append("posicao = %s")
        params.append(nova_posicao)
        
    if novo_codigo_equipe:
        updates.append("codigo_equipe = %s")
        params.append(novo_codigo_equipe)
        
    if not updates:
        print("Nenhuma alteração solicitada. Operação cancelada.")
        return

    sql = "UPDATE Jogadores SET " + ", ".join(updates) + " WHERE codigo_jogador = %s;"
    params.append(codigo)
    
    _, linhas_afetadas = executar_consulta(sql, tuple(params), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nJogador com ID {codigo} atualizado com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nNenhuma alteração feita no jogador com ID {codigo}.")
    else:
        print("\nErro ao tentar atualizar o jogador.")

def excluir_jogador():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para excluir dados.")
        return
    
    # Lista os jogadores para que o usuário possa ver os IDs
    listar_jogadores()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) do jogador a ser excluído: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    # Confirmação de exclusão
    confirmacao = input(f"Tem certeza que deseja excluir o jogador com ID {codigo}? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação de exclusão cancelada.")
        return

    sql = "DELETE FROM Jogadores WHERE codigo_jogador = %s;"
    _, linhas_afetadas = executar_consulta(sql, (codigo,), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nJogador com ID {codigo} excluído com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nErro: Nenhum jogador encontrado com o ID {codigo}.")
    else:
        print("\nErro ao tentar excluir o jogador.")
