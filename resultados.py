from db_connector import executar_consulta
from auth import is_logged_in
from tabulate import tabulate

def listar_resultados():
    sql = "SELECT * FROM Resultados;"
    colunas_res, resultados = executar_consulta(sql)
    
    if resultados:
        print("\n--- Listagem de Resultados ---")
        sql_completo = "SELECT codigo_resultado, codigo_jogo, equipe_vencedora, equipe_perdedora, placar_equipe_casa, placar_equipe_visitante FROM Resultados;"
        colunas_res_completo, resultados_completo = executar_consulta(sql_completo)
        
        if resultados_completo:
            print(tabulate(resultados_completo, headers=['ID Resultado', 'ID Jogo', 'Vencedor (ID)', 'Perdedor (ID)', 'Placar Casa', 'Placar Visitante'], tablefmt="fancy_grid"))
        else:
            print(tabulate(resultados, headers=colunas_res, tablefmt="fancy_grid"))
            
    elif resultados is not None:
        print("\nNenhum resultado encontrado.")

def inserir_resultado():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para inserir dados.")
        return
    jogo = input("Código do Jogo (ID): ")
    vencedora = input("Código da Equipe Vencedora (ID, ou deixe em branco se for empate): ")
    perdedora = input("Código da Equipe Perdedora (ID, ou deixe em branco se for empate): ")
    placar_casa = input("Placar da Equipe da Casa: ")
    placar_visitante = input("Placar da Equipe Visitante: ")
    
    vencedora = vencedora if vencedora.strip() else None
    perdedora = perdedora if perdedora.strip() else None
    
    sql = "INSERT INTO Resultados (codigo_jogo, equipe_vencedora, equipe_perdedora, placar_equipe_casa, placar_equipe_visitante) VALUES (%s, %s, %s, %s, %s);"
    _, linhas_afetadas = executar_consulta(sql, (jogo, vencedora, perdedora, placar_casa, placar_visitante), fetch=False)
    if linhas_afetadas is not None:
        print(f"\nResultado do Jogo {jogo} inserido com sucesso.")

def atualizar_resultado():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para atualizar dados.")
        return
    
    listar_resultados()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) do resultado a ser atualizado: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    sql_check = "SELECT codigo_jogo, equipe_vencedora, equipe_perdedora, placar_equipe_casa, placar_equipe_visitante FROM Resultados WHERE codigo_resultado = %s;"
    _, resultado_atual = executar_consulta(sql_check, (codigo,), fetch=True)
    
    if not resultado_atual:
        print(f"Erro: Nenhum resultado encontrado com o ID {codigo}.")
        return

    jogo_atual, vencedor_atual, perdedor_atual, placar_casa_atual, placar_visitante_atual = resultado_atual[0]

    print(f"\n--- Atualizando Resultado ID: {codigo} ---")
    
    novo_jogo = input(f"Novo Código do Jogo (atual: {jogo_atual}, deixe em branco para manter): ")
    novo_vencedor = input(f"Novo Código da Equipe Vencedora (atual: {vencedor_atual if vencedor_atual else 'N/A'}, deixe em branco para manter): ")
    novo_perdedor = input(f"Novo Código da Equipe Perdedora (atual: {perdedor_atual if perdedor_atual else 'N/A'}, deixe em branco para manter): ")
    novo_placar_casa = input(f"Novo Placar da Equipe Casa (atual: {placar_casa_atual}, deixe em branco para manter): ")
    novo_placar_visitante = input(f"Novo Placar da Equipe Visitante (atual: {placar_visitante_atual}, deixe em branco para manter): ")

    vencedor_final = novo_vencedor if novo_vencedor else vencedor_atual
    perdedor_final = novo_perdedor if novo_perdedor else perdedor_atual
    
    if not novo_vencedor and not novo_perdedor:
        pass
    elif novo_vencedor.strip() == "" and novo_perdedor.strip() == "":
        vencedor_final = None
        perdedor_final = None
    else:
        vencedor_final = novo_vencedor if novo_vencedor.strip() else None
        perdedor_final = novo_perdedor if novo_perdedor.strip() else None



    updates = []
    params = []
    
    if novo_jogo:
        updates.append("codigo_jogo = %s")
        params.append(novo_jogo)
    
   
    if novo_vencedor or vencedor_final is None:
        updates.append("equipe_vencedora = %s")
        params.append(vencedor_final)
        
    if novo_perdedor or perdedor_final is None:
        updates.append("equipe_perdedora = %s")
        params.append(perdedor_final)
        
    if novo_placar_casa:
        updates.append("placar_equipe_casa = %s")
        params.append(novo_placar_casa)
        
    if novo_placar_visitante:
        updates.append("placar_equipe_visitante = %s")
        params.append(novo_placar_visitante)
        
    if not updates:
        print("Nenhuma alteração solicitada. Operação cancelada.")
        return

    sql = "UPDATE Resultados SET " + ", ".join(updates) + " WHERE codigo_resultado = %s;"
    params.append(codigo)
    
    _, linhas_afetadas = executar_consulta(sql, tuple(params), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nResultado com ID {codigo} atualizado com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nNenhuma alteração feita no resultado com ID {codigo}.")
    else:
        print("\nErro ao tentar atualizar o resultado.")

def excluir_resultado():
    if not is_logged_in():
        print("\nAcesso negado. Faça login como administrador para excluir dados.")
        return
    
   
    listar_resultados()
    
    try:
        codigo = int(input("Digite o CÓDIGO (ID) do resultado a ser excluído: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

   
    confirmacao = input(f"Tem certeza que deseja excluir o resultado com ID {codigo}? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação de exclusão cancelada.")
        return

    sql = "DELETE FROM Resultados WHERE codigo_resultado = %s;"
    _, linhas_afetadas = executar_consulta(sql, (codigo,), fetch=False)
    
    if linhas_afetadas is not None and linhas_afetadas > 0:
        print(f"\nResultado com ID {codigo} excluído com sucesso.")
    elif linhas_afetadas == 0:
        print(f"\nErro: Nenhum resultado encontrado com o ID {codigo}.")
    else:
        print("\nErro ao tentar excluir o resultado.")

