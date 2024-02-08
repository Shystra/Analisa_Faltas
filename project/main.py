import pandas as pd
import os

diretorio = "C:/Users/localuser/Documents/Lucas/Python/Trabalha Faltas"

dfs = []

for arquivo in os.listdir(diretorio):
    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
        caminho_completo = os.path.join(diretorio, arquivo)
        df = pd.read_excel(caminho_completo, sheet_name=1)
        dfs.append(df)

df_consolidado = pd.concat(dfs, ignore_index=True)
df_consolidado.columns = df_consolidado.columns.str.strip()
df_consolidado['Dia'] = pd.to_datetime(df_consolidado['Dia'], format='%d/%m/%y')



# print(df_consolidado.columns)
# print(df_consolidado)
# print(df_consolidado['Dia'].isna().sum())
# print(df_consolidado['Senha'])
# print(df_consolidado)


# exemplo_df = df_consolidado[df_consolidado['Senha'] == 517465].sort_values(by='Dia')
# print(exemplo_df[['Senha', 'Dia']])


def tem_faltas_consecutivas(grupo):
    # Converte as datas para o tipo datetime e extrai os períodos mensais
    grupo['Dia'] = pd.to_datetime(grupo['Dia'])
    meses = grupo['Dia'].dt.to_period('M').sort_values().unique()
    
    # Verifica se há atestados em pelo menos dois meses consecutivos, com um intervalo permitido de um mês
    meses_consecutivos = 0
    for i in range(len(meses) - 1):
        diferenca_mes = (meses[i + 1] - meses[i]).n
        
        # Se a diferença é de 1 mês, incrementa a contagem de meses consecutivos
        if diferenca_mes == 1:
            meses_consecutivos += 1
        # Se a diferença é maior que 1 mês, reinicia a contagem
        elif diferenca_mes > 1:
            meses_consecutivos = 0
        
        # Verifica se a contagem de meses consecutivos atende ao critério mínimo
        if meses_consecutivos >= 2:  # Tem pelo menos dois meses consecutivos (considerando o mês atual na contagem)
            return True
        
        
        if "FALTA" in grupo['Motivo'].values:
            dias_falta = grupo[grupo['Motivo'] == "FALTA"].shape[0]
            if dias_falta > 3:
            # Verifica se há mais de 3 dias de falta, independente da sequência de meses
                return True

    
    # Se não atender aos critérios após iterar por todos os meses, retorna False
    return False


def executar_analise(df_consolidado):
    # Lista de motivos aceitáveis
    motivos_validos = [
        'Atestado Médico',
        'Declaração de Comparecimento',
        'Dispensado pelo Contratante',
        'Falta 12x36 - Feriado',
        'Atestado de Acompanhamento',
        'Atestado Médico - COVID',
        'Licença Casamento',
        'Licença Paternidade',
        'Acompanhamento esposa gestante.',
        'Suspensão',
        'Dispensa Sindical',
        'Atestado de Comparecimento',
        'Doação de Sangue',
        'Declaração - Policia Civil',
        'FALTA'
    ]
    
    # Garante que 'Dia' está em formato datetime
    df_consolidado['Dia'] = pd.to_datetime(df_consolidado['Dia'])
    
    # Filtra o DataFrame para manter apenas os registros de 2023 e com motivos válidos
    df_filtrado = df_consolidado[
        ((df_consolidado['Dia'].dt.year == 2023) | (df_consolidado['Dia'].dt.year == 2024)) &
        (df_consolidado['Motivo'].isin(motivos_validos))
    ]
    
    # Aplica a lógica de faltas consecutivas no DataFrame filtrado
    resultado = df_filtrado.groupby('Senha').filter(tem_faltas_consecutivas)

    print("Segundo Resultado:")

    if not resultado.empty:
        print(resultado[['Senha', 'Funcionário', 'Motivo', 'Dia']])
        return resultado[['Senha', 'Funcionário', 'Motivo', 'Dia']]
    else:
        print("Nenhum registro encontrado para 2023 ou 2024 que atenda aos critérios.")
        return pd.DataFrame()



    







