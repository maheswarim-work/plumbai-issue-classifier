import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPlumbingIssueClassifierAPI:
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Smart Plumbing Issue Classifier API" in data["message"]
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model_loaded" in data
        assert "version" in data
        assert "uptime_seconds" in data
    
    def test_categories_endpoint(self):
        """Test the categories endpoint"""
        response = client.get("/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "descriptions" in data
        assert len(data["categories"]) > 0
    
    def test_severity_levels_endpoint(self):
        """Test the severity levels endpoint"""
        response = client.get("/severity-levels")
        assert response.status_code == 200
        data = response.json()
        assert "severity_levels" in data
        assert "descriptions" in data
        assert len(data["severity_levels"]) > 0
    
    def test_urgency_levels_endpoint(self):
        """Test the urgency levels endpoint"""
        response = client.get("/urgency-levels")
        assert response.status_code == 200
        data = response.json()
        assert "urgency_levels" in data
        assert "descriptions" in data
        assert len(data["urgency_levels"]) > 0
    
    def test_classify_leak_issue(self):
        """Test classification of a leak issue"""
        request_data = {
            "description": "Water is leaking from under the kitchen sink",
            "customer_name": "John Doe",
            "phone_number": "555-1234",
            "address": "123 Main St"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "request_id" in data
        assert "classification" in data
        assert "processing_time_ms" in data
        assert "model_version" in data
        
        classification = data["classification"]
        assert classification["category"] == "leak"
        assert classification["confidence"] > 0.5
        assert "pipe wrench" in classification["required_tools"]
    
    def test_classify_clog_issue(self):
        """Test classification of a clog issue"""
        request_data = {
            "description": "Kitchen sink is clogged and water won't drain"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        classification = data["classification"]
        assert classification["category"] == "clog"
        assert classification["confidence"] > 0.5
    
    def test_classify_water_heater_issue(self):
        """Test classification of a water heater issue"""
        request_data = {
            "description": "No hot water coming from faucet"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        classification = data["classification"]
        assert classification["category"] == "water_heater"
        assert classification["confidence"] > 0.5
    
    def test_classify_emergency_issue(self):
        """Test classification of an emergency issue"""
        request_data = {
            "description": "Emergency! Pipe burst and water is flooding the basement"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        classification = data["classification"]
        assert classification["urgency"] == "emergency"
        assert classification["severity"] == "critical"
        assert "Dispatch emergency technician" in classification["next_steps"][0]
    
    def test_invalid_request_missing_description(self):
        """Test handling of invalid request without description"""
        request_data = {
            "customer_name": "John Doe"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_request_empty_description(self):
        """Test handling of empty description"""
        request_data = {
            "description": ""
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_request_short_description(self):
        """Test handling of description that's too short"""
        request_data = {
            "description": "Leak"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_classification_response_structure(self):
        """Test that classification response has all required fields"""
        request_data = {
            "description": "Faucet is dripping"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Check main response structure
        required_fields = ["request_id", "classification", "processing_time_ms", "model_version"]
        for field in required_fields:
            assert field in data
        
        # Check classification structure
        classification = data["classification"]
        required_classification_fields = [
            "category", "confidence", "severity", "urgency", 
            "estimated_duration", "required_tools", "recommended_parts",
            "safety_notes", "next_steps"
        ]
        for field in required_classification_fields:
            assert field in classification
        
        # Check data types
        assert isinstance(data["request_id"], str)
        assert isinstance(data["processing_time_ms"], (int, float))
        assert isinstance(data["model_version"], str)
        assert isinstance(classification["confidence"], (int, float))
        assert isinstance(classification["required_tools"], list)
        assert isinstance(classification["recommended_parts"], list)
        assert isinstance(classification["safety_notes"], list)
        assert isinstance(classification["next_steps"], list)
    
    def test_processing_time_reasonable(self):
        """Test that processing time is reasonable"""
        request_data = {
            "description": "Sink is clogged"
        }
        
        response = client.post("/classify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Processing time should be reasonable (less than 1 second)
        assert data["processing_time_ms"] > 0
        assert data["processing_time_ms"] < 1000 