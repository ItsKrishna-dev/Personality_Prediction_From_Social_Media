# Big Five Personality Prediction Backend

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install fastapi uvicorn python-dotenv google-generativeai sentence-transformers vaderSentiment scikit-learn xgboost nltk joblib pandas numpy
```

### 2. Download NLTK Data
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords')"
```

### 3. Setup Environment Variables
Create a `.env` file in the backend directory:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key
```

Get a free API key from: https://makersuite.google.com/app/apikey

### 4. Prepare Model Files
Create a `model` directory and place your trained models:
```
backend/
├── model/
│   ├── Big_5_final.json
│   ├── lda_model.joblib
│   └── lda_vec.joblib
```

If you need to recreate the LDA models, run:
```bash
python fix_lda_vectorizer_final.py
```

### 5. Run the Backend
```bash
cd backend
python app.py
```

Or using uvicorn:
```bash
uvicorn app:app --reload --port 8000
```

The API will be available at: http://localhost:8000

### API Endpoints

**POST /predict**
- Request: `{"comments": ["text1", "text2", ...], "include_summary": true}`
- Response: `{"scores": {...}, "interpretations": {...}, "summary": {...}, "success": true}`

**GET /**
- Health check endpoint

## Frontend Integration

The frontend expects the backend to run on `http://localhost:8000`

Make sure to start the backend before using the frontend!
