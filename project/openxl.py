import pandas as pd
from main import executar_analise, df_consolidado

# Executa a análise para obter o DataFrame resultado
resultado_filtrado = executar_analise(df_consolidado)

# Especifica o caminho do arquivo Excel
caminho_arquivo_excel = "resultado_faltas_consecutivas.xlsx"

# Salva o DataFrame resultado em um arquivo Excel
if not resultado_filtrado.empty:
    resultado_filtrado.to_excel(caminho_arquivo_excel, index=False, engine='openpyxl')
    print(f"Arquivo Excel gerado com sucesso: {caminho_arquivo_excel}")
else:
    print("Nenhum dado para exportar.")
