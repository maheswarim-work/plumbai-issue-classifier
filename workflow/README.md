# 🚰 Plumber Workflow System

A complete workflow management system that integrates with the Smart Plumbing Issue Classifier API to streamline plumbing business operations.

## 🎯 Overview

This workflow system provides plumbers with:
- **AI-powered issue classification** for faster triage
- **Automated job prioritization** based on urgency and severity
- **Smart technician assignment** based on skills and location
- **Mobile app interface** for technicians in the field
- **Real-time dispatch management** with priority queuing
- **Comprehensive reporting** and analytics

## 🏗️ System Components

### 1. **Plumber Dashboard** (`plumber_dashboard.py`)
- **Purpose**: Main office interface for dispatchers and managers
- **Features**:
  - Job creation and management
  - Technician assignment
  - Real-time status tracking
  - Job reporting and analytics
  - API integration for classification

### 2. **Mobile App** (`mobile_app.py`)
- **Purpose**: Field interface for technicians
- **Features**:
  - Job details and instructions
  - On-site issue classification
  - Tools and safety checklists
  - Job status updates
  - Parts tracking

### 3. **Dispatch System** (`dispatch_system.py`)
- **Purpose**: Automated job assignment and prioritization
- **Features**:
  - Priority queue management
  - Smart technician matching
  - Emergency response handling
  - Real-time status updates
  - Location-based assignment

### 4. **Complete Workflow Demo** (`run_workflow_demo.py`)
- **Purpose**: End-to-end workflow demonstration
- **Features**:
  - Simulates complete business process
  - Shows all systems working together
  - Demonstrates real-world scenarios

## 🚀 Quick Start

### Prerequisites
1. **API Running**: Make sure the Smart Plumbing Issue Classifier API is running
   ```bash
   python run.py
   ```

2. **Dependencies**: Install required packages
   ```bash
   pip install requests
   ```

### Running the Workflow

#### 1. **Complete Workflow Demo**
```bash
cd workflow
python run_workflow_demo.py
```

#### 2. **Individual System Demos**

**Dashboard Demo:**
```bash
python plumber_dashboard.py
```

**Mobile App Demo:**
```bash
python mobile_app.py
```

**Dispatch System Demo:**
```bash
python dispatch_system.py
```

## 📋 Workflow Process

### Phase 1: Customer Call
1. **Customer calls** with plumbing issue
2. **AI classification** determines:
   - Issue category (leak, clog, etc.)
   - Severity level (low, medium, high, critical)
   - Urgency level (low, medium, high, emergency)
   - Required tools and parts
   - Safety considerations
   - Estimated duration

### Phase 2: Job Assignment
1. **Priority queuing** based on urgency
2. **Technician matching** based on:
   - Skills match
   - Location proximity
   - Current availability
3. **Automatic assignment** to best technician

### Phase 3: Field Work
1. **Technician receives** job details on mobile app
2. **On-site classification** for additional details
3. **Tools and safety** checklists provided
4. **Real-time updates** to office systems

### Phase 4: Completion
1. **Job completion** with notes and parts used
2. **System updates** across all components
3. **Reporting** and analytics generation

## 🎯 Business Benefits

### For Dispatchers
- ✅ **Faster triage** with AI classification
- ✅ **Better prioritization** of emergency calls
- ✅ **Reduced errors** in job assignment
- ✅ **Real-time visibility** of all jobs

### For Technicians
- ✅ **Clear job instructions** with tools and parts lists
- ✅ **Safety guidelines** for each job type
- ✅ **On-site classification** for complex issues
- ✅ **Easy status updates** from mobile app

### For Business Owners
- ✅ **Improved response times** for emergencies
- ✅ **Better resource utilization**
- ✅ **Enhanced customer satisfaction**
- ✅ **Comprehensive reporting** and analytics

## 🔧 Configuration

### API Configuration
Edit the API URL in each system:
```python
API_BASE_URL = "http://localhost:8000"  # Change as needed
```

### Technician Management
Add/remove technicians in `dispatch_system.py`:
```python
self.technicians = [
    Technician("T001", "Mike Johnson", ["leak", "clog", "faucet"], "Downtown"),
    # Add more technicians...
]
```

### Priority Settings
Adjust priority levels in `dispatch_system.py`:
```python
class JobPriority(Enum):
    EMERGENCY = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
```

## 📊 Analytics & Reporting

### Job Reports
- **JSON export** of all job data
- **Performance metrics** tracking
- **Response time** analysis
- **Technician efficiency** reports

### Key Metrics
- Total jobs processed
- Emergency response times
- Technician utilization
- Customer satisfaction scores
- AI classification accuracy

## 🔮 Future Enhancements

### Planned Features
- [ ] **GPS tracking** for technicians
- [ ] **Customer portal** for job status
- [ ] **Inventory integration** for parts tracking
- [ ] **Advanced analytics** dashboard
- [ ] **Multi-location** support
- [ ] **Integration** with accounting systems

### API Enhancements
- [ ] **Image classification** for visual issues
- [ ] **Voice-to-text** for phone calls
- [ ] **Predictive maintenance** suggestions
- [ ] **Cost estimation** based on classification

## 🛠️ Technical Details

### Architecture
- **Modular design** for easy customization
- **API-first approach** for scalability
- **Fallback systems** for offline operation
- **Real-time updates** across all systems

### Data Flow
```
Customer Call → API Classification → Priority Queue → 
Technician Assignment → Mobile App → Field Work → 
Status Updates → Completion → Reporting
```

### Error Handling
- **API fallback** when service is unavailable
- **Graceful degradation** for offline operation
- **Data persistence** for job continuity
- **Error logging** for troubleshooting

## 📞 Support

For questions or issues:
1. Check the API is running: `python run.py`
2. Verify dependencies: `pip install requests`
3. Check network connectivity to API
4. Review error logs for troubleshooting

## 🚀 Production Deployment

### Requirements
- **API Server**: Deploy the classifier API
- **Database**: Add persistent storage for jobs
- **Mobile App**: Develop native mobile apps
- **Web Dashboard**: Create web-based dashboard
- **Security**: Add authentication and authorization

### Scaling Considerations
- **Load balancing** for high-volume operations
- **Database optimization** for large job volumes
- **Mobile app distribution** for technicians
- **API rate limiting** for fair usage
- **Backup systems** for critical operations

---

**Built with ❤️ for plumbing professionals** 