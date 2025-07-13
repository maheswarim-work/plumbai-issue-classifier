import pytest
from app.classifier import PlumbingIssueClassifier
from app.models import IssueCategory, IssueSeverity, IssueUrgency

class TestPlumbingIssueClassifier:
    
    @pytest.fixture
    def classifier(self):
        """Create a classifier instance for testing"""
        return PlumbingIssueClassifier()
    
    def test_classify_leak_issue(self, classifier):
        """Test classification of a leak issue"""
        result = classifier.classify_issue("Water is leaking from under the kitchen sink")
        
        assert result['category'] == IssueCategory.LEAK
        assert result['confidence'] > 0.5
        assert result['severity'] in [IssueSeverity.MEDIUM, IssueSeverity.HIGH]
        assert 'pipe wrench' in result['required_tools']
        assert 'Turn off water supply' in result['safety_notes'][0]
    
    def test_classify_clog_issue(self, classifier):
        """Test classification of a clog issue"""
        result = classifier.classify_issue("Kitchen sink is clogged and water won't drain")
        
        assert result['category'] == IssueCategory.CLOG
        assert result['confidence'] > 0.5
        assert 'plunger' in result['required_tools'] or 'drain snake' in result['required_tools']
    
    def test_classify_water_heater_issue(self, classifier):
        """Test classification of a water heater issue"""
        result = classifier.classify_issue("No hot water coming from faucet")
        
        assert result['category'] == IssueCategory.WATER_HEATER
        assert result['confidence'] > 0.5
        assert 'multimeter' in result['required_tools']
    
    def test_classify_faucet_issue(self, classifier):
        """Test classification of a faucet issue"""
        result = classifier.classify_issue("Faucet handle is loose and dripping")
        
        assert result['category'] == IssueCategory.FAUCET
        assert result['confidence'] > 0.5
        assert 'faucet wrench' in result['required_tools']
    
    def test_classify_toilet_issue(self, classifier):
        """Test classification of a toilet issue"""
        result = classifier.classify_issue("Toilet won't flush properly")
        
        assert result['category'] == IssueCategory.TOILET
        assert result['confidence'] > 0.5
        assert 'toilet auger' in result['required_tools']
    
    def test_emergency_urgency_detection(self, classifier):
        """Test detection of emergency urgency"""
        result = classifier.classify_issue("Emergency! Pipe burst and water is flooding the basement")
        
        assert result['urgency'] == IssueUrgency.EMERGENCY
        assert result['severity'] == IssueSeverity.CRITICAL
        assert "Dispatch emergency technician" in result['next_steps'][0]
    
    def test_critical_severity_detection(self, classifier):
        """Test detection of critical severity"""
        result = classifier.classify_issue("Critical pipe burst causing major flooding")
        
        assert result['severity'] == IssueSeverity.CRITICAL
        assert result['urgency'] == IssueUrgency.EMERGENCY
    
    def test_low_severity_detection(self, classifier):
        """Test detection of low severity"""
        result = classifier.classify_issue("Slight drip from faucet")
        
        assert result['severity'] == IssueSeverity.LOW
    
    def test_text_preprocessing(self, classifier):
        """Test text preprocessing functionality"""
        dirty_text = "Water is leaking!!! from under the sink... (urgent)"
        cleaned = classifier._preprocess_text(dirty_text)
        
        assert "!!!" not in cleaned
        assert "..." not in cleaned
        assert "(" not in cleaned
        assert ")" not in cleaned
    
    def test_duration_estimates(self, classifier):
        """Test that duration estimates are provided"""
        result = classifier.classify_issue("Sink is clogged")
        
        assert result['estimated_duration'] is not None
        assert isinstance(result['estimated_duration'], str)
        assert len(result['estimated_duration']) > 0
    
    def test_safety_notes_presence(self, classifier):
        """Test that safety notes are provided"""
        result = classifier.classify_issue("Water heater not working")
        
        assert len(result['safety_notes']) > 0
        assert all(isinstance(note, str) for note in result['safety_notes'])
    
    def test_next_steps_generation(self, classifier):
        """Test that next steps are generated"""
        result = classifier.classify_issue("Sewer line backing up")
        
        assert len(result['next_steps']) > 0
        assert all(isinstance(step, str) for step in result['next_steps'])
    
    def test_confidence_scores(self, classifier):
        """Test that confidence scores are reasonable"""
        result = classifier.classify_issue("Kitchen sink is clogged")
        
        assert 0.0 <= result['confidence'] <= 1.0
        assert result['confidence'] > 0.1  # Should have some confidence
    
    def test_processing_time(self, classifier):
        """Test that processing time is recorded"""
        result = classifier.classify_issue("Faucet is dripping")
        
        assert 'processing_time_ms' in result
        assert result['processing_time_ms'] > 0
        assert result['processing_time_ms'] < 1000  # Should be fast
    
    def test_unknown_issue_fallback(self, classifier):
        """Test handling of unknown issue types"""
        result = classifier.classify_issue("Something very unusual is happening with my plumbing")
        
        # Should still return a valid classification
        assert result['category'] in IssueCategory
        assert result['severity'] in IssueSeverity
        assert result['urgency'] in IssueUrgency 