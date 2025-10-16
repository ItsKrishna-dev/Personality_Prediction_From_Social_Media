# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

from model_loader import Big5ModelLoader
from gemini_summarizer import GeminiPersonalitySummarizer

app = FastAPI(title="Big Five Personality Prediction API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model and summarizer
model_loader = Big5ModelLoader('C:/Users/KRISHNA CHAURASIA/Downloads/Personality_ui/model/Big_5_final.json','C:/Users/KRISHNA CHAURASIA/Downloads/Personality_ui/model/lda_model.joblib','C:/Users/KRISHNA CHAURASIA/Downloads/Personality_ui/model/lda_vec.joblib')
summarizer = GeminiPersonalitySummarizer()

# Request/Response models
class PredictionRequest(BaseModel):
    comments: List[str]
    include_summary: bool = True

class TraitScore(BaseModel):
    score: float
    percentage: float

class PredictionResponse(BaseModel):
    scores: Dict[str, TraitScore]
    interpretations: Dict[str, str]
    summary: Dict[str, str] = None
    success: bool = True

@app.get("/")
async def root():
    return {"message": "Big Five Personality Prediction API", "status": "running"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_personality(request: PredictionRequest):
    """Predict Big Five personality traits from user comments"""
    try:
        # Validate input
        if not request.comments or len(request.comments) == 0:
            raise HTTPException(status_code=400, detail="No comments provided")
        
        # Get predictions
        scores = model_loader.predict(request.comments)
        
        # Get basic interpretations
        interpretations = {}
        for trait, data in scores.items():
            interpretations[trait] = model_loader.get_trait_interpretation(
                trait, data['score']
            )
        
        # Generate AI summary if requested
        summary = None
        if request.include_summary:
            try:
                summary = summarizer.create_personality_summary(scores)
            except Exception as e:
                print(f"Error generating summary: {e}")
                summary = {
                    'full_summary': 'AI summary temporarily unavailable',
                    'short_summary': 'Unable to generate summary at this time'
                }
        
        return PredictionResponse(
            scores=scores,
            interpretations=interpretations,
            summary=summary,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/trait-insight")
async def get_trait_insight(trait: str, score: float):
    """Get detailed insights for a specific trait"""
    try:
        insight = summarizer.get_trait_specific_insights(trait, score)
        return {"trait": trait, "score": score, "insight": insight}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)