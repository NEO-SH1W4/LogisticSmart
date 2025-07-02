"""
Componentes de interface do usuário para o LogisticSmart.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import plotly.express as px

def render_sidebar(permissions: Dict[str, bool]):
    """
    Renderiza a sidebar com opções baseadas nas permissões do usuário.
    
    Args:
        permissions: Dicionário com permissões do usuário
    """
    st.markdown("## 🎛️ Painel de Controle")
    
    # Informações do usuário
    user_data = st.session_state.get('user_data', {})
    
    with st.expander("👤 Informações do Usuário", expanded=True):
        st.write(f"**Nome:** {user_data.get('name', 'N/A')}")
        st.write(f"**Perfil:** {user_data.get('role', 'N/A').title()}")
        
        # Permissões
        st.write("**Permissões:**")
        perm_icons = {
            'upload_files': '📁',
            'view_reports': '📊',
            'export_data': '📥',
            'manage_users': '👥',
            'view_logs': '📋',
            'advanced_filters': '🔍'
        }
        
        for perm, allowed in permissions.items():
            icon = perm_icons.get(perm, '•')
            status = "✅" if allowed else "❌"
            perm_name = perm.replace('_', ' ').title()
            st.write(f"{icon} {perm_name}: {status}")
    
    # Configurações rápidas
    if permissions.get('advanced_filters', False):
        with st.expander("⚙️ Configurações Rápidas"):
            # Cache
            if st.button("🗑️ Limpar Cache", help="Limpa dados em cache"):
                st.cache_data.clear()
                st.success("Cache limpo!")
                st.rerun()
            
            # Modo escuro/claro
            theme_mode = st.toggle("🌙 Modo Escuro", value=True)
            st.session_state.theme_mode = theme_mode
    
    # Estatísticas da sessão
    with st.expander("📊 Estatísticas da Sessão"):
        if hasattr(st.session_state, 'uploaded_data') and st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            st.metric("📋 Registros Carregados", len(df))
            st.metric("📅 Colunas", len(df.columns))
            
            # Uso de memória
            memory_mb = df.memory_usage(deep=True).sum() / 1024**2
            st.metric("💾 Memória", f"{memory_mb:.1f} MB")
        else:
            st.info("Nenhum dado carregado")

def render_file_upload() -> Optional[Any]:
    """
    Renderiza o componente de upload de arquivo.
    
    Returns:
        Arquivo carregado ou None
    """
    st.markdown("### 📁 Upload de Arquivo")
    
    # Informações sobre formatos suportados
    with st.expander("ℹ️ Formatos Suportados e Estrutura"):
        st.markdown("""
        **Formatos Aceitos:**
        - 📄 Excel (.xlsx, .xls)
        - 📄 CSV (.csv)
        
        **Estrutura Esperada:**
        - **Obrigatório**: Coluna com data de entrega
        - **Opcional**: Entregador, Cidade, Status, Produto, Cliente
        
        **Exemplo de Colunas:**
        - `Data prevista de entrega`
        - `Entregador` ou `Responsável`
        - `Cidade` ou `Destino`
        - `Status` ou `Situação`
        - `Tipo de produto` ou `Item`
        - `Cliente` ou `Destinatário`
        
        ⚡ O sistema detecta automaticamente as colunas!
        """)
    
    # Upload
    uploaded_file = st.file_uploader(
        "Escolha um arquivo:",
        type=['xlsx', 'xls', 'csv'],
        help="Arraste e solte o arquivo ou clique para navegar",
        key="file_uploader"
    )
    
    if uploaded_file:
        # Informações do arquivo
        file_size = len(uploaded_file.getvalue()) / 1024**2  # MB
        st.info(f"📄 **{uploaded_file.name}** ({file_size:.1f} MB)")
        
        # Validações básicas
        if file_size > 200:  # 200MB
            st.error("⚠️ Arquivo muito grande! Máximo permitido: 200MB")
            return None
        
        return uploaded_file
    
    return None

def render_filters(processor, advanced_mode: bool = False) -> Dict[str, Any]:
    """
    Renderiza filtros dinâmicos baseados nos dados carregados.
    
    Args:
        processor: Instância do DataProcessor
        advanced_mode: Se deve mostrar filtros avançados
        
    Returns:
        Dicionário com filtros selecionados
    """
    filters = {}
    
    if not hasattr(processor, 'df') or processor.df is None:
        st.info("📋 Carregue dados para ver os filtros disponíveis")
        return filters
    
    df = processor.df
    detected_columns = processor.detected_columns
    
    # Filtro de data
    st.markdown("#### 📅 Filtro por Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        date_options = {
            "Hoje": datetime.now().date(),
            "Ontem": datetime.now().date() - timedelta(days=1),
            "Amanhã": datetime.now().date() + timedelta(days=1),
            "Esta Semana": None,  # Será tratado separadamente
            "Personalizada": None
        }
        
        date_choice = st.selectbox(
            "📆 Período:",
            options=list(date_options.keys()),
            index=0
        )
    
    with col2:
        if date_choice == "Personalizada":
            custom_date = st.date_input(
                "Selecione a data:",
                value=datetime.now().date(),
                help="Escolha uma data específica"
            )
            filters['date_filter'] = custom_date
        elif date_choice == "Esta Semana":
            # Calcular início da semana
            today = datetime.now().date()
            start_week = today - timedelta(days=today.weekday())
            st.info(f"📅 Semana de {start_week.strftime('%d/%m')} até hoje")
            filters['date_range'] = (start_week, today)
        else:
            filters['date_filter'] = date_options[date_choice]
    
    # Filtros por colunas detectadas
    st.markdown("#### 🎛️ Filtros por Categoria")
    
    filter_cols = st.columns(2)
    col_index = 0
    
    for filter_type, column_name in detected_columns.items():
        if filter_type == 'data_entrega':  # Já tratado acima
            continue
        
        if column_name and column_name in df.columns:
            options = processor.get_filter_options(column_name)
            
            if options and len(options) > 1:  # Só mostrar se houver opções variadas
                with filter_cols[col_index % 2]:
                    filter_label = {
                        'entregador': '👤 Entregador',
                        'cidade': '🏙️ Cidade',
                        'status': '📊 Status',
                        'produto': '📦 Produto',
                        'cliente': '👥 Cliente'
                    }.get(filter_type, f"🔍 {column_name}")
                    
                    if advanced_mode:
                        # Filtro múltiplo para modo avançado
                        selected_values = st.multiselect(
                            filter_label,
                            options=options,
                            default=[],
                            help=f"Selecione um ou mais valores para {column_name}"
                        )
                        if selected_values:
                            filters[filter_type] = selected_values
                    else:
                        # Filtro único para modo básico
                        selected_value = st.selectbox(
                            filter_label,
                            options=["Todos"] + options,
                            index=0,
                            help=f"Filtrar por {column_name}"
                        )
                        if selected_value != "Todos":
                            filters[filter_type] = selected_value
                
                col_index += 1
    
    # Filtros avançados
    if advanced_mode:
        with st.expander("🔍 Filtros Avançados"):
            # Filtro por período de tempo
            st.markdown("**📊 Análise Temporal:**")
            
            time_analysis = st.radio(
                "Tipo de análise:",
                options=["Dia específico", "Período", "Últimos dias"],
                horizontal=True
            )
            
            if time_analysis == "Período":
                date_col1, date_col2 = st.columns(2)
                with date_col1:
                    start_date = st.date_input("Data inicial:", datetime.now().date() - timedelta(days=7))
                with date_col2:
                    end_date = st.date_input("Data final:", datetime.now().date())
                
                if start_date <= end_date:
                    filters['date_range'] = (start_date, end_date)
                else:
                    st.error("Data inicial deve ser anterior à data final!")
            
            elif time_analysis == "Últimos dias":
                days_back = st.slider("Quantos dias atrás:", 1, 30, 7)
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=days_back)
                filters['date_range'] = (start_date, end_date)
            
            # Filtros numéricos se disponíveis
            numeric_columns = df.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                st.markdown("**🔢 Filtros Numéricos:**")
                
                for col in numeric_columns:
                    if df[col].nunique() > 10:  # Só para colunas com boa variação
                        min_val = float(df[col].min())
                        max_val = float(df[col].max())
                        
                        if min_val != max_val:
                            range_values = st.slider(
                                f"Faixa para {col}:",
                                min_value=min_val,
                                max_value=max_val,
                                value=(min_val, max_val),
                                step=(max_val - min_val) / 100
                            )
                            
                            if range_values != (min_val, max_val):
                                filters[f'{col}_range'] = range_values
    
    # Resumo dos filtros ativos
    active_filters = [k for k, v in filters.items() if v is not None and v != []]
    if active_filters:
        st.success(f"🎯 {len(active_filters)} filtro(s) ativo(s)")
    
    # Salvar filtros na sessão
    st.session_state.current_filters = filters
    
    return filters

def render_data_preview(df: pd.DataFrame, max_rows: int = 100):
    """
    Renderiza uma prévia dos dados carregados.
    
    Args:
        df: DataFrame com os dados
        max_rows: Número máximo de linhas para exibir
    """
    st.markdown("### 👁️ Prévia dos Dados")
    
    # Informações básicas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total de Linhas", len(df))
    
    with col2:
        st.metric("📊 Colunas", len(df.columns))
    
    with col3:
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("💾 Memória", f"{memory_mb:.1f} MB")
    
    with col4:
        null_count = df.isnull().sum().sum()
        st.metric("⚠️ Valores Nulos", null_count)
    
    # Prévia da tabela
    display_df = df.head(max_rows)
    
    st.markdown(f"**Exibindo {len(display_df)} de {len(df)} registros:**")
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Informações sobre as colunas
    with st.expander("📊 Informações das Colunas"):
        col_info = []
        for col in df.columns:
            info = {
                'Coluna': col,
                'Tipo': str(df[col].dtype),
                'Não Nulos': df[col].count(),
                'Nulos': df[col].isnull().sum(),
                'Únicos': df[col].nunique()
            }
            col_info.append(info)
        
        info_df = pd.DataFrame(col_info)
        st.dataframe(info_df, use_container_width=True)

def render_quick_stats(df: pd.DataFrame, processor):
    """
    Renderiza estatísticas rápidas dos dados.
    
    Args:
        df: DataFrame com os dados
        processor: Instância do DataProcessor
    """
    st.markdown("### 📈 Estatísticas Rápidas")
    
    # Estatísticas gerais
    stats = processor.get_statistics(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Gráfico de status (se disponível)
        status_dist = stats.get('status_distribution', {})
        if status_dist:
            fig_status = px.pie(
                values=list(status_dist.values()),
                names=list(status_dist.keys()),
                title="📊 Distribuição por Status"
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Top entregadores
        if 'entregador' in processor.detected_columns:
            top_deliverers = processor.group_by_deliverer(df).head(5)
            if not top_deliverers.empty:
                fig_deliverers = px.bar(
                    top_deliverers,
                    x='Quantidade',
                    y='Entregador',
                    orientation='h',
                    title="🏆 Top 5 Entregadores"
                )
                st.plotly_chart(fig_deliverers, use_container_width=True)
    
    with col3:
        # Métricas resumidas
        st.markdown("**📋 Resumo:**")
        st.write(f"• **Total de registros:** {stats.get('total_records', 0)}")
        st.write(f"• **Entregadores únicos:** {stats.get('unique_deliverers', 0)}")
        st.write(f"• **Cidades únicas:** {stats.get('unique_cities', 0)}")
        
        date_range = stats.get('date_range')
        if date_range:
            days = (date_range['max'] - date_range['min']).days
            st.write(f"• **Período:** {days} dias")
            st.write(f"• **De:** {date_range['min'].strftime('%d/%m/%Y')}")
            st.write(f"• **Até:** {date_range['max'].strftime('%d/%m/%Y')}")

def render_export_buttons(data: pd.DataFrame, export_manager, permissions: Dict[str, bool]):
    """
    Renderiza botões de exportação baseados nas permissões.
    
    Args:
        data: DataFrame para exportar
        export_manager: Instância do ExportManager
        permissions: Permissões do usuário
    """
    if not permissions.get('export_data', False):
        st.info("🔒 Exportação não disponível para seu perfil")
        return
    
    st.markdown("### 📥 Exportar Dados")
    
    if data.empty:
        st.warning("⚠️ Nenhum dado para exportar")
        return
    
    # Opções de exportação
    available_formats = export_manager.get_available_formats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    with col1:
        if 'Excel' in available_formats and st.button("📄 Excel", use_container_width=True):
            try:
                excel_data = export_manager.to_excel(data)
                st.download_button(
                    "⬇️ Download Excel",
                    excel_data,
                    file_name=f"logistic_report_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")
    
    with col2:
        if 'CSV' in available_formats and st.button("📝 CSV", use_container_width=True):
            try:
                csv_data = export_manager.to_csv(data)
                st.download_button(
                    "⬇️ Download CSV",
                    csv_data,
                    file_name=f"logistic_report_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Erro ao gerar CSV: {e}")
    
    with col3:
        if 'Word' in available_formats and st.button("📝 Word", use_container_width=True):
            try:
                docx_data = export_manager.to_docx(data)
                if docx_data:
                    st.download_button(
                        "⬇️ Download Word",
                        docx_data,
                        file_name=f"logistic_report_{timestamp}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                else:
                    st.error("Word export não está disponível")
            except Exception as e:
                st.error(f"Erro ao gerar Word: {e}")
    
    with col4:
        if 'PDF' in available_formats and st.button("📄 PDF", use_container_width=True):
            try:
                pdf_data = export_manager.to_pdf(data)
                if pdf_data:
                    st.download_button(
                        "⬇️ Download PDF",
                        pdf_data,
                        file_name=f"logistic_report_{timestamp}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error("PDF export não está disponível")
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")

