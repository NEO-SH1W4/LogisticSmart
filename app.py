"""
LogisticSmart v2.0 - Sistema Inteligente de Análise de Entregas
Desenvolvido por NEO-SH1W4

Aplicação principal usando Streamlit com autenticação segura,
processamento inteligente de dados e interface moderna.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path para imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.config.settings import get_config, create_directories, STREAMLIT_CONFIG
from src.auth.authentication import render_login_form, logout
from src.utils.data_processor import DataProcessor
from src.utils.export_utils import ExportManager
from src.components.ui_components import render_sidebar, render_file_upload, render_filters

# Configurar a página
st.set_page_config(**STREAMLIT_CONFIG)

# Criar diretórios necessários
create_directories()

def initialize_session_state():
    """Inicializa variáveis de sessão."""
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor()
    
    if 'export_manager' not in st.session_state:
        st.session_state.export_manager = ExportManager()
    
    if 'current_filters' not in st.session_state:
        st.session_state.current_filters = {}
    
    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = 'pending'

def render_header():
    """Renderiza o cabeçalho da aplicação."""
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown("# 📦 LogisticSmart v2.0")
    
    with col2:
        st.markdown("### Sistema Inteligente de Análise de Entregas")
    
    with col3:
        user_data = st.session_state.get('user_data', {})
        if user_data:
            st.markdown(f"👤 **{user_data.get('name', 'Usuário')}**")
            if st.button("🚪 Sair", help="Fazer logout"):
                logout()

def render_main_content():
    """Renderiza o conteúdo principal da aplicação."""
    user_data = st.session_state.get('user_data', {})
    permissions = user_data.get('permissions', {})
    
    # Sidebar com filtros e opções
    with st.sidebar:
        render_sidebar(permissions)
    
    # Conteúdo principal
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Análise de Dados", 
        "📈 Dashboard", 
        "⚙️ Qualidade dos Dados", 
        "ℹ️ Sobre"
    ])
    
    with tab1:
        render_data_analysis_tab(permissions)
    
    with tab2:
        render_dashboard_tab()
    
    with tab3:
        render_data_quality_tab()
    
    with tab4:
        render_about_tab()

def render_data_analysis_tab(permissions):
    """Renderiza a aba de análise de dados."""
    processor = st.session_state.data_processor
    
    # Upload de arquivo
    if permissions.get('upload_files', False):
        uploaded_file = render_file_upload()
        
        if uploaded_file:
            with st.spinner("📂 Processando arquivo..."):
                success, message, df = processor.load_file(
                    uploaded_file.getvalue(), 
                    uploaded_file.name
                )
            
            if success:
                st.success(message)
                st.session_state.uploaded_data = df
            else:
                st.error(message)
                return
    else:
        st.info("👁️ Modo somente leitura - Upload não disponível para seu perfil")
    
    # Verificar se há dados carregados
    if not hasattr(st.session_state, 'uploaded_data') or st.session_state.uploaded_data is None:
        st.warning("📋 Carregue um arquivo para começar a análise")
        return
    
    df = st.session_state.uploaded_data
    
    # Filtros
    st.markdown("---")
    st.markdown("### 🎛️ Filtros de Análise")
    
    filters = render_filters(processor, permissions.get('advanced_filters', False))
    
    # Aplicar filtros
    filtered_df = processor.apply_filters(filters)
    
    # Modo de análise
    analysis_mode = st.radio(
        "📊 Tipo de Análise:",
        options=['pending', 'delivered', 'all'],
        format_func=lambda x: {
            'pending': '⏳ Entregas Pendentes',
            'delivered': '✅ Entregas Realizadas',
            'all': '📋 Todas as Entregas'
        }[x],
        index=['pending', 'delivered', 'all'].index(st.session_state.analysis_mode),
        horizontal=True
    )
    
    st.session_state.analysis_mode = analysis_mode
    
    # Filtrar por status
    status_filtered_df = processor.filter_by_status(filtered_df, analysis_mode)
    
    if status_filtered_df.empty:
        st.warning("⚠️ Nenhum registro encontrado com os filtros selecionados")
        return
    
    # Resultados agrupados
    st.markdown("---")
    st.markdown("### 📊 Resultados por Entregador")
    
    grouped_data = processor.group_by_deliverer(status_filtered_df)
    
    if not grouped_data.empty:
        # Exibir tabela
        st.dataframe(
            grouped_data,
            use_container_width=True,
            hide_index=True
        )
        
        # Estatísticas rápidas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total de Entregas", len(status_filtered_df))
        
        with col2:
            st.metric("👥 Entregadores", len(grouped_data))
        
        with col3:
            avg_deliveries = grouped_data['Quantidade'].mean()
            st.metric("📊 Média por Entregador", f"{avg_deliveries:.1f}")
        
        with col4:
            top_deliverer = grouped_data.iloc[0] if len(grouped_data) > 0 else None
            if top_deliverer is not None:
                st.metric("🏆 Top Entregador", f"{top_deliverer['Quantidade']}")
        
        # Exportação
        if permissions.get('export_data', False):
            st.markdown("---")
            st.markdown("### 📥 Exportar Resultados")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Exportar Excel", use_container_width=True):
                    excel_data = st.session_state.export_manager.to_excel(grouped_data)
                    st.download_button(
                        "⬇️ Download Excel",
                        excel_data,
                        file_name=f"relatorio_entregas_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col2:
                if st.button("📝 Exportar CSV", use_container_width=True):
                    csv_data = st.session_state.export_manager.to_csv(grouped_data)
                    st.download_button(
                        "⬇️ Download CSV",
                        csv_data,
                        file_name=f"relatorio_entregas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                if st.button("📄 Exportar PDF", use_container_width=True):
                    try:
                        pdf_data = st.session_state.export_manager.to_pdf(grouped_data)
                        st.download_button(
                            "⬇️ Download PDF",
                            pdf_data,
                            file_name=f"relatorio_entregas_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Erro ao gerar PDF: {e}")

def render_dashboard_tab():
    """Renderiza a aba do dashboard."""
    if not hasattr(st.session_state, 'uploaded_data') or st.session_state.uploaded_data is None:
        st.info("📊 Carregue dados na aba 'Análise de Dados' para visualizar o dashboard")
        return
    
    processor = st.session_state.data_processor
    df = st.session_state.uploaded_data
    
    # Aplicar filtros atuais
    filtered_df = processor.apply_filters(st.session_state.current_filters)
    
    if filtered_df.empty:
        st.warning("Nenhum dado para exibir no dashboard")
        return
    
    st.markdown("### 📈 Dashboard Executivo")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de entregas por entregador
        grouped_data = processor.group_by_deliverer(filtered_df)
        if not grouped_data.empty:
            fig_bar = px.bar(
                grouped_data.head(10),
                x='Entregador',
                y='Quantidade',
                title="Top 10 Entregadores",
                color='Quantidade',
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Gráfico de pizza
        if not grouped_data.empty:
            fig_pie = px.pie(
                grouped_data.head(8),
                values='Quantidade',
                names='Entregador',
                title="Distribuição de Entregas"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Estatísticas detalhadas
    st.markdown("---")
    stats = processor.get_statistics(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total de Registros", stats.get('total_records', 0))
    
    with col2:
        st.metric("👥 Entregadores Únicos", stats.get('unique_deliverers', 0))
    
    with col3:
        st.metric("🏙️ Cidades Únicas", stats.get('unique_cities', 0))
    
    with col4:
        date_range = stats.get('date_range')
        if date_range:
            days = (date_range['max'] - date_range['min']).days
            st.metric("📅 Período (dias)", days)

def render_data_quality_tab():
    """Renderiza a aba de qualidade dos dados."""
    if not hasattr(st.session_state, 'uploaded_data') or st.session_state.uploaded_data is None:
        st.info("🔍 Carregue dados para avaliar a qualidade")
        return
    
    processor = st.session_state.data_processor
    df = st.session_state.uploaded_data
    
    st.markdown("### 🔍 Avaliação da Qualidade dos Dados")
    
    # Análise de qualidade
    quality_report = processor.validate_data_quality(df)
    
    # Score de qualidade
    score = quality_report.get('quality_score', 0)
    color = "green" if score >= 80 else "orange" if score >= 60 else "red"
    
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; border-radius: 10px; background-color: {color}20; border: 2px solid {color};'>
        <h2 style='color: {color}; margin: 0;'>Score de Qualidade: {score}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Problemas encontrados
    issues = quality_report.get('issues', [])
    if issues:
        st.markdown("#### ⚠️ Problemas Detectados:")
        for issue in issues:
            st.warning(issue)
    
    # Recomendações
    recommendations = quality_report.get('recommendations', [])
    if recommendations:
        st.markdown("#### 💡 Recomendações:")
        for rec in recommendations:
            st.info(rec)
    
    # Informações detalhadas
    with st.expander("📊 Detalhes dos Dados"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Informações Gerais:**")
            st.write(f"- Linhas: {len(df)}")
            st.write(f"- Colunas: {len(df.columns)}")
            st.write(f"- Memória: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        with col2:
            st.markdown("**Tipos de Dados:**")
            dtype_counts = df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                st.write(f"- {dtype}: {count} colunas")

def render_about_tab():
    """Renderiza a aba sobre."""
    st.markdown("### ℹ️ Sobre o LogisticSmart v2.0")
    
    st.markdown("""
    **LogisticSmart** é um sistema inteligente para análise e geração de relatórios de entregas,
    desenvolvido com foco em usabilidade, segurança e performance.
    
    #### 🚀 Funcionalidades Principais:
    - ✅ **Autenticação Segura** com diferentes níveis de acesso
    - 📊 **Processamento Inteligente** de dados Excel/CSV
    - 🎛️ **Filtros Adaptativos** baseados na estrutura dos dados
    - 📈 **Dashboard Interativo** com visualizações modernas
    - 📥 **Exportação Múltipla** (Excel, CSV, PDF)
    - 🔍 **Análise de Qualidade** dos dados
    - ⚡ **Cache Inteligente** para melhor performance
    
    #### 👥 Perfis de Usuário:
    - **👑 Admin**: Acesso completo a todas as funcionalidades
    - **👤 Usuário**: Upload, análise e exportação de dados
    - **👁️ Visitante**: Visualização de relatórios apenas
    
    #### 🛠️ Tecnologias Utilizadas:
    - **Frontend**: Streamlit, Plotly, HTML/CSS
    - **Backend**: Python, Pandas, NumPy
    - **Segurança**: bcrypt, JSON Web Tokens
    - **Exportação**: openpyxl, python-docx, pdfkit
    
    #### 📋 Estrutura de Dados Suportada:
    O sistema detecta automaticamente colunas como:
    - Data prevista de entrega (obrigatória)
    - Entregador/Responsável
    - Cidade/Local/Destino
    - Status/Situação
    - Tipo de produto
    - Cliente/Destinatário
    
    #### 🔗 Links Úteis:
    - **GitHub**: [NEO-SH1W4/LogisticSmart](https://github.com/NEO-SH1W4/LogisticSmart)
    - **Demo Online**: [LogisticSmart Demo](https://logisticsmartx33beta.streamlit.app/)
    
    ---
    
    **Desenvolvido por**: NEO-SH1W4  
    **Versão**: 2.0.0  
    **Última Atualização**: {datetime.now().strftime('%d/%m/%Y')}
    """)

def main():
    """Função principal da aplicação."""
    initialize_session_state()
    
    # Verificar autenticação
    user_data = render_login_form()
    
    if user_data:
        render_header()
        render_main_content()
    else:
        # Aplicar CSS customizado para a tela de login
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f1116 0%, #1c1f26 100%);
        }
        
        .stForm {
            background: rgba(28, 31, 38, 0.8);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid #08c6ff;
            backdrop-filter: blur(10px);
        }
        
        .stTextInput > div > div > input {
            background-color: rgba(28, 31, 38, 0.8);
            border: 1px solid #08c6ff;
            border-radius: 8px;
            color: #f8f9fa;
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #08c6ff, #0056b3);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
        }
        </style>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

