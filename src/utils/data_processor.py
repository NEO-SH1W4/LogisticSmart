"""
Utilitários para processamento e validação de dados.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import streamlit as st
import logging
from pathlib import Path

from ..config.settings import REQUIRED_COLUMNS, AUTO_FILTERS

logger = logging.getLogger(__name__)

class DataProcessor:
    """Processador principal de dados do LogisticSmart."""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.original_columns: List[str] = []
        self.detected_columns: Dict[str, str] = {}
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def load_file(_self, file_content: bytes, filename: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Carrega arquivo Excel ou CSV.
        
        Args:
            file_content: Conteúdo do arquivo
            filename: Nome do arquivo
            
        Returns:
            Tupla (sucesso, mensagem, dataframe)
        """
        try:
            file_extension = Path(filename).suffix.lower()
            
            if file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_content, engine='openpyxl')
            elif file_extension == '.csv':
                # Tentar diferentes encodings e separadores
                try:
                    df = pd.read_csv(file_content, encoding='utf-8', sep=';')
                except:
                    try:
                        df = pd.read_csv(file_content, encoding='latin-1', sep=';')
                    except:
                        df = pd.read_csv(file_content, encoding='utf-8', sep=',')
            else:
                return False, f"Formato de arquivo não suportado: {file_extension}", None
            
            if df.empty:
                return False, "Arquivo está vazio", None
            
            # Validar e processar
            success, message = _self._validate_dataframe(df)
            if not success:
                return False, message, None
            
            # Detectar colunas automaticamente
            _self.original_columns = df.columns.tolist()
            _self.detected_columns = _self._detect_columns(df)
            _self.df = _self._preprocess_dataframe(df)
            
            logger.info(f"Arquivo carregado com sucesso: {filename}, {len(df)} linhas")
            return True, f"✅ Arquivo carregado: {len(df)} registros", _self.df
            
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo {filename}: {e}")
            return False, f"Erro ao carregar arquivo: {str(e)}", None
    
    def _validate_dataframe(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Valida estrutura básica do DataFrame."""
        if df.empty:
            return False, "DataFrame está vazio"
        
        # Verificar se há pelo menos uma coluna com dados
        if df.dropna(how='all').empty:
            return False, "Arquivo não contém dados válidos"
        
        # Verificar colunas obrigatórias
        missing_required = []
        for col in REQUIRED_COLUMNS:
            if not any(col.lower() in str(c).lower() for c in df.columns):
                missing_required.append(col)
        
        if missing_required:
            return False, f"Colunas obrigatórias não encontradas: {', '.join(missing_required)}"
        
        return True, "DataFrame válido"
    
    def _detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Detecta automaticamente o tipo de cada coluna."""
        detected = {}
        
        for col in df.columns:
            col_lower = str(col).lower()
            
            # Verificar cada tipo de filtro automático
            for filter_type, keywords in AUTO_FILTERS.items():
                for keyword in keywords:
                    if keyword.lower() in col_lower:
                        detected[filter_type] = col
                        break
                if filter_type in detected:
                    break
            
            # Detectar coluna de data obrigatória
            for required_col in REQUIRED_COLUMNS:
                if required_col.lower() in col_lower:
                    detected['data_entrega'] = col
                    break
        
        return detected
    
    def _preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pré-processa o DataFrame para padronizar dados."""
        df_processed = df.copy()
        
        # Processar coluna de data
        date_col = self.detected_columns.get('data_entrega')
        if date_col and date_col in df_processed.columns:
            df_processed[date_col] = pd.to_datetime(
                df_processed[date_col], 
                errors='coerce',
                infer_datetime_format=True
            )
            
            # Remover linhas com datas inválidas
            df_processed = df_processed.dropna(subset=[date_col])
        
        # Limpar strings
        for col in df_processed.select_dtypes(include=['object']).columns:
            df_processed[col] = df_processed[col].astype(str).str.strip()
            df_processed[col] = df_processed[col].replace('nan', '')
        
        # Remover linhas completamente vazias
        df_processed = df_processed.dropna(how='all')
        
        return df_processed
    
    def get_filter_options(self, column: str) -> List[str]:
        """Retorna opções únicas para filtros."""
        if self.df is None or column not in self.df.columns:
            return []
        
        options = self.df[column].dropna().unique()
        return sorted([str(opt) for opt in options if str(opt) != 'nan'])
    
    def apply_filters(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Aplica filtros ao DataFrame."""
        if self.df is None:
            return pd.DataFrame()
        
        filtered_df = self.df.copy()
        
        # Filtro por data
        if 'date_filter' in filters and filters['date_filter']:
            date_col = self.detected_columns.get('data_entrega')
            if date_col and date_col in filtered_df.columns:
                target_date = filters['date_filter']
                filtered_df = filtered_df[
                    filtered_df[date_col].dt.date == target_date
                ]
        
        # Filtros por colunas específicas
        for filter_name, values in filters.items():
            if filter_name == 'date_filter' or not values:
                continue
            
            # Mapear filtro para coluna real
            column = None
            if filter_name in self.detected_columns:
                column = self.detected_columns[filter_name]
            elif filter_name in self.df.columns:
                column = filter_name
            
            if column and column in filtered_df.columns:
                if isinstance(values, list):
                    filtered_df = filtered_df[
                        filtered_df[column].astype(str).isin([str(v) for v in values])
                    ]
                else:
                    filtered_df = filtered_df[
                        filtered_df[column].astype(str) == str(values)
                    ]
        
        return filtered_df
    
    def filter_by_status(self, df: pd.DataFrame, status_type: str = 'all') -> pd.DataFrame:
        """Filtra por status de entrega."""
        if status_type == 'all':
            return df
        
        status_col = self.detected_columns.get('status')
        if not status_col or status_col not in df.columns:
            return df
        
        if status_type == 'delivered':
            # Buscar indicadores de entrega
            delivered_indicators = ['entregue', 'entregado', 'delivered', 'ok', 'concluido', 'finalizado']
            mask = df[status_col].astype(str).str.lower().str.contains(
                '|'.join(delivered_indicators), na=False
            )
            return df[mask]
        
        elif status_type == 'pending':
            # Buscar indicadores de pendência
            pending_indicators = ['pendente', 'pending', 'aguardando', 'em rota', 'em transito']
            mask = df[status_col].astype(str).str.lower().str.contains(
                '|'.join(pending_indicators), na=False
            )
            return df[mask]
        
        return df
    
    def group_by_deliverer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Agrupa entregas por entregador."""
        if df.empty:
            return pd.DataFrame(columns=['Entregador', 'Quantidade'])
        
        deliverer_col = self.detected_columns.get('entregador')
        if not deliverer_col or deliverer_col not in df.columns:
            return pd.DataFrame(columns=['Entregador', 'Quantidade'])
        
        result = (
            df[deliverer_col]
            .value_counts()
            .reset_index()
            .rename(columns={deliverer_col: 'Quantidade', 'index': 'Entregador'})
        )
        
        # Adicionar estatísticas extras se possível
        if len(result) > 0:
            result = result.sort_values('Quantidade', ascending=False)
            result['Percentual'] = (result['Quantidade'] / result['Quantidade'].sum() * 100).round(1)
        
        return result
    
    def get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Gera estatísticas do DataFrame."""
        if df.empty:
            return {}
        
        stats = {
            'total_records': len(df),
            'date_range': None,
            'unique_deliverers': 0,
            'unique_cities': 0,
            'status_distribution': {},
        }
        
        # Estatísticas de data
        date_col = self.detected_columns.get('data_entrega')
        if date_col and date_col in df.columns:
            dates = df[date_col].dropna()
            if not dates.empty:
                stats['date_range'] = {
                    'min': dates.min().date(),
                    'max': dates.max().date()
                }
        
        # Estatísticas de entregadores
        deliverer_col = self.detected_columns.get('entregador')
        if deliverer_col and deliverer_col in df.columns:
            stats['unique_deliverers'] = df[deliverer_col].nunique()
        
        # Estatísticas de cidades
        city_col = self.detected_columns.get('cidade')
        if city_col and city_col in df.columns:
            stats['unique_cities'] = df[city_col].nunique()
        
        # Distribuição de status
        status_col = self.detected_columns.get('status')
        if status_col and status_col in df.columns:
            stats['status_distribution'] = df[status_col].value_counts().to_dict()
        
        return stats
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Avalia qualidade dos dados."""
        if df.empty:
            return {'quality_score': 0, 'issues': ['DataFrame vazio']}
        
        issues = []
        quality_score = 100
        
        # Verificar dados faltantes
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            missing_percentage = (missing_data.sum() / (len(df) * len(df.columns))) * 100
            quality_score -= min(missing_percentage, 30)
            issues.append(f"Dados faltantes: {missing_percentage:.1f}%")
        
        # Verificar duplicatas
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            duplicate_percentage = (duplicates / len(df)) * 100
            quality_score -= min(duplicate_percentage, 20)
            issues.append(f"Registros duplicados: {duplicates} ({duplicate_percentage:.1f}%)")
        
        # Verificar consistência de datas
        date_col = self.detected_columns.get('data_entrega')
        if date_col and date_col in df.columns:
            future_dates = df[df[date_col] > datetime.now()]
            if len(future_dates) > len(df) * 0.8:  # Mais de 80% no futuro
                quality_score -= 15
                issues.append("Muitas datas futuras detectadas")
        
        # Verificar valores extremos
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].std() > df[col].mean() * 3:  # Desvio muito alto
                quality_score -= 5
                issues.append(f"Valores extremos em {col}")
        
        quality_score = max(0, min(100, quality_score))
        
        return {
            'quality_score': round(quality_score, 1),
            'issues': issues,
            'recommendations': _get_quality_recommendations(issues)
        }

def _get_quality_recommendations(issues: List[str]) -> List[str]:
    """Gera recomendações baseadas nos problemas encontrados."""
    recommendations = []
    
    for issue in issues:
        if 'faltantes' in issue:
            recommendations.append("Considere preencher dados faltantes ou remover registros incompletos")
        elif 'duplicados' in issue:
            recommendations.append("Remova registros duplicados para melhorar a precisão")
        elif 'datas futuras' in issue:
            recommendations.append("Verifique se as datas estão no formato correto")
        elif 'extremos' in issue:
            recommendations.append("Revise valores discrepantes que podem ser erros de digitação")
    
    return recommendations

