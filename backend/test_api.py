import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_supabase():
    """Mock Supabase clients"""
    with patch('app.supabase_admin') as mock_admin, \
         patch('app.supabase_client') as mock_client:
        yield mock_admin, mock_client

class TestUserEndpoints:
    """Test class for user-related API endpoints"""
    
    def test_home_endpoint(self, client):
        """Test the home endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data.decode() == "Welcome to the NBA IQ App!"
    
    def test_create_user_success(self, client, mock_supabase):
        """Test successful user creation"""
        mock_admin, mock_client = mock_supabase
        
        # Mock existing user check (no existing user)
        mock_admin.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        # Mock successful user creation
        mock_response = MagicMock()
        mock_response.data = [{
            "id": "test-user-123",
            "full_name": "Test User",
            "email": "test@example.com",
            "avatar_url": "https://example.com/avatar.jpg"
        }]
        mock_admin.table.return_value.insert.return_value.execute.return_value = mock_response
        
        user_data = {
            "user_id": "test-user-123",
            "email": "test@example.com",
            "full_name": "Test User",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        
        response = client.post('/api/users', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "User created successfully"
        assert data["user"]["id"] == "test-user-123"
    
    def test_create_user_already_exists(self, client, mock_supabase):
        """Test user creation when user already exists"""
        mock_admin, mock_client = mock_supabase
        
        # Mock existing user
        existing_user_data = [{"id": "test-user-123"}]
        mock_admin.table.return_value.select.return_value.eq.return_value.execute.return_value.data = existing_user_data
        
        user_data = {
            "user_id": "test-user-123",
            "email": "test@example.com",
            "full_name": "Test User",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        
        response = client.post('/api/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "User already exists"
    
    def test_create_user_missing_required_fields(self, client):
        """Test user creation with missing required fields"""
        incomplete_data = {
            "user_id": "test-user-123",
            "email": "test@example.com"
            # Missing full_name
        }
        
        response = client.post('/api/users',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Missing required fields" in data["error"]
    
    def test_create_user_database_error(self, client, mock_supabase):
        """Test user creation when database insertion fails"""
        mock_admin, mock_client = mock_supabase
        
        # Mock no existing user
        mock_admin.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        # Mock failed insertion (no data returned)
        mock_response = MagicMock()
        mock_response.data = None
        mock_admin.table.return_value.insert.return_value.execute.return_value = mock_response
        
        user_data = {
            "user_id": "test-user-123",
            "email": "test@example.com",
            "full_name": "Test User",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        
        response = client.post('/api/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["error"] == "Failed to create user"
    
    def test_get_user_success(self, client, mock_supabase):
        """Test successful user retrieval"""
        mock_admin, mock_client = mock_supabase
        
        # Mock successful token verification
        mock_user = MagicMock()
        mock_client.auth.get_user.return_value.user = mock_user
        
        # Mock successful user retrieval from database
        user_data = {
            "id": "test-user-123",
            "full_name": "Test User",
            "email": "test@example.com",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        mock_admin.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [user_data]
        
        headers = {"Authorization": "Bearer valid-jwt-token"}
        response = client.get('/api/users/test-user-123', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == "test-user-123"
        assert data["full_name"] == "Test User"
    
    def test_get_user_missing_authorization(self, client):
        """Test user retrieval without authorization header"""
        response = client.get('/api/users/test-user-123')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Missing or invalid Authorization header"
    
    def test_get_user_invalid_authorization_format(self, client):
        """Test user retrieval with invalid authorization header format"""
        headers = {"Authorization": "InvalidFormat token"}
        response = client.get('/api/users/test-user-123', headers=headers)
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Missing or invalid Authorization header"
    
    def test_get_user_invalid_token(self, client, mock_supabase):
        """Test user retrieval with invalid JWT token"""
        mock_admin, mock_client = mock_supabase
        
        # Mock invalid token (no user returned)
        mock_client.auth.get_user.return_value.user = None
        
        headers = {"Authorization": "Bearer invalid-jwt-token"}
        response = client.get('/api/users/test-user-123', headers=headers)
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Invalid token"
    
    def test_get_user_not_found(self, client, mock_supabase):
        """Test user retrieval when user doesn't exist in database"""
        mock_admin, mock_client = mock_supabase
        
        # Mock successful token verification
        mock_user = MagicMock()
        mock_client.auth.get_user.return_value.user = mock_user
        
        # Mock user not found in database
        mock_admin.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        headers = {"Authorization": "Bearer valid-jwt-token"}
        response = client.get('/api/users/nonexistent-user', headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["error"] == "User not found"
    
    def test_get_user_server_error(self, client, mock_supabase):
        """Test user retrieval when server error occurs"""
        mock_admin, mock_client = mock_supabase
        
        # Mock exception during token verification
        mock_client.auth.get_user.side_effect = Exception("Database connection error")
        
        headers = {"Authorization": "Bearer valid-jwt-token"}
        response = client.get('/api/users/test-user-123', headers=headers)
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["error"] == "Internal server error"

if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])
