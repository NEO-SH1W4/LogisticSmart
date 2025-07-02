"""
Configurações centralizadas do LogisticSmart.
"""
import os
from pathlib import Path
from typing import Dict, Any

# Diretórios base
BASE_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "Relatórios"
TEMP_DIR = BASE_DIR / "temp"

# Configurações da aplicação
APP_CONFIG = {
    "name": "LogisticSmart",
    "version": "2.0.0",
    "description": "Sistema Inteligente de Análise de Entregas",
    "author": "NEO-SH1W4",
    "max_upload_size": 200 * 1024 * 1024,  # 200MB
    "supported_formats": [".xlsx", ".xls", ".csv"],
}

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "page_title": "LogisticSmart v2.0",
    "page_icon": "📦",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Configurações de tema
THEME_CONFIG = {
    "base": "dark",
    "primaryColor": "#08c6ff",
    "backgroundColor": "#0f1116",
    "secondaryBackgroundColor": "#1c1f26",
    "textColor": "#f8f9fa",
}

# Configurações de cache
CACHE_CONFIG = {
    "ttl": 3600,  # 1 hora
    "max_entries": 100,
    "persist": True,
}

# Colunas obrigatórias e opcionais
REQUIRED_COLUMNS = ["Data prevista de entrega"]
OPTIONAL_COLUMNS = [
    "Entregador",
    "Cidade", 
    "Status",
    "Tipo de produto",
    "Destino",
    "Cliente",
    "Valor",
    "Observações"
]

# Filtros automáticos baseados em padrões
AUTO_FILTERS = {
    "status": ["Status", "Situação", "Estado"],
    "entregador": ["Entregador", "Responsável", "Motorista"],
    "cidade": ["Cidade", "Local", "Destino", "Município"],
    "produto": ["Produto", "Tipo de produto", "Item", "Mercadoria"],
    "cliente": ["Cliente", "Destinatário", "Receptor"],
}

# Configurações de exportação
EXPORT_CONFIG = {
    "excel": {
        "engine": "openpyxl",
        "index": False,
        "sheet_name": "Relatório",
    },
    "csv": {
        "index": False,
        "encoding": "utf-8-sig",
        "sep": ";"
    },
    "pdf": {
        "options": {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
        }
    }
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": ["console", "file"],
    "file_path": BASE_DIR / "logs" / "logistic_smart.log",
}

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Retorna configurações específicas ou todas as configurações.
    
    Args:
        section: Nome da seção de configuração
        
    Returns:
        Dicionário com as configurações
    """
    configs = {
        "app": APP_CONFIG,
        "streamlit": STREAMLIT_CONFIG,
        "theme": THEME_CONFIG,
        "cache": CACHE_CONFIG,
        "export": EXPORT_CONFIG,
        "logging": LOGGING_CONFIG,
    }
    
    if section:
        return configs.get(section, {})
    return configs

def create_directories():
    """Cria diretórios necessários se não existirem."""
    directories = [UPLOAD_DIR, REPORTS_DIR, TEMP_DIR, BASE_DIR / "logs"]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

