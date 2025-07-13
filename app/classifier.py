import re
import time
from typing import Dict, List, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os
from .models import IssueCategory, IssueSeverity, IssueUrgency

class PlumbingIssueClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.categories = list(IssueCategory)
        self.severity_keywords = {
            IssueSeverity.LOW: ['slow', 'minor', 'small', 'slight', 'drip'],
            IssueSeverity.MEDIUM: ['moderate', 'medium', 'noticeable', 'consistent'],
            IssueSeverity.HIGH: ['major', 'significant', 'serious', 'bad', 'severe'],
            IssueSeverity.CRITICAL: ['emergency', 'flooding', 'burst', 'overflow', 'urgent', 'critical']
        }
        self.urgency_keywords = {
            IssueUrgency.LOW: ['when convenient', 'no rush', 'sometime', 'non-urgent'],
            IssueUrgency.MEDIUM: ['soon', 'asap', 'quickly', 'prompt'],
            IssueUrgency.HIGH: ['urgent', 'immediate', 'right away', 'emergency'],
            IssueUrgency.EMERGENCY: ['emergency', 'flooding', 'burst', 'overflow', 'urgent', 'critical', 'now']
        }
        self.category_keywords = {
            IssueCategory.LEAK: ['leak', 'drip', 'water', 'wet', 'moisture', 'puddle'],
            IssueCategory.CLOG: ['clog', 'blocked', 'slow drain', 'backup', 'overflow'],
            IssueCategory.WATER_HEATER: ['hot water', 'heater', 'warm', 'temperature', 'heating'],
            IssueCategory.FAUCET: ['faucet', 'tap', 'handle', 'spout', 'aerator'],
            IssueCategory.TOILET: ['toilet', 'flush', 'bowl', 'tank', 'seat'],
            IssueCategory.DRAIN: ['drain', 'sink', 'tub', 'shower', 'basin'],
            IssueCategory.PIPE: ['pipe', 'fitting', 'joint', 'connection', 'line'],
            IssueCategory.SEWER: ['sewer', 'main line', 'septic', 'backup', 'smell'],
            IssueCategory.GARBAGE_DISPOSAL: ['disposal', 'grinder', 'garbage', 'food waste'],
            IssueCategory.WATER_PRESSURE: ['pressure', 'low flow', 'weak', 'strong', 'force']
        }
        
        self.tools_by_category = {
            IssueCategory.LEAK: ['pipe wrench', 'plumber\'s tape', 'soldering torch', 'pipe cutter'],
            IssueCategory.CLOG: ['plunger', 'drain snake', 'auger', 'chemical cleaner'],
            IssueCategory.WATER_HEATER: ['multimeter', 'thermostat', 'element wrench', 'pipe wrench'],
            IssueCategory.FAUCET: ['faucet wrench', 'screwdriver', 'plumber\'s tape', 'cartridge puller'],
            IssueCategory.TOILET: ['toilet auger', 'wax ring', 'closet bolts', 'tank repair kit'],
            IssueCategory.DRAIN: ['drain snake', 'plunger', 'chemical cleaner', 'auger'],
            IssueCategory.PIPE: ['pipe wrench', 'pipe cutter', 'soldering torch', 'fittings'],
            IssueCategory.SEWER: ['sewer snake', 'camera', 'rooter', 'hydro jet'],
            IssueCategory.GARBAGE_DISPOSAL: ['hex wrench', 'allen wrench', 'replacement parts'],
            IssueCategory.WATER_PRESSURE: ['pressure gauge', 'pressure regulator', 'pipe wrench']
        }
        
        self.parts_by_category = {
            IssueCategory.LEAK: ['pipe fittings', 'soldering materials', 'pipe sections'],
            IssueCategory.CLOG: ['drain cleaner', 'replacement drain parts'],
            IssueCategory.WATER_HEATER: ['thermostat', 'heating element', 'anode rod'],
            IssueCategory.FAUCET: ['faucet cartridge', 'o-rings', 'aerator', 'handle'],
            IssueCategory.TOILET: ['flapper', 'fill valve', 'flush valve', 'wax ring'],
            IssueCategory.DRAIN: ['drain trap', 'drain pipe', 'cleanout plug'],
            IssueCategory.PIPE: ['pipe sections', 'fittings', 'soldering materials'],
            IssueCategory.SEWER: ['sewer pipe', 'cleanout cap', 'root treatment'],
            IssueCategory.GARBAGE_DISPOSAL: ['disposal unit', 'mounting hardware'],
            IssueCategory.WATER_PRESSURE: ['pressure regulator', 'pressure gauge']
        }
        
        self.safety_notes_by_category = {
            IssueCategory.LEAK: ['Turn off water supply before repairs', 'Check for electrical hazards near water'],
            IssueCategory.CLOG: ['Use appropriate PPE when using chemicals', 'Avoid harsh chemicals on older pipes'],
            IssueCategory.WATER_HEATER: ['Turn off power/gas before service', 'Check for gas leaks'],
            IssueCategory.FAUCET: ['Turn off water supply', 'Check for hot water scalding'],
            IssueCategory.TOILET: ['Turn off water supply', 'Use proper lifting techniques'],
            IssueCategory.DRAIN: ['Use appropriate PPE', 'Ventilate area when using chemicals'],
            IssueCategory.PIPE: ['Turn off water supply', 'Check for gas leaks if near gas lines'],
            IssueCategory.SEWER: ['Use appropriate PPE', 'Ventilate area', 'Check for gas buildup'],
            IssueCategory.GARBAGE_DISPOSAL: ['Turn off power before service', 'Never put hand in disposal'],
            IssueCategory.WATER_PRESSURE: ['Check for burst pipes', 'Monitor for leaks after adjustment']
        }
        
        self.duration_estimates = {
            IssueCategory.LEAK: '1-3 hours',
            IssueCategory.CLOG: '30 minutes - 2 hours',
            IssueCategory.WATER_HEATER: '2-4 hours',
            IssueCategory.FAUCET: '1-2 hours',
            IssueCategory.TOILET: '1-2 hours',
            IssueCategory.DRAIN: '30 minutes - 2 hours',
            IssueCategory.PIPE: '2-4 hours',
            IssueCategory.SEWER: '2-6 hours',
            IssueCategory.GARBAGE_DISPOSAL: '1-2 hours',
            IssueCategory.WATER_PRESSURE: '1-3 hours'
        }
        
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load pre-trained model or train a new one with sample data"""
        model_path = 'plumbing_classifier_model.pkl'
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self._train_model()
    
    def _train_model(self):
        """Train the classifier with sample plumbing issue data"""
        # Sample training data - in production, this would come from real customer data
        training_data = [
            ("water is leaking from under the sink", "leak"),
            ("kitchen sink is clogged and water won't drain", "clog"),
            ("no hot water coming from faucet", "water_heater"),
            ("faucet handle is loose and dripping", "faucet"),
            ("toilet won't flush properly", "toilet"),
            ("bathroom drain is slow", "drain"),
            ("pipe burst in basement", "pipe"),
            ("sewer line is backing up", "sewer"),
            ("garbage disposal is making noise", "garbage_disposal"),
            ("water pressure is very low", "water_pressure"),
            ("sink is making noise", "faucet"),
            ("no hot water", "water_heater"),
            ("drain is blocked", "clog"),
            ("pipe is leaking", "leak"),
            ("toilet is running", "toilet"),
            ("shower drain is slow", "drain"),
            ("water heater is not working", "water_heater"),
            ("faucet is dripping", "faucet"),
            ("sewer smell in yard", "sewer"),
            ("disposal is jammed", "garbage_disposal"),
            ("pressure is too high", "water_pressure"),
            ("pipe is frozen", "pipe"),
            ("drain is overflowing", "clog"),
            ("water is brown", "water_heater"),
            ("faucet handle broke", "faucet"),
            ("toilet is clogged", "toilet"),
            ("sink is backing up", "drain"),
            ("main line is blocked", "sewer"),
            ("disposal won't turn on", "garbage_disposal"),
            ("pressure regulator failed", "water_pressure"),
            ("pipe is corroded", "pipe"),
            ("water is leaking from ceiling", "leak"),
            ("drain is making gurgling noise", "clog"),
            ("heater pilot light won't stay lit", "water_heater"),
            ("faucet aerator is clogged", "faucet"),
            ("toilet tank is leaking", "toilet"),
            ("bathroom sink is slow", "drain"),
            ("sewer cleanout is overflowing", "sewer"),
            ("disposal is leaking", "garbage_disposal"),
            ("pressure valve is faulty", "water_pressure"),
            ("pipe joint is leaking", "pipe"),
        ]
        
        texts, labels = zip(*training_data)
        
        # Create and train the pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('clf', MultinomialNB())
        ])
        
        self.model.fit(texts, labels)
        
        # Save the model
        with open('plumbing_classifier_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
    
    def classify_issue(self, description: str) -> Dict[str, Any]:
        """Classify a plumbing issue based on the description"""
        start_time = time.time()
        
        # Clean and preprocess the description
        cleaned_description = self._preprocess_text(description.lower())
        
        # Predict category
        predicted_category = self.model.predict([cleaned_description])[0]
        confidence = max(self.model.predict_proba([cleaned_description])[0])
        
        # Determine severity and urgency
        severity = self._determine_severity(cleaned_description)
        urgency = self._determine_urgency(cleaned_description)
        
        # Get category enum
        category_enum = IssueCategory(predicted_category)
        
        # Get recommendations
        tools = self.tools_by_category.get(category_enum, [])
        parts = self.parts_by_category.get(category_enum, [])
        safety_notes = self.safety_notes_by_category.get(category_enum, [])
        duration = self.duration_estimates.get(category_enum, '1-2 hours')
        
        # Generate next steps
        next_steps = self._generate_next_steps(category_enum, severity, urgency)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return {
            'category': category_enum,
            'confidence': confidence,
            'severity': severity,
            'urgency': urgency,
            'estimated_duration': duration,
            'required_tools': tools,
            'recommended_parts': parts,
            'safety_notes': safety_notes,
            'next_steps': next_steps,
            'processing_time_ms': processing_time
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess the input text"""
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _determine_severity(self, text: str) -> IssueSeverity:
        """Determine issue severity based on keywords"""
        text_lower = text.lower()
        
        for severity, keywords in self.severity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return severity
        
        # Default to medium if no specific keywords found
        return IssueSeverity.MEDIUM
    
    def _determine_urgency(self, text: str) -> IssueUrgency:
        """Determine issue urgency based on keywords"""
        text_lower = text.lower()
        
        for urgency, keywords in self.urgency_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return urgency
        
        # Default to medium if no specific keywords found
        return IssueUrgency.MEDIUM
    
    def _generate_next_steps(self, category: IssueCategory, severity: IssueSeverity, urgency: IssueUrgency) -> List[str]:
        """Generate appropriate next steps based on classification"""
        steps = []
        
        # Emergency steps
        if urgency == IssueUrgency.EMERGENCY:
            steps.append("Dispatch emergency technician immediately")
            steps.append("Contact customer to confirm address and access")
        
        # High urgency steps
        elif urgency == IssueUrgency.HIGH:
            steps.append("Schedule technician within 2-4 hours")
            steps.append("Contact customer to confirm availability")
        
        # Standard steps
        else:
            steps.append("Schedule technician within 24-48 hours")
            steps.append("Send confirmation email to customer")
        
        # Category-specific steps
        if category == IssueCategory.LEAK:
            steps.append("Instruct customer to turn off water supply if possible")
            steps.append("Prepare leak detection equipment")
        elif category == IssueCategory.CLOG:
            steps.append("Bring appropriate drain cleaning tools")
            steps.append("Check if customer has tried DIY solutions")
        elif category == IssueCategory.WATER_HEATER:
            steps.append("Bring multimeter and testing equipment")
            steps.append("Check warranty status if applicable")
        elif category == IssueCategory.SEWER:
            steps.append("Bring sewer camera and rooter equipment")
            steps.append("Check for city sewer line responsibility")
        
        # Severity-specific steps
        if severity in [IssueSeverity.HIGH, IssueSeverity.CRITICAL]:
            steps.append("Bring backup technician if needed")
            steps.append("Prepare for potential emergency parts ordering")
        
        return steps 