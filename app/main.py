import time
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .models import (
    IssueRequest, IssueResponse, IssueClassification, 
    HealthResponse, ErrorResponse
)
from .classifier import PlumbingIssueClassifier

# Global classifier instance
classifier = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global classifier
    classifier = PlumbingIssueClassifier()
    print("🚰 Plumbing Issue Classifier initialized!")
    yield
    # Shutdown
    print("🔧 Shutting down Plumbing Issue Classifier...")

app = FastAPI(
    title="Smart Plumbing Issue Classifier API",
    description="AI-powered API for classifying plumbing issues and providing recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Smart Plumbing Issue Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0
    
    return HealthResponse(
        status="healthy",
        model_loaded=classifier is not None,
        version="1.0.0",
        uptime_seconds=uptime
    )

@app.post("/classify", response_model=IssueResponse)
async def classify_issue(request: IssueRequest):
    """
    Classify a plumbing issue based on customer description.
    
    This endpoint analyzes the customer's description and provides:
    - Issue category classification
    - Severity and urgency assessment
    - Required tools and parts
    - Safety considerations
    - Recommended next steps
    """
    try:
        if classifier is None:
            raise HTTPException(status_code=503, detail="Classifier not initialized")
        
        # Classify the issue
        result = classifier.classify_issue(request.description)
        
        # Create classification object
        classification = IssueClassification(
            category=result['category'],
            confidence=result['confidence'],
            severity=result['severity'],
            urgency=result['urgency'],
            estimated_duration=result['estimated_duration'],
            required_tools=result['required_tools'],
            recommended_parts=result['recommended_parts'],
            safety_notes=result['safety_notes'],
            next_steps=result['next_steps']
        )
        
        # Generate response
        response = IssueResponse(
            request_id=str(uuid.uuid4()),
            classification=classification,
            processing_time_ms=result['processing_time_ms'],
            model_version="1.0.0"
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get all available issue categories"""
    from .models import IssueCategory
    return {
        "categories": [category.value for category in IssueCategory],
        "descriptions": {
            "leak": "Water leaks from pipes, fixtures, or appliances",
            "clog": "Blocked drains, toilets, or pipes",
            "water_heater": "Issues with hot water supply or heater",
            "faucet": "Problems with faucets, taps, or handles",
            "toilet": "Toilet flushing, running, or clogging issues",
            "drain": "Slow or blocked drains",
            "pipe": "Pipe damage, corrosion, or fitting issues",
            "sewer": "Sewer line backups or main line issues",
            "garbage_disposal": "Garbage disposal problems",
            "water_pressure": "Low or high water pressure issues",
            "other": "Other plumbing-related issues"
        }
    }

@app.get("/severity-levels")
async def get_severity_levels():
    """Get all available severity levels"""
    from .models import IssueSeverity
    return {
        "severity_levels": [severity.value for severity in IssueSeverity],
        "descriptions": {
            "low": "Minor issues that don't require immediate attention",
            "medium": "Moderate issues that should be addressed soon",
            "high": "Serious issues requiring prompt attention",
            "critical": "Emergency situations requiring immediate response"
        }
    }

@app.get("/urgency-levels")
async def get_urgency_levels():
    """Get all available urgency levels"""
    from .models import IssueUrgency
    return {
        "urgency_levels": [urgency.value for urgency in IssueUrgency],
        "descriptions": {
            "low": "Can be scheduled at customer's convenience",
            "medium": "Should be addressed within 24-48 hours",
            "high": "Requires attention within 2-4 hours",
            "emergency": "Requires immediate emergency response"
        }
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler for HTTP errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail="Please check the request and try again"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred"
        ).dict()
    )

# Store startup time for health check
@app.on_event("startup")
async def startup_event():
    app.state.start_time = time.time() 