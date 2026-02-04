import pytest
from datetime import datetime, timedelta
from app.utils.jwt import JWTHandler
from app.utils.password import PasswordHasher


class TestJWTHandler:
    def setup_method(self):
        self.jwt_handler = JWTHandler()
    
    def test_create_table_token(self):
        token = self.jwt_handler.create_table_token(
            store_id=1,
            table_id=1,
            table_number=5,
            session_id=10
        )
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_admin_token(self):
        token = self.jwt_handler.create_admin_token(
            store_id=1,
            user_id=1,
            username="admin"
        )
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_table_token(self):
        token = self.jwt_handler.create_table_token(
            store_id=1,
            table_id=1,
            table_number=5,
            session_id=10
        )
        payload = self.jwt_handler.verify_token(token, token_type="table")
        
        assert payload.token_type == "table"
        assert payload.store_id == 1
        assert payload.table_id == 1
        assert payload.table_number == 5
        assert payload.session_id == 10
    
    def test_verify_admin_token(self):
        token = self.jwt_handler.create_admin_token(
            store_id=1,
            user_id=1,
            username="admin"
        )
        payload = self.jwt_handler.verify_token(token, token_type="admin")
        
        assert payload.token_type == "admin"
        assert payload.store_id == 1
        assert payload.user_id == 1
        assert payload.username == "admin"
    
    def test_verify_wrong_token_type(self):
        token = self.jwt_handler.create_table_token(
            store_id=1,
            table_id=1,
            table_number=5,
            session_id=10
        )
        with pytest.raises(Exception):
            self.jwt_handler.verify_token(token, token_type="admin")
    
    def test_verify_invalid_token(self):
        with pytest.raises(Exception):
            self.jwt_handler.verify_token("invalid-token", token_type="table")


class TestPasswordHasher:
    def setup_method(self):
        self.hasher = PasswordHasher()
    
    def test_hash_password(self):
        password = "test1234"
        hashed = self.hasher.hash(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password_correct(self):
        password = "test1234"
        hashed = self.hasher.hash(password)
        
        assert self.hasher.verify(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        password = "test1234"
        hashed = self.hasher.hash(password)
        
        assert self.hasher.verify("wrong-password", hashed) is False
    
    def test_different_hashes_for_same_password(self):
        password = "test1234"
        hash1 = self.hasher.hash(password)
        hash2 = self.hasher.hash(password)
        
        # bcrypt generates different hashes each time
        assert hash1 != hash2
        # But both should verify correctly
        assert self.hasher.verify(password, hash1) is True
        assert self.hasher.verify(password, hash2) is True
