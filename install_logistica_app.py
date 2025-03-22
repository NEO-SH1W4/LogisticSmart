import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
import base64
from docx import Document
import pdfkit
import tempfile
import re

st.set_page_config(page_title="Relatório de Entregas - Web", layout="wide")
st.title("📦 Logística Online - Relatório por Entregador")

st.markdown("### 📂 Suba seu arquivo `.xlsx` com os dados de entregas:")

uploaded_file = st.file_uploader("Escolher arquivo Excel", type=["xlsx"], help="O arquivo deve estar no formato Excel (.xlsx)")

def gerar_docx(resultado):
    doc = Document()
    doc.add_heading("Relatório de Entregas Agrupadas", level=1)
    table = doc.add_table(rows=1, cols=len(resultado.columns))
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(resultado.columns):
        hdr_cells[i].text = col
    for _, row in resultado.iterrows():
        row_cells = table.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)
    temp = BytesIO()
    doc.save(temp)
    temp.seek(0)
    return temp

def gerar_pdf(resultado):
    html = resultado.to_html(index=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        f.write(html.encode("utf-8"))
        f.flush()
        pdf_data = pdfkit.from_file(f.name, False)
        return BytesIO(pdf_data)

# === NLP simples (Fase 1) ===
def interpretar_comando(texto):
    texto = texto.lower()
    filtros = {}

    if "camaçari" in texto:
        filtros["Cidade"] = "Camaçari"
    if "salvador" in texto:
        filtros["Cidade"] = "Salvador"
    if "lauro" in texto:
        filtros["Cidade"] = "Lauro de Freitas"
    if "dias d'ávila" in texto:
        filtros["Cidade"] = "Dias D'Ávila"
    if "ausência" in texto:
        filtros["Tipo problemático"] = "Ausência"
    if "endereço" in texto:
        filtros["Tipo problemático"] = "Endereço incorreto"
    if "telefone" in texto:
        filtros["Tipo problemático"] = "Telefone errado"
    if "ez" in texto:
        filtros["Tipo de produto"] = "EZ"
    if "entregue" in texto:
        filtros["Status"] = "Entregue"
    if "pendente" in texto:
        filtros["Status"] = "Pendente"

    return filtros

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        if 'Data prevista de entrega' not in df.columns:
            st.error("❌ Coluna obrigatória 'Data prevista de entrega' não encontrada.")
            st.stop()

        df['Data prevista de entrega'] = pd.to_datetime(df['Data prevista de entrega'], errors='coerce')
        df = df.dropna(subset=['Data prevista de entrega'])

        aba = st.radio("Selecione a visualização:", ["🔍 Análise de Pendentes", "✅ Entregas Realizadas"])

        hoje = datetime.now().date()
        opcoes_data = {"Hoje": hoje, "Ontem": hoje - timedelta(days=1), "Amanhã": hoje + timedelta(days=1)}
        opcao = st.selectbox("📅 Filtrar por data:", list(opcoes_data.keys()) + ["Selecionar manualmente"])

        if opcao == "Selecionar manualmente":
            data_alvo = st.date_input("📆 Escolha a data:", hoje)
        else:
            data_alvo = opcoes_data[opcao]

        df = df[df['Data prevista de entrega'].dt.date == data_alvo]

        if aba == "✅ Entregas Realizadas":
            if 'Status' in df.columns:
                df = df[df['Status'].astype(str).str.lower().str.contains("entregue")]

        colunas = df.columns

        def filtrar_opcoes(coluna):
            if coluna in colunas:
                return sorted(df[coluna].astype(str).dropna().unique().tolist())
            return []

        st.markdown("---")
        st.markdown("### 🤖 Ou digite um comando inteligente:")
        comando = st.text_input("Ex: entregas pendentes em Salvador com problema de endereço")

        if comando:
            filtros_nlp = interpretar_comando(comando)
            for coluna, valor in filtros_nlp.items():
                if coluna in df.columns:
                    df = df[df[coluna].astype(str).str.contains(valor, case=False, na=False)]

        st.markdown("---")
        st.markdown("### 🎛️ Filtros manuais (opcional):")

        cidades = st.multiselect("🏙️ Filtrar por cidade:", filtrar_opcoes('Cidade'))
        entregadores = st.multiselect("👤 Filtrar por entregador:", filtrar_opcoes('Entregador'))
        problematicos = st.multiselect("⚠️ Filtrar por tipo de problema:", filtrar_opcoes('Tipo problemático'))
        produtos = st.multiselect("📦 Filtrar por tipo de produto:", filtrar_opcoes('Tipo de produto'))
        destinos = st.multiselect("🚚 Filtrar por destino:", filtrar_opcoes('Destino'))

        if cidades:
            df = df[df['Cidade'].astype(str).isin(cidades)]
        if entregadores:
            df = df[df['Entregador'].astype(str).isin(entregadores)]
        if problematicos:
            df = df[df['Tipo problemático'].astype(str).isin(problematicos)]
        if produtos:
            df = df[df['Tipo de produto'].astype(str).isin(produtos)]
        if destinos:
            df = df[df['Destino'].astype(str).isin(destinos)]

        if df.empty:
            st.warning("⚠️ Nenhuma entrega encontrada para os filtros selecionados.")
        else:
            resultado = (
                df['Entregador']
                .value_counts()
                .reset_index()
                .rename(columns={'index': 'Entregador', 'Entregador': 'Quantidade'})
            )

            st.subheader("📊 Resumo por entregador")
            st.dataframe(resultado)

            buffer = BytesIO()
            resultado.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            b64 = base64.b64encode(buffer.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="entregas_agrupadas_{data_alvo.strftime('%d-%m')}.xlsx">🔗 Baixar Excel</a>'
            st.markdown(href, unsafe_allow_html=True)

            st.download_button("📄 Baixar como DOCX", gerar_docx(resultado), file_name=f"relatorio_{data_alvo.strftime('%d-%m')}.docx")

            if st.button("📅 Baixar como PDF"):
                st.download_button("📅 Clique para baixar PDF", gerar_pdf(resultado), file_name=f"relatorio_{data_alvo.strftime('%d-%m')}.pdf")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
