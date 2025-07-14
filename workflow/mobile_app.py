#!/usr/bin/env python3
"""
Mobile App Interface for Plumbers
Simplified interface for technicians in the field
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import os

class MobilePlumberApp:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.current_job = None
        self.technician_id = None
        
    def login(self, technician_id: str) -> bool:
        """Login as a technician"""
        self.technician_id = technician_id
        print(f"✅ Logged in as: {technician_id}")
        return True
    
    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get job details from the workflow system"""
        # In a real app, this would fetch from the workflow system
        # For demo, we'll create a sample job
        return {
            "id": job_id,
            "customer": {
                "name": "John Smith",
                "phone": "555-1234",
                "address": "123 Main St"
            },
            "description": "Kitchen sink is clogged and water won't drain",
            "priority": "medium",
            "estimated_duration": "1-2 hours"
        }
    
    def classify_issue_on_site(self, description: str) -> Dict:
        """Classify an issue using the API while on site"""
        try:
            payload = {
                "description": description
            }
            
            response = requests.post(
                f"{self.api_url}/classify",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_classification(description)
                
        except Exception as e:
            print(f"⚠️  API Error: {e}")
            return self._fallback_classification(description)
    
    def _fallback_classification(self, description: str) -> Dict:
        """Fallback when API is unavailable"""
        return {
            "classification": {
                "category": "other",
                "confidence": 0.5,
                "severity": "medium",
                "urgency": "medium",
                "estimated_duration": "1-2 hours",
                "required_tools": ["Basic tools"],
                "recommended_parts": ["Standard parts"],
                "safety_notes": ["Follow safety procedures"],
                "next_steps": ["Assess situation"]
            }
        }
    
    def start_job(self, job_id: str):
        """Start working on a job"""
        self.current_job = job_id
        print(f"🔧 Started job: {job_id}")
        print(f"   Technician: {self.technician_id}")
        print(f"   Time: {datetime.now().strftime('%H:%M')}")
    
    def update_job_status(self, status: str, notes: str = ""):
        """Update job status"""
        if not self.current_job:
            print("❌ No active job")
            return
        
        print(f"📝 Job {self.current_job} - {status}")
        if notes:
            print(f"   Notes: {notes}")
    
    def get_tools_checklist(self, job_data: Dict) -> List[str]:
        """Get tools checklist for the job"""
        classification = job_data.get("classification", {})
        tools = classification.get("required_tools", [])
        
        # Add common tools
        common_tools = ["Safety glasses", "Gloves", "Flashlight"]
        all_tools = common_tools + tools
        
        return all_tools
    
    def get_safety_checklist(self, job_data: Dict) -> List[str]:
        """Get safety checklist for the job"""
        classification = job_data.get("classification", {})
        safety_notes = classification.get("safety_notes", [])
        
        # Add common safety items
        common_safety = [
            "Turn off water supply",
            "Check for electrical hazards",
            "Wear appropriate PPE"
        ]
        
        return common_safety + safety_notes
    
    def complete_job(self, notes: str = "", parts_used: List[str] = None):
        """Complete the current job"""
        if not self.current_job:
            print("❌ No active job")
            return
        
        print(f"✅ Completed job: {self.current_job}")
        print(f"   Technician: {self.technician_id}")
        print(f"   Completion time: {datetime.now().strftime('%H:%M')}")
        
        if notes:
            print(f"   Notes: {notes}")
        
        if parts_used:
            print(f"   Parts used: {', '.join(parts_used)}")
        
        self.current_job = None
    
    def display_mobile_interface(self):
        """Display the mobile interface"""
        print("\n" + "="*50)
        print("📱 MOBILE PLUMBER APP")
        print("="*50)
        
        if self.technician_id:
            print(f"👤 Technician: {self.technician_id}")
        
        if self.current_job:
            print(f"🔧 Active Job: {self.current_job}")
        else:
            print("⏳ No active job")
        
        print("\n📋 Quick Actions:")
        print("   1. Start New Job")
        print("   2. View Current Job")
        print("   3. Update Job Status")
        print("   4. Complete Job")
        print("   5. Classify Issue")
        print("   6. View Tools Checklist")
        print("   7. View Safety Checklist")
        print("   8. Exit")
    
    def run_mobile_demo(self):
        """Run a mobile app demonstration"""
        print("📱 Mobile Plumber App Demo")
        print("Simulating technician workflow in the field...")
        
        # Login
        self.login("Mike Johnson")
        
        # Get a job
        job_data = self.get_job_details("JOB-0001")
        
        # Start the job
        self.start_job("JOB-0001")
        
        # Classify issue on site
        print("\n🔍 Classifying issue on site...")
        result = self.classify_issue_on_site("Kitchen sink is clogged and water won't drain")
        classification = result["classification"]
        
        print(f"✅ Classification Results:")
        print(f"   Category: {classification['category']}")
        print(f"   Severity: {classification['severity']}")
        print(f"   Estimated Duration: {classification['estimated_duration']}")
        
        # Show tools checklist
        print(f"\n🛠️  Tools Checklist:")
        tools = self.get_tools_checklist(result)
        for i, tool in enumerate(tools, 1):
            print(f"   {i}. {tool}")
        
        # Show safety checklist
        print(f"\n⚠️  Safety Checklist:")
        safety_items = self.get_safety_checklist(result)
        for i, item in enumerate(safety_items, 1):
            print(f"   {i}. {item}")
        
        # Update job status
        self.update_job_status("In Progress", "Assessing the clog")
        
        # Complete job
        self.complete_job(
            notes="Replaced drain trap, cleared blockage",
            parts_used=["New drain trap", "Plumber's putty"]
        )
        
        # Show mobile interface
        self.display_mobile_interface()
        
        print("\n✅ Mobile app demo completed!")

def main():
    """Main mobile app demonstration"""
    app = MobilePlumberApp()
    app.run_mobile_demo()

if __name__ == "__main__":
    main() 