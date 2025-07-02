"""
Sistema de autenticação do LogisticSmart.
"""
import streamlit as st
import bcrypt
import os
from typing import Optional, Dict, Tuple
from pathlib import Path
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Gerenciador de autenticação da aplicação."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Inicializa o gerenciador de autenticação.
        
        Args:
            config_path: Caminho para o arquivo de configuração de usuários
        """
        self.config_path = config_path or Path(__file__).parent / "users.json"
        self.users = self._load_users()
    
    def _load_users(self) -> Dict[str, Dict]:
        """Carrega usuários do arquivo de configuração."""
        if not self.config_path.exists():
            # Criar usuários padrão se o arquivo não existir
            default_users = {
                "admin": {
                    "password_hash": self._hash_password("admin123"),
                    "role": "admin",
                    "name": "Administrador",
                    "active": True
                },
                "visitante": {
                    "password_hash": self._hash_password("fasebeta"),
                    "role": "viewer",
                    "name": "Visitante",
                    "active": True
                },
                "neo": {
                    "password_hash": self._hash_password("matrix"),
                    "role": "admin",
                    "name": "Neo",
                    "active": True
                }
            }
            self._save_users(default_users)
            return default_users
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar usuários: {e}")
            return {}
    
    def _save_users(self, users: Dict[str, Dict]):
        """Salva usuários no arquivo de configuração."""
        try:
            os.makedirs(self.config_path.parent, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar usuários: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Gera hash da senha."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verifica se a senha está correta."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Autentica um usuário.
        
        Args:
            username: Nome do usuário
            password: Senha do usuário
            
        Returns:
            Tupla (sucesso, dados_do_usuario)
        """
        username = username.lower().strip()
        
        if username not in self.users:
            logger.warning(f"Tentativa de login com usuário inexistente: {username}")
            return False, None
        
        user_data = self.users[username]
        
        if not user_data.get('active', False):
            logger.warning(f"Tentativa de login com usuário inativo: {username}")
            return False, None
        
        if self._verify_password(password, user_data['password_hash']):
            logger.info(f"Login bem-sucedido para usuário: {username}")
            return True, {
                'username': username,
                'name': user_data.get('name', username),
                'role': user_data.get('role', 'viewer'),
                'permissions': self._get_permissions(user_data.get('role', 'viewer'))
            }
        
        logger.warning(f"Senha incorreta para usuário: {username}")
        return False, None
    
    def _get_permissions(self, role: str) -> Dict[str, bool]:
        """Retorna permissões baseadas no papel do usuário."""
        permissions = {
            'admin': {
                'upload_files': True,
                'view_reports': True,
                'export_data': True,
                'manage_users': True,
                'view_logs': True,
                'advanced_filters': True
            },
            'user': {
                'upload_files': True,
                'view_reports': True,
                'export_data': True,
                'manage_users': False,
                'view_logs': False,
                'advanced_filters': True
            },
            'viewer': {
                'upload_files': False,
                'view_reports': True,
                'export_data': False,
                'manage_users': False,
                'view_logs': False,
                'advanced_filters': False
            }
        }
        
        return permissions.get(role, permissions['viewer'])
    
    def create_user(self, username: str, password: str, name: str, role: str = 'user') -> bool:
        """
        Cria um novo usuário.
        
        Args:
            username: Nome do usuário
            password: Senha do usuário
            name: Nome completo
            role: Papel do usuário
            
        Returns:
            True se criado com sucesso
        """
        username = username.lower().strip()
        
        if username in self.users:
            return False
        
        self.users[username] = {
            'password_hash': self._hash_password(password),
            'role': role,
            'name': name,
            'active': True
        }
        
        self._save_users(self.users)
        logger.info(f"Usuário criado: {username}")
        return True
    
    def update_password(self, username: str, new_password: str) -> bool:
        """Atualiza a senha de um usuário."""
        username = username.lower().strip()
        
        if username not in self.users:
            return False
        
        self.users[username]['password_hash'] = self._hash_password(new_password)
        self._save_users(self.users)
        logger.info(f"Senha atualizada para usuário: {username}")
        return True
    
    def deactivate_user(self, username: str) -> bool:
        """Desativa um usuário."""
        username = username.lower().strip()
        
        if username not in self.users:
            return False
        
        self.users[username]['active'] = False
        self._save_users(self.users)
        logger.info(f"Usuário desativado: {username}")
        return True

def render_login_form() -> Optional[Dict]:
    """
    Renderiza o formulário de login e gerencia a autenticação.
    
    Returns:
        Dados do usuário se autenticado, None caso contrário
    """
    auth_manager = AuthenticationManager()
    
    # Verificar se já está autenticado
    if st.session_state.get('authenticated', False):
        return st.session_state.get('user_data')
    
    # Renderizar formulário de login
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🔐 LogisticSmart v2.0</h1>
        <p style='color: #08c6ff; font-size: 1.2rem;'>Sistema Inteligente de Análise de Entregas</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.subheader("🚪 Acesso ao Sistema")
            
            username = st.text_input(
                "👤 Usuário:",
                placeholder="Digite seu nome de usuário",
                help="Use: admin, visitante ou neo"
            )
            
            password = st.text_input(
                "🔑 Senha:",
                type="password",
                placeholder="Digite sua senha"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_button = st.form_submit_button(
                    "🔓 Entrar",
                    use_container_width=True,
                    type="primary"
                )
            
            with col_btn2:
                demo_button = st.form_submit_button(
                    "👁️ Demo",
                    use_container_width=True,
                    help="Acesso de demonstração"
                )
    
    # Processar login
    if login_button and username and password:
        success, user_data = auth_manager.authenticate(username, password)
        
        if success:
            st.session_state.authenticated = True
            st.session_state.user_data = user_data
            st.success(f"✅ Bem-vindo, {user_data['name']}!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos!")
    
    # Processar demo
    if demo_button:
        success, user_data = auth_manager.authenticate("visitante", "fasebeta")
        if success:
            st.session_state.authenticated = True
            st.session_state.user_data = user_data
            st.info("🎯 Modo demonstração ativado!")
            st.rerun()
    
    # Informações de acesso
    with st.expander("ℹ️ Informações de Acesso"):
        st.markdown("""
        **Contas de Teste:**
        - **Admin**: admin / admin123
        - **Visitante**: visitante / fasebeta  
        - **Neo**: neo / matrix
        
        **Funcionalidades por Perfil:**
        - **Admin**: Acesso completo
        - **Visitante**: Apenas visualização
        - **Neo**: Acesso completo
        """)
    
    return None

def logout():
    """Realiza logout do usuário."""
    for key in ['authenticated', 'user_data']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def require_auth(min_role: str = 'viewer'):
    """
    Decorator para exigir autenticação.
    
    Args:
        min_role: Papel mínimo necessário
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_data = st.session_state.get('user_data')
            if not user_data:
                render_login_form()
                st.stop()
            
            # Verificar permissões se necessário
            role_hierarchy = {'viewer': 0, 'user': 1, 'admin': 2}
            user_level = role_hierarchy.get(user_data.get('role', 'viewer'), 0)
            required_level = role_hierarchy.get(min_role, 0)
            
            if user_level < required_level:
                st.error("🚫 Você não tem permissão para acessar esta funcionalidade!")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

