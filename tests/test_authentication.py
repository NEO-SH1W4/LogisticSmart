"""
Testes para o módulo de autenticação.
"""
import pytest
import tempfile
import json
from pathlib import Path

from src.auth.authentication import AuthenticationManager


class TestAuthenticationManager:
    """Testes para a classe AuthenticationManager."""
    
    def setup_method(self):
        """Setup para cada teste."""
        # Usar arquivo temporário para não interferir com dados reais
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.auth_manager = AuthenticationManager(Path(self.temp_file.name))
    
    def teardown_method(self):
        """Cleanup após cada teste."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_init_creates_default_users(self):
        """Testa se usuários padrão são criados na inicialização."""
        assert 'admin' in self.auth_manager.users
        assert 'visitante' in self.auth_manager.users
        assert 'neo' in self.auth_manager.users
    
    def test_hash_password(self):
        """Testa geração de hash de senha."""
        password = "test123"
        hashed = self.auth_manager._hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 50  # bcrypt hash é longo
    
    def test_verify_password_correct(self):
        """Testa verificação de senha correta."""
        password = "test123"
        hashed = self.auth_manager._hash_password(password)
        
        assert self.auth_manager._verify_password(password, hashed)
    
    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta."""
        password = "test123"
        wrong_password = "wrong"
        hashed = self.auth_manager._hash_password(password)
        
        assert not self.auth_manager._verify_password(wrong_password, hashed)
    
    def test_authenticate_success(self):
        """Testa autenticação bem-sucedida."""
        success, user_data = self.auth_manager.authenticate("admin", "admin123")
        
        assert success
        assert user_data is not None
        assert user_data['username'] == 'admin'
        assert user_data['role'] == 'admin'
        assert 'permissions' in user_data
    
    def test_authenticate_wrong_password(self):
        """Testa autenticação com senha errada."""
        success, user_data = self.auth_manager.authenticate("admin", "wrongpassword")
        
        assert not success
        assert user_data is None
    
    def test_authenticate_nonexistent_user(self):
        """Testa autenticação com usuário inexistente."""
        success, user_data = self.auth_manager.authenticate("nonexistent", "password")
        
        assert not success
        assert user_data is None
    
    def test_authenticate_inactive_user(self):
        """Testa autenticação com usuário inativo."""
        # Criar usuário inativo
        self.auth_manager.users['inactive'] = {
            'password_hash': self.auth_manager._hash_password('test'),
            'role': 'user',
            'name': 'Inactive User',
            'active': False
        }
        
        success, user_data = self.auth_manager.authenticate("inactive", "test")
        
        assert not success
        assert user_data is None
    
    def test_create_user_success(self):
        """Testa criação de usuário bem-sucedida."""
        success = self.auth_manager.create_user(
            "newuser", "password123", "New User", "user"
        )
        
        assert success
        assert "newuser" in self.auth_manager.users
        assert self.auth_manager.users["newuser"]["name"] == "New User"
        assert self.auth_manager.users["newuser"]["role"] == "user"
        assert self.auth_manager.users["newuser"]["active"]
    
    def test_create_user_already_exists(self):
        """Testa criação de usuário que já existe."""
        success = self.auth_manager.create_user(
            "admin", "password123", "Admin User", "admin"
        )
        
        assert not success
    
    def test_update_password_success(self):
        """Testa atualização de senha bem-sucedida."""
        old_hash = self.auth_manager.users['admin']['password_hash']
        
        success = self.auth_manager.update_password("admin", "newpassword")
        
        assert success
        new_hash = self.auth_manager.users['admin']['password_hash']
        assert new_hash != old_hash
        
        # Verificar se nova senha funciona
        success, _ = self.auth_manager.authenticate("admin", "newpassword")
        assert success
    
    def test_update_password_nonexistent_user(self):
        """Testa atualização de senha para usuário inexistente."""
        success = self.auth_manager.update_password("nonexistent", "newpassword")
        
        assert not success
    
    def test_deactivate_user_success(self):
        """Testa desativação de usuário bem-sucedida."""
        success = self.auth_manager.deactivate_user("admin")
        
        assert success
        assert not self.auth_manager.users['admin']['active']
    
    def test_deactivate_user_nonexistent(self):
        """Testa desativação de usuário inexistente."""
        success = self.auth_manager.deactivate_user("nonexistent")
        
        assert not success
    
    def test_get_permissions_admin(self):
        """Testa permissões para usuário admin."""
        permissions = self.auth_manager._get_permissions('admin')
        
        assert permissions['upload_files']
        assert permissions['view_reports']
        assert permissions['export_data']
        assert permissions['manage_users']
        assert permissions['view_logs']
        assert permissions['advanced_filters']
    
    def test_get_permissions_user(self):
        """Testa permissões para usuário comum."""
        permissions = self.auth_manager._get_permissions('user')
        
        assert permissions['upload_files']
        assert permissions['view_reports']
        assert permissions['export_data']
        assert not permissions['manage_users']
        assert not permissions['view_logs']
        assert permissions['advanced_filters']
    
    def test_get_permissions_viewer(self):
        """Testa permissões para visitante."""
        permissions = self.auth_manager._get_permissions('viewer')
        
        assert not permissions['upload_files']
        assert permissions['view_reports']
        assert not permissions['export_data']
        assert not permissions['manage_users']
        assert not permissions['view_logs']
        assert not permissions['advanced_filters']
    
    def test_save_and_load_users(self):
        """Testa salvamento e carregamento de usuários."""
        # Criar novo usuário
        self.auth_manager.create_user("testuser", "testpass", "Test User", "user")
        
        # Criar novo gerenciador com mesmo arquivo
        new_auth_manager = AuthenticationManager(Path(self.temp_file.name))
        
        # Verificar se usuário foi persistido
        assert "testuser" in new_auth_manager.users
        assert new_auth_manager.users["testuser"]["name"] == "Test User"

