#!/usr/bin/env python3
"""
Plumber Dashboard - Workflow Management System
Integrates with Smart Plumbing Issue Classifier API
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dataclasses import dataclass
from enum import Enum

# API Configuration
API_BASE_URL = "http://localhost:8000"

class JobStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PriorityLevel(Enum):
    EMERGENCY = "emergency"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Customer:
    name: str
    phone: str
    address: str
    email: Optional[str] = None

@dataclass
class Job:
    id: str
    customer: Customer
    description: str
    classification: Dict
    status: JobStatus
    priority: PriorityLevel
    estimated_duration: str
    required_tools: List[str]
    recommended_parts: List[str]
    safety_notes: List[str]
    created_at: datetime
    assigned_technician: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    notes: str = ""

class PlumberWorkflow:
    def __init__(self):
        self.jobs: List[Job] = []
        self.technicians = [
            "Mike Johnson",
            "Sarah Williams", 
            "David Chen",
            "Lisa Rodriguez"
        ]
        self.api_available = self._check_api_health()
    
    def _check_api_health(self) -> bool:
        """Check if the API is available"""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def classify_issue(self, description: str, customer_info: Dict) -> Dict:
        """Classify a plumbing issue using the API"""
        if not self.api_available:
            return self._fallback_classification(description)
        
        try:
            payload = {
                "description": description,
                **customer_info
            }
            
            response = requests.post(
                f"{API_BASE_URL}/classify",
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
        """Fallback classification when API is unavailable"""
        description_lower = description.lower()
        
        # Simple keyword-based classification
        if any(word in description_lower for word in ['leak', 'drip', 'water']):
            category = "leak"
            severity = "medium"
            urgency = "medium"
        elif any(word in description_lower for word in ['clog', 'blocked', 'slow drain']):
            category = "clog"
            severity = "medium"
            urgency = "medium"
        elif any(word in description_lower for word in ['hot water', 'heater']):
            category = "water_heater"
            severity = "medium"
            urgency = "medium"
        elif any(word in description_lower for word in ['faucet', 'tap']):
            category = "faucet"
            severity = "low"
            urgency = "medium"
        elif any(word in description_lower for word in ['toilet', 'flush']):
            category = "toilet"
            severity = "medium"
            urgency = "medium"
        elif any(word in description_lower for word in ['emergency', 'burst', 'flooding']):
            category = "pipe"
            severity = "critical"
            urgency = "emergency"
        else:
            category = "other"
            severity = "medium"
            urgency = "medium"
        
        return {
            "classification": {
                "category": category,
                "confidence": 0.5,
                "severity": severity,
                "urgency": urgency,
                "estimated_duration": "1-2 hours",
                "required_tools": ["Basic plumbing tools"],
                "recommended_parts": ["Standard parts"],
                "safety_notes": ["Follow standard safety procedures"],
                "next_steps": ["Schedule technician"]
            },
            "processing_time_ms": 0,
            "model_version": "fallback"
        }
    
    def create_job(self, customer: Customer, description: str) -> Job:
        """Create a new job with AI classification"""
        print(f"\n🔍 Analyzing issue: '{description}'")
        
        # Classify the issue
        customer_info = {
            "customer_name": customer.name,
            "phone_number": customer.phone,
            "address": customer.address
        }
        
        result = self.classify_issue(description, customer_info)
        classification = result["classification"]
        
        # Determine priority based on urgency
        urgency = classification["urgency"]
        if urgency == "emergency":
            priority = PriorityLevel.EMERGENCY
        elif urgency == "high":
            priority = PriorityLevel.HIGH
        elif urgency == "low":
            priority = PriorityLevel.LOW
        else:
            priority = PriorityLevel.MEDIUM
        
        # Create job
        job = Job(
            id=f"JOB-{len(self.jobs) + 1:04d}",
            customer=customer,
            description=description,
            classification=classification,
            status=JobStatus.PENDING,
            priority=priority,
            estimated_duration=classification["estimated_duration"],
            required_tools=classification["required_tools"],
            recommended_parts=classification["recommended_parts"],
            safety_notes=classification["safety_notes"],
            created_at=datetime.now()
        )
        
        self.jobs.append(job)
        
        print(f"✅ Job created: {job.id}")
        print(f"   Category: {classification['category']}")
        print(f"   Priority: {priority.name}")
        print(f"   Estimated Duration: {classification['estimated_duration']}")
        
        return job
    
    def assign_job(self, job_id: str, technician: str) -> bool:
        """Assign a job to a technician"""
        job = self._find_job(job_id)
        if not job:
            print(f"❌ Job {job_id} not found")
            return False
        
        if technician not in self.technicians:
            print(f"❌ Technician {technician} not found")
            return False
        
        job.assigned_technician = technician
        job.status = JobStatus.ASSIGNED
        
        print(f"✅ Job {job_id} assigned to {technician}")
        return True
    
    def start_job(self, job_id: str) -> bool:
        """Start work on a job"""
        job = self._find_job(job_id)
        if not job:
            return False
        
        job.status = JobStatus.IN_PROGRESS
        print(f"🔧 Started work on job {job_id}")
        return True
    
    def complete_job(self, job_id: str, notes: str = "") -> bool:
        """Complete a job"""
        job = self._find_job(job_id)
        if not job:
            return False
        
        job.status = JobStatus.COMPLETED
        job.notes = notes
        print(f"✅ Completed job {job_id}")
        return True
    
    def _find_job(self, job_id: str) -> Optional[Job]:
        """Find a job by ID"""
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None
    
    def get_jobs_by_status(self, status: JobStatus) -> List[Job]:
        """Get jobs filtered by status"""
        return [job for job in self.jobs if job.status == status]
    
    def get_jobs_by_priority(self, priority: PriorityLevel) -> List[Job]:
        """Get jobs filtered by priority"""
        return [job for job in self.jobs if job.priority == priority]
    
    def get_emergency_jobs(self) -> List[Job]:
        """Get all emergency jobs"""
        return [job for job in self.jobs if job.priority == PriorityLevel.EMERGENCY]
    
    def display_job(self, job: Job):
        """Display detailed job information"""
        print(f"\n📋 Job: {job.id}")
        print(f"   Customer: {job.customer.name}")
        print(f"   Phone: {job.customer.phone}")
        print(f"   Address: {job.customer.address}")
        print(f"   Description: {job.description}")
        print(f"   Status: {job.status.value}")
        print(f"   Priority: {job.priority.name}")
        print(f"   Category: {job.classification['category']}")
        print(f"   Estimated Duration: {job.estimated_duration}")
        
        if job.assigned_technician:
            print(f"   Assigned To: {job.assigned_technician}")
        
        print(f"   Required Tools: {', '.join(job.required_tools)}")
        print(f"   Recommended Parts: {', '.join(job.recommended_parts)}")
        print(f"   Safety Notes: {', '.join(job.safety_notes)}")
        
        if job.notes:
            print(f"   Notes: {job.notes}")
    
    def display_dashboard(self):
        """Display the main dashboard"""
        print("\n" + "="*60)
        print("🚰 PLUMBER WORKFLOW DASHBOARD")
        print("="*60)
        
        # API Status
        status = "✅ Online" if self.api_available else "❌ Offline"
        print(f"API Status: {status}")
        
        # Job Statistics
        total_jobs = len(self.jobs)
        pending_jobs = len(self.get_jobs_by_status(JobStatus.PENDING))
        in_progress = len(self.get_jobs_by_status(JobStatus.IN_PROGRESS))
        completed = len(self.get_jobs_by_status(JobStatus.COMPLETED))
        emergency_jobs = len(self.get_emergency_jobs())
        
        print(f"\n📊 Job Statistics:")
        print(f"   Total Jobs: {total_jobs}")
        print(f"   Pending: {pending_jobs}")
        print(f"   In Progress: {in_progress}")
        print(f"   Completed: {completed}")
        print(f"   Emergency: {emergency_jobs}")
        
        # Show emergency jobs first
        if emergency_jobs > 0:
            print(f"\n🚨 EMERGENCY JOBS:")
            for job in self.get_emergency_jobs():
                print(f"   {job.id}: {job.customer.name} - {job.description[:50]}...")
        
        # Show pending jobs
        pending = self.get_jobs_by_status(JobStatus.PENDING)
        if pending:
            print(f"\n⏳ PENDING JOBS:")
            for job in pending[:5]:  # Show first 5
                print(f"   {job.id}: {job.customer.name} - {job.description[:50]}...")
        
        # Show in-progress jobs
        in_progress_jobs = self.get_jobs_by_status(JobStatus.IN_PROGRESS)
        if in_progress_jobs:
            print(f"\n🔧 IN PROGRESS:")
            for job in in_progress_jobs:
                print(f"   {job.id}: {job.assigned_technician} - {job.description[:50]}...")
    
    def export_job_report(self, filename: str = "job_report.json"):
        """Export jobs to JSON file"""
        report = {
            "export_date": datetime.now().isoformat(),
            "total_jobs": len(self.jobs),
            "jobs": []
        }
        
        for job in self.jobs:
            job_data = {
                "id": job.id,
                "customer": {
                    "name": job.customer.name,
                    "phone": job.customer.phone,
                    "address": job.customer.address
                },
                "description": job.description,
                "classification": job.classification,
                "status": job.status.value,
                "priority": job.priority.name,
                "assigned_technician": job.assigned_technician,
                "estimated_duration": job.estimated_duration,
                "required_tools": job.required_tools,
                "recommended_parts": job.recommended_parts,
                "safety_notes": job.safety_notes,
                "created_at": job.created_at.isoformat(),
                "notes": job.notes
            }
            report["jobs"].append(job_data)
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Job report exported to {filename}")

def main():
    """Main workflow demonstration"""
    workflow = PlumberWorkflow()
    
    print("🚰 Welcome to the Plumber Workflow System!")
    print("This system integrates with the Smart Plumbing Issue Classifier API")
    
    # Simulate incoming calls
    print("\n📞 Simulating incoming customer calls...")
    
    # Emergency call
    customer1 = Customer("Mary Smith", "555-0101", "123 Oak St, Anytown")
    job1 = workflow.create_job(customer1, "EMERGENCY! Pipe burst in basement, water everywhere!")
    
    # Regular call
    customer2 = Customer("John Davis", "555-0202", "456 Pine Ave, Somewhere")
    job2 = workflow.create_job(customer2, "Kitchen sink is clogged and water won't drain")
    
    # Another call
    customer3 = Customer("Lisa Brown", "555-0303", "789 Elm Rd, Elsewhere")
    job3 = workflow.create_job(customer3, "No hot water coming from any faucet")
    
    # Assign jobs
    workflow.assign_job(job1.id, "Mike Johnson")
    workflow.assign_job(job2.id, "Sarah Williams")
    
    # Start emergency job
    workflow.start_job(job1.id)
    
    # Display dashboard
    workflow.display_dashboard()
    
    # Show detailed job info
    print("\n📋 Detailed Job Information:")
    workflow.display_job(job1)
    
    # Export report
    workflow.export_job_report()
    
    print("\n✅ Workflow demonstration completed!")

if __name__ == "__main__":
    main() 