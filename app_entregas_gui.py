import warnings
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Button, Combobox
from tkcalendar import DateEntry
import os 

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Button, Combobox
from tkcalendar import DateEntry
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def encontrar_arquivo_excel_mais_recente(pasta='.'):
    arquivos = [f for f in os.listdir(pasta) if f.endswith('.xlsx')]
    if not arquivos:
        return None
    arquivos.sort(key=lambda f: os.path.getmtime(os.path.join(pasta, f)), reverse=True)
    return arquivos[0]

def agrupar_e_salvar(df, data_alvo, filtros):
    df_filtrado = df[df['Data prevista de entrega'].dt.date == data_alvo]

    for coluna, valor in filtros.items():
        if valor and valor != "Todos" and coluna in df.columns:
            df_filtrado = df_filtrado[df_filtrado[coluna] == valor]

    if df_filtrado.empty:
        messagebox.showinfo("Sem entregas", "Nenhuma entrega encontrada para os filtros selecionados.")
        return

    resultado = (
        df_filtrado['Entregador']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Entregador', 'Entregador': 'Quantidade'})
    )

    nome_saida = f'entregas_agrupadas_{data_alvo.strftime("%d-%m")}.xlsx'
    resultado.to_excel(nome_saida, index=False)
    messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso:\n{nome_saida}")
    os.startfile(os.path.abspath(nome_saida))

def gerar_relatorio(data_opcao):
    arquivo = encontrar_arquivo_excel_mais_recente()
    if not arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo .xlsx encontrado.")
        return

    try:
        df = pd.read_excel(arquivo, sheet_name=0, engine='openpyxl')
        df['Data prevista de entrega'] = pd.to_datetime(df['Data prevista de entrega'], errors='coerce')

        if data_opcao == "Ontem":
            data = datetime.now().date() - timedelta(days=1)
        elif data_opcao == "Hoje":
            data = datetime.now().date()
        elif data_opcao == "Amanhã":
            data = datetime.now().date() + timedelta(days=1)
        else:
            data = cal.get_date()

        filtros = {
            'Status': status_combo.get() if 'Status' in df.columns else None,
            'Cidade': cidade_combo.get() if 'Cidade' in df.columns else None,
            'Entregador': entregador_combo.get() if 'Entregador' in df.columns else None
        }

        agrupar_e_salvar(df, data, filtros)

    except Exception as e:
        messagebox.showerror("Erro ao processar", str(e))

def iniciar_app():
    global cal, status_combo, cidade_combo, entregador_combo

    arquivo = encontrar_arquivo_excel_mais_recente()
    if not arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo Excel encontrado.")
        return

    df = pd.read_excel(arquivo, sheet_name=0, engine='openpyxl')
    df['Data prevista de entrega'] = pd.to_datetime(df['Data prevista de entrega'], errors='coerce')

    app = tk.Tk()
    app.title("app_logistica_gui - Relatório de Entregas")
    app.geometry("420x500")

    # Seletor de Data
    tk.Label(app, text="Data de Vencimento:", font=("Arial", 11)).pack(pady=5)
    opcoes_data = ["Ontem", "Hoje", "Amanhã", "Selecionar manualmente"]
    data_combo = Combobox(app, values=opcoes_data, state="readonly", width=30)
    data_combo.current(1)
    data_combo.pack(pady=3)

    cal = DateEntry(app, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    cal.set_date(datetime.now())
    cal.pack(pady=5)

    # Campos Condicionais
    if 'Status' in df.columns:
        tk.Label(app, text="Status:", font=("Arial", 11)).pack(pady=5)
        status_opcoes = ["Todos"] + sorted(df['Status'].dropna().unique().tolist())
        status_combo = Combobox(app, values=status_opcoes, state="readonly", width=30)
        status_combo.current(0)
        status_combo.pack(pady=3)
    else:
        status_combo = Combobox(app, values=["Todos"], state="readonly", width=30)
        status_combo.set("Todos")

    if 'Cidade' in df.columns:
        tk.Label(app, text="Cidade:", font=("Arial", 11)).pack(pady=5)
        cidade_opcoes = ["Todas"] + sorted(df['Cidade'].dropna().unique().tolist())
        cidade_combo = Combobox(app, values=cidade_opcoes, state="readonly", width=30)
        cidade_combo.current(0)
        cidade_combo.pack(pady=3)
    else:
        cidade_combo = Combobox(app, values=["Todas"], state="readonly", width=30)
        cidade_combo.set("Todas")

    if 'Entregador' in df.columns:
        tk.Label(app, text="Entregador:", font=("Arial", 11)).pack(pady=5)
        entregador_opcoes = ["Todos"] + sorted(df['Entregador'].dropna().unique().tolist())
        entregador_combo = Combobox(app, values=entregador_opcoes, state="readonly", width=30)
        entregador_combo.current(0)
        entregador_combo.pack(pady=3)
    else:
        entregador_combo = Combobox(app, values=["Todos"], state="readonly", width=30)
        entregador_combo.set("Todos")

    # Botão de execução
    Button(app, text="Gerar Relatório", command=lambda: gerar_relatorio(data_combo.get())).pack(pady=20)

    app.mainloop()

iniciar_app()
