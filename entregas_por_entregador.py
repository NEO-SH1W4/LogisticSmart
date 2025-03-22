import pandas as pd
from datetime import datetime, timedelta
import os
import sys
import subprocess
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

COLUNA_DATA = 'Data prevista de entrega'
COLUNA_ENTREGADOR = 'Entregador'
PASTA = '.'

def encontrar_arquivo_excel_mais_recente(pasta=PASTA):
    arquivos = [f for f in os.listdir(pasta) if f.endswith('.xlsx')]
    print("\nArquivos .xlsx encontrados na pasta:")
    if not arquivos:
        print("Nenhum arquivo Excel encontrado.")
        return None
    for i, f in enumerate(arquivos, 1):
        print(f"{i}. {f}")
    arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(pasta, x)), reverse=True)
    return arquivos[0]

def carregar_dados(caminho_arquivo):
    try:
        return pd.read_excel(caminho_arquivo, sheet_name=0, engine='openpyxl')
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        sys.exit(1)

def validar_colunas(df):
    obrigatorias = [COLUNA_DATA, COLUNA_ENTREGADOR]
    for col in obrigatorias:
        if col not in df.columns:
            print(f"Coluna obrigatória ausente: {col}")
            sys.exit(1)

def agrupar_e_salvar(df, data_alvo):
    filtrado = df[df[COLUNA_DATA].dt.date == data_alvo]
    if filtrado.empty:
        print(f"Nenhuma entrega para {data_alvo.strftime('%d/%m/%Y')}")
        return

    agrupado = (
        filtrado[COLUNA_ENTREGADOR]
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Entregador', COLUNA_ENTREGADOR: 'Quantidade'})
    )

    nome_saida = f'entregas_agrupadas_{data_alvo.strftime("%d-%m")}.xlsx'
    agrupado.to_excel(nome_saida, index=False)
    caminho = os.path.abspath(nome_saida)
    print(f"Relatório gerado: {caminho}")

    # Abre a pasta com o arquivo selecionado
    subprocess.run(f'explorer /select,"{caminho}"')

def main():
    print("Relatório de Entregas por Entregador (Multidata)")
    arquivo = encontrar_arquivo_excel_mais_recente()
    if not arquivo:
        sys.exit(1)

    print(f"Arquivo selecionado: {arquivo}")
    df = carregar_dados(arquivo)
    validar_colunas(df)

    # Converte a coluna de data
    df[COLUNA_DATA] = pd.to_datetime(df[COLUNA_DATA], errors='coerce')

    # Datas a serem processadas
    hoje = datetime.now().date()
    ontem = hoje - timedelta(days=1)
    amanha = hoje + timedelta(days=1)

    for data in [ontem, hoje, amanha]:
        print(f"\nProcessando entregas para: {data.strftime('%d/%m/%Y')}")
        agrupar_e_salvar(df, data)

if __name__ == "__main__":
    main()
