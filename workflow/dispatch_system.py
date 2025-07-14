#!/usr/bin/env python3
"""
Dispatch System for Plumbing Business
Automatically prioritizes and assigns jobs based on AI classification
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import heapq

class JobPriority(Enum):
    EMERGENCY = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Technician:
    id: str
    name: str
    skills: List[str]
    current_location: str
    available: bool = True
    current_job: Optional[str] = None
    estimated_completion: Optional[datetime] = None

@dataclass
class DispatchJob:
    id: str
    customer_name: str
    phone: str
    address: str
    description: str
    classification: Dict
    priority: JobPriority
    created_at: datetime
    estimated_duration: str
    required_tools: List[str]
    safety_notes: List[str]
    assigned_technician: Optional[str] = None

class DispatchSystem:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.jobs: List[DispatchJob] = []
        self.technicians: List[Technician] = []
        self.job_queue = []  # Priority queue
        
        # Initialize technicians
        self._initialize_technicians()
    
    def _initialize_technicians(self):
        """Initialize available technicians"""
        self.technicians = [
            Technician("T001", "Mike Johnson", ["leak", "clog", "faucet"], "Downtown"),
            Technician("T002", "Sarah Williams", ["water_heater", "pipe", "sewer"], "Northside"),
            Technician("T003", "David Chen", ["toilet", "drain", "garbage_disposal"], "Southside"),
            Technician("T004", "Lisa Rodriguez", ["emergency", "leak", "pipe"], "Eastside")
        ]
    
    def classify_and_queue_job(self, customer_name: str, phone: str, address: str, description: str) -> DispatchJob:
        """Classify a new job and add it to the queue"""
        print(f"\n📞 New call from {customer_name}")
        print(f"   Issue: {description}")
        
        # Classify the issue
        result = self._classify_issue(description)
        classification = result["classification"]
        
        # Determine priority
        urgency = classification["urgency"]
        if urgency == "emergency":
            priority = JobPriority.EMERGENCY
        elif urgency == "high":
            priority = JobPriority.HIGH
        elif urgency == "low":
            priority = JobPriority.LOW
        else:
            priority = JobPriority.MEDIUM
        
        # Create dispatch job
        job = DispatchJob(
            id=f"JOB-{len(self.jobs) + 1:04d}",
            customer_name=customer_name,
            phone=phone,
            address=address,
            description=description,
            classification=classification,
            priority=priority,
            created_at=datetime.now(),
            estimated_duration=classification["estimated_duration"],
            required_tools=classification["required_tools"],
            safety_notes=classification["safety_notes"]
        )
        
        self.jobs.append(job)
        
        # Add to priority queue (negative priority for max heap)
        heapq.heappush(self.job_queue, (-priority.value, job.created_at.timestamp(), job))
        
        print(f"✅ Job queued: {job.id}")
        print(f"   Priority: {priority.name}")
        print(f"   Category: {classification['category']}")
        print(f"   Estimated Duration: {classification['estimated_duration']}")
        
        return job
    
    def _classify_issue(self, description: str) -> Dict:
        """Classify an issue using the API"""
        try:
            payload = {"description": description}
            response = requests.post(f"{self.api_url}/classify", json=payload, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_classification(description)
                
        except Exception as e:
            print(f"⚠️  API Error: {e}")
            return self._fallback_classification(description)
    
    def _fallback_classification(self, description: str) -> Dict:
        """Fallback classification"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['emergency', 'burst', 'flooding']):
            category = "pipe"
            urgency = "emergency"
        elif any(word in description_lower for word in ['leak', 'drip']):
            category = "leak"
            urgency = "medium"
        elif any(word in description_lower for word in ['clog', 'blocked']):
            category = "clog"
            urgency = "medium"
        else:
            category = "other"
            urgency = "medium"
        
        return {
            "classification": {
                "category": category,
                "urgency": urgency,
                "severity": "medium",
                "estimated_duration": "1-2 hours",
                "required_tools": ["Basic tools"],
                "safety_notes": ["Follow safety procedures"]
            }
        }
    
    def assign_jobs(self):
        """Assign jobs to available technicians"""
        print("\n🔧 Assigning jobs to technicians...")
        
        while self.job_queue and self._get_available_technicians():
            # Get highest priority job
            _, _, job = heapq.heappop(self.job_queue)
            
            # Find best technician
            technician = self._find_best_technician(job)
            
            if technician:
                self._assign_job_to_technician(job, technician)
            else:
                # Put job back in queue if no technician available
                heapq.heappush(self.job_queue, (-job.priority.value, job.created_at.timestamp(), job))
                break
    
    def _get_available_technicians(self) -> List[Technician]:
        """Get list of available technicians"""
        return [t for t in self.technicians if t.available]
    
    def _find_best_technician(self, job: DispatchJob) -> Optional[Technician]:
        """Find the best technician for a job based on skills and location"""
        available_technicians = self._get_available_technicians()
        
        if not available_technicians:
            return None
        
        # Score technicians based on skills match and location
        technician_scores = []
        
        for tech in available_technicians:
            score = 0
            
            # Skills match
            job_category = job.classification["category"]
            if job_category in tech.skills:
                score += 10
            
            # Emergency jobs get priority
            if job.priority == JobPriority.EMERGENCY:
                if "emergency" in tech.skills:
                    score += 20
                else:
                    score += 5
            
            # Location proximity (simplified)
            if "downtown" in tech.current_location.lower() and "downtown" in job.address.lower():
                score += 5
            
            technician_scores.append((score, tech))
        
        # Return technician with highest score
        technician_scores.sort(key=lambda x: (x[0], x[1].id), reverse=True)
        return technician_scores[0][1]
    
    def _assign_job_to_technician(self, job: DispatchJob, technician: Technician):
        """Assign a job to a technician"""
        job.assigned_technician = technician.id
        technician.current_job = job.id
        technician.available = False
        
        # Estimate completion time
        duration_str = job.estimated_duration
        hours = self._parse_duration(duration_str)
        technician.estimated_completion = datetime.now() + timedelta(hours=hours)
        
        print(f"✅ Job {job.id} assigned to {technician.name}")
        print(f"   Customer: {job.customer_name}")
        print(f"   Address: {job.address}")
        print(f"   Estimated completion: {technician.estimated_completion.strftime('%H:%M')}")
        print(f"   Required tools: {', '.join(job.required_tools)}")
    
    def _parse_duration(self, duration_str: str) -> float:
        """Parse duration string to hours"""
        if "hours" in duration_str:
            # Extract number from "1-3 hours" or "2 hours"
            import re
            numbers = re.findall(r'\d+', duration_str)
            if numbers:
                return float(numbers[0])
        return 2.0  # Default 2 hours
    
    def update_technician_status(self, technician_id: str, available: bool, current_location: str = None):
        """Update technician availability"""
        for tech in self.technicians:
            if tech.id == technician_id:
                tech.available = available
                if current_location:
                    tech.current_location = current_location
                print(f"✅ Technician {tech.name} status updated")
                break
    
    def complete_job(self, technician_id: str):
        """Mark a job as completed"""
        for tech in self.technicians:
            if tech.id == technician_id and tech.current_job:
                job_id = tech.current_job
                tech.current_job = None
                tech.available = True
                tech.estimated_completion = None
                
                print(f"✅ Job {job_id} completed by {tech.name}")
                break
    
    def display_dispatch_status(self):
        """Display current dispatch status"""
        print("\n" + "="*60)
        print("🚰 DISPATCH SYSTEM STATUS")
        print("="*60)
        
        # Job queue status
        pending_jobs = len(self.job_queue)
        total_jobs = len(self.jobs)
        assigned_jobs = len([j for j in self.jobs if j.assigned_technician])
        
        print(f"\n📊 Job Status:")
        print(f"   Total Jobs: {total_jobs}")
        print(f"   Pending: {pending_jobs}")
        print(f"   Assigned: {assigned_jobs}")
        
        # Emergency jobs
        emergency_jobs = [j for j in self.jobs if j.priority == JobPriority.EMERGENCY]
        if emergency_jobs:
            print(f"\n🚨 Emergency Jobs:")
            for job in emergency_jobs:
                status = "Assigned" if job.assigned_technician else "Pending"
                print(f"   {job.id}: {job.customer_name} - {status}")
        
        # Technician status
        print(f"\n👥 Technician Status:")
        for tech in self.technicians:
            status = "Available" if tech.available else "Busy"
            current_job = tech.current_job if tech.current_job else "None"
            print(f"   {tech.name}: {status} - Job: {current_job}")
        
        # Pending jobs
        if self.job_queue:
            print(f"\n⏳ Next Jobs in Queue:")
            # Show next 3 jobs
            temp_queue = self.job_queue.copy()
            for i in range(min(3, len(temp_queue))):
                _, _, job = heapq.heappop(temp_queue)
                print(f"   {job.id}: {job.customer_name} - {job.description[:40]}...")
    
    def run_dispatch_demo(self):
        """Run a dispatch system demonstration"""
        print("🚰 Dispatch System Demo")
        print("Simulating incoming calls and automatic job assignment...")
        
        # Simulate incoming calls
        calls = [
            ("Mary Smith", "555-0101", "123 Oak St, Downtown", "EMERGENCY! Pipe burst in basement, water everywhere!"),
            ("John Davis", "555-0202", "456 Pine Ave, Northside", "Kitchen sink is clogged and water won't drain"),
            ("Lisa Brown", "555-0303", "789 Elm Rd, Southside", "No hot water coming from any faucet"),
            ("Bob Wilson", "555-0404", "321 Maple Dr, Eastside", "Toilet won't flush properly"),
            ("Alice Johnson", "555-0505", "654 Cedar Ln, Downtown", "Water heater making strange noises")
        ]
        
        # Process calls
        for customer_name, phone, address, description in calls:
            self.classify_and_queue_job(customer_name, phone, address, description)
            print("-" * 40)
        
        # Assign jobs
        self.assign_jobs()
        
        # Display status
        self.display_dispatch_status()
        
        # Simulate job completion
        print(f"\n⏰ Simulating job completion...")
        self.complete_job("T001")  # Mike completes his job
        
        # Reassign jobs
        self.assign_jobs()
        
        # Final status
        self.display_dispatch_status()
        
        print("\n✅ Dispatch system demo completed!")

def main():
    """Main dispatch system demonstration"""
    dispatch = DispatchSystem()
    dispatch.run_dispatch_demo()

if __name__ == "__main__":
    main() 