# Smart Plumbing Issue Classifier API

🚰 **AI-powered API for classifying plumbing issues and providing intelligent recommendations**

Help plumbing businesses quickly triage customer service requests using NLP. This tool uses machine learning to classify customer-reported issues into predefined categories and suggests appropriate tools, parts, safety considerations, and next steps.

## 🎯 Use Case

Customers often describe issues vaguely ("my sink is making noise", "no hot water"), and dispatchers have to guess severity, urgency, or required tools. This API uses NLP to classify customer-reported issues into predefined categories and provides comprehensive recommendations.

## ✨ Features

- **Smart Issue Classification**: Automatically categorizes plumbing issues (leak, clog, water heater, etc.)
- **Severity & Urgency Assessment**: Determines issue severity (low, medium, high, critical) and urgency (low, medium, high, emergency)
- **Tool & Parts Recommendations**: Suggests required tools and parts for each issue type
- **Safety Guidelines**: Provides safety considerations for technicians
- **Next Steps**: Generates appropriate next steps based on classification
- **Duration Estimates**: Provides time estimates for issue resolution
- **RESTful API**: Clean, documented API with automatic OpenAPI documentation

## 🏗️ Architecture

```
app/
├── __init__.py          # Package initialization
├── models.py            # Pydantic models for request/response schemas
├── classifier.py        # Core NLP classifier with ML pipeline
└── main.py             # FastAPI application with endpoints

tests/
├── __init__.py         # Test package
├── test_classifier.py  # Unit tests for classifier
└── test_api.py        # Integration tests for API endpoints

run.py                  # Application entry point
requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

```bash
python run.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Test the API

```bash
# Run tests
pytest tests/

# Test with curl
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Water is leaking from under the kitchen sink",
    "customer_name": "John Doe",
    "phone_number": "555-1234"
  }'
```

## 📋 API Endpoints

### POST `/classify`
Classify a plumbing issue based on customer description.

**Request:**
```json
{
  "description": "Water is leaking from under the kitchen sink",
  "customer_name": "John Doe",
  "phone_number": "555-1234",
  "address": "123 Main St"
}
```

**Response:**
```json
{
  "request_id": "uuid-string",
  "classification": {
    "category": "leak",
    "confidence": 0.85,
    "severity": "medium",
    "urgency": "medium",
    "estimated_duration": "1-3 hours",
    "required_tools": ["pipe wrench", "plumber's tape", "soldering torch"],
    "recommended_parts": ["pipe fittings", "soldering materials"],
    "safety_notes": ["Turn off water supply before repairs"],
    "next_steps": ["Schedule technician within 24-48 hours"]
  },
  "processing_time_ms": 45.2,
  "model_version": "1.0.0"
}
```

### GET `/health`
Health check endpoint.

### GET `/categories`
Get all available issue categories.

### GET `/severity-levels`
Get all available severity levels.

### GET `/urgency-levels`
Get all available urgency levels.

## 🔧 Issue Categories

- **leak**: Water leaks from pipes, fixtures, or appliances
- **clog**: Blocked drains, toilets, or pipes
- **water_heater**: Issues with hot water supply or heater
- **faucet**: Problems with faucets, taps, or handles
- **toilet**: Toilet flushing, running, or clogging issues
- **drain**: Slow or blocked drains
- **pipe**: Pipe damage, corrosion, or fitting issues
- **sewer**: Sewer line backups or main line issues
- **garbage_disposal**: Garbage disposal problems
- **water_pressure**: Low or high water pressure issues
- **other**: Other plumbing-related issues

## 🎯 Severity Levels

- **low**: Minor issues that don't require immediate attention
- **medium**: Moderate issues that should be addressed soon
- **high**: Serious issues requiring prompt attention
- **critical**: Emergency situations requiring immediate response

## ⚡ Urgency Levels

- **low**: Can be scheduled at customer's convenience
- **medium**: Should be addressed within 24-48 hours
- **high**: Requires attention within 2-4 hours
- **emergency**: Requires immediate emergency response

## 🤖 Machine Learning Model

The classifier uses:
- **TF-IDF Vectorization**: Converts text descriptions to numerical features
- **Naive Bayes Classification**: Fast and effective for text classification
- **Keyword-based Analysis**: Additional logic for severity and urgency detection
- **Rule-based Recommendations**: Domain-specific knowledge for tools, parts, and safety

The model is trained on sample plumbing issue data and can be easily retrained with real customer data.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_classifier.py

# Run with coverage
pytest --cov=app tests/
```

## 🔧 Configuration

Environment variables (optional):
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (default: False)

## 📦 Dependencies

- **FastAPI**: Modern web framework for APIs
- **scikit-learn**: Machine learning library
- **pydantic**: Data validation
- **uvicorn**: ASGI server
- **pytest**: Testing framework

## 🚀 Production Deployment

1. **Docker** (recommended):
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "run.py"]
   ```

2. **Environment Variables**:
   ```bash
   export HOST=0.0.0.0
   export PORT=8000
   export DEBUG=False
   ```

3. **Process Manager** (e.g., systemd, supervisor)

## 🔮 Future Enhancements

- [ ] Integration with real customer data for model training
- [ ] Advanced NLP models (BERT, transformers)
- [ ] Image classification for visual issue detection
- [ ] Integration with scheduling systems
- [ ] Customer notification system
- [ ] Analytics dashboard
- [ ] Multi-language support

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Built with ❤️ for plumbing professionals**
