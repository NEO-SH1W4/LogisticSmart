"""
Testes para o módulo de processamento de dados.
"""
import pytest
import pandas as pd
from datetime import datetime
from io import BytesIO

from src.utils.data_processor import DataProcessor


class TestDataProcessor:
    """Testes para a classe DataProcessor."""
    
    def setup_method(self):
        """Setup para cada teste."""
        self.processor = DataProcessor()
    
    def test_init(self):
        """Testa inicialização do DataProcessor."""
        assert self.processor.df is None
        assert self.processor.original_columns == []
        assert self.processor.detected_columns == {}
    
    def test_validate_dataframe_empty(self):
        """Testa validação de DataFrame vazio."""
        empty_df = pd.DataFrame()
        success, message = self.processor._validate_dataframe(empty_df)
        
        assert not success
        assert "vazio" in message.lower()
    
    def test_validate_dataframe_no_required_columns(self):
        """Testa validação de DataFrame sem colunas obrigatórias."""
        df = pd.DataFrame({
            'coluna1': [1, 2, 3],
            'coluna2': ['a', 'b', 'c']
        })
        
        success, message = self.processor._validate_dataframe(df)
        
        assert not success
        assert "obrigatórias" in message.lower()
    
    def test_validate_dataframe_with_required_columns(self):
        """Testa validação de DataFrame com colunas obrigatórias."""
        df = pd.DataFrame({
            'Data prevista de entrega': ['2025-01-01', '2025-01-02'],
            'Entregador': ['João', 'Maria']
        })
        
        success, message = self.processor._validate_dataframe(df)
        
        assert success
        assert "válido" in message.lower()
    
    def test_detect_columns(self):
        """Testa detecção automática de colunas."""
        df = pd.DataFrame({
            'Data prevista de entrega': ['2025-01-01', '2025-01-02'],
            'Entregador': ['João', 'Maria'],
            'Cidade': ['São Paulo', 'Rio de Janeiro'],
            'Status': ['Pendente', 'Entregue']
        })
        
        detected = self.processor._detect_columns(df)
        
        assert 'data_entrega' in detected
        assert 'entregador' in detected
        assert 'cidade' in detected
        assert 'status' in detected
    
    def test_get_filter_options_empty_df(self):
        """Testa obtenção de opções de filtro com DataFrame vazio."""
        options = self.processor.get_filter_options('test_column')
        
        assert options == []
    
    def test_get_filter_options_with_data(self):
        """Testa obtenção de opções de filtro com dados."""
        self.processor.df = pd.DataFrame({
            'Cidade': ['São Paulo', 'Rio de Janeiro', 'São Paulo', 'Brasília']
        })
        
        options = self.processor.get_filter_options('Cidade')
        
        assert len(options) == 3
        assert 'São Paulo' in options
        assert 'Rio de Janeiro' in options
        assert 'Brasília' in options
    
    def test_group_by_deliverer_empty_df(self):
        """Testa agrupamento por entregador com DataFrame vazio."""
        empty_df = pd.DataFrame()
        result = self.processor.group_by_deliverer(empty_df)
        
        assert result.empty
        assert list(result.columns) == ['Entregador', 'Quantidade']
    
    def test_group_by_deliverer_with_data(self):
        """Testa agrupamento por entregador com dados."""
        df = pd.DataFrame({
            'Entregador': ['João', 'Maria', 'João', 'Pedro', 'Maria', 'João']
        })
        
        self.processor.detected_columns = {'entregador': 'Entregador'}
        result = self.processor.group_by_deliverer(df)
        
        assert len(result) == 3
        assert result.iloc[0]['Entregador'] == 'João'
        assert result.iloc[0]['Quantidade'] == 3
    
    def test_filter_by_status_all(self):
        """Testa filtro por status - todos."""
        df = pd.DataFrame({
            'Status': ['Pendente', 'Entregue', 'Cancelado']
        })
        
        result = self.processor.filter_by_status(df, 'all')
        
        assert len(result) == 3
    
    def test_filter_by_status_delivered(self):
        """Testa filtro por status - entregues."""
        df = pd.DataFrame({
            'Status': ['Pendente', 'Entregue', 'Cancelado', 'Entregado']
        })
        
        self.processor.detected_columns = {'status': 'Status'}
        result = self.processor.filter_by_status(df, 'delivered')
        
        assert len(result) == 2  # 'Entregue' e 'Entregado'


@pytest.fixture
def sample_excel_data():
    """Fixture com dados de exemplo para testes."""
    data = {
        'Data prevista de entrega': ['2025-01-01', '2025-01-02', '2025-01-03'],
        'Entregador': ['João', 'Maria', 'João'],
        'Cidade': ['São Paulo', 'Rio de Janeiro', 'Brasília'],
        'Status': ['Pendente', 'Entregue', 'Pendente'],
        'Cliente': ['Cliente A', 'Cliente B', 'Cliente C']
    }
    
    df = pd.DataFrame(data)
    
    # Criar arquivo Excel em memória
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    
    return buffer


def test_load_file_excel(sample_excel_data):
    """Testa carregamento de arquivo Excel."""
    processor = DataProcessor()
    
    success, message, loaded_df = processor.load_file(
        sample_excel_data.getvalue(),
        "test_file.xlsx"
    )
    
    assert success
    assert loaded_df is not None
    assert len(loaded_df) == 3
    assert 'Data prevista de entrega' in loaded_df.columns


def test_load_file_unsupported_format():
    """Testa carregamento de arquivo com formato não suportado."""
    processor = DataProcessor()
    
    success, message, loaded_df = processor.load_file(
        b"test content",
        "test_file.txt"
    )
    
    assert not success
    assert "não suportado" in message.lower()
    assert loaded_df is None

