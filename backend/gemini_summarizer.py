# backend/gemini_summarizer.py - WORKING VERSION
import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiPersonalitySummarizer:
    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        
        # List of models to try in order (October 2025 working models)
        models_to_try = [
            'gemini-1.5-flash',      # Current free tier model
            'gemini-1.5-flash-latest',
            'gemini-2.5-flash-preview-09-2025',
            'models/gemini-1.5-flash',
            'models/gemini-pro',
            'gemini-1.0-pro-latest',
            'gemini-1.0-pro'
        ]
        
        model_loaded = False
        last_error = None
        
        for model_name in models_to_try:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test the model works
                test_response = self.model.generate_content("Test")
                print(f"✓ Successfully loaded Gemini model: {model_name}")
                model_loaded = True
                break
            except Exception as e:
                last_error = e
                print(f"⚠ Model {model_name} not available: {str(e)[:100]}")
                continue
        
        if not model_loaded:
            print(f"❌ No Gemini models available. Last error: {last_error}")
            print("⚠ Running in fallback mode (basic summaries without AI)")
            self.model = None
        
    def create_personality_summary(self, scores: Dict[str, Dict]) -> Dict[str, str]:
        """Generate comprehensive personality summary using Gemini"""
        
        # Prepare scores for prompt
        scores_text = "\n".join([
            f"- {trait}: {data['score']}/10 ({data['percentage']}%)"
            for trait, data in scores.items()
        ])
        
        # If model not available, use fallback
        if self.model is None:
            return self._generate_fallback_summary(scores, scores_text)
        
        try:
            # Create detailed prompt
            prompt = f"""
Based on the following Big Five personality trait scores, provide a comprehensive personality analysis:

{scores_text}

Please provide:

1. **Overall Personality Summary** (2-3 sentences): A concise overview of the person's personality based on all five traits.

2. **Trait-by-Trait Analysis**: For each trait, explain what their score means:
   - Openness to Experience
   - Conscientiousness
   - Extraversion
   - Agreeableness
   - Neuroticism (Emotional Stability)

3. **Strengths**: List 3-4 key personality strengths based on these scores.

4. **Growth Areas**: Suggest 2-3 areas where they might consider personal development.

5. **Career Suggestions**: Recommend 3-4 career paths or work environments that would suit this personality profile.

6. **Relationship Style**: Describe how they likely approach personal and professional relationships.

Format the response in clear sections with bullet points where appropriate. Be encouraging and constructive.
"""
            
            # Generate summary
            response = self.model.generate_content(prompt)
            full_summary = response.text
            
            # Create short summary for quick view
            short_prompt = f"""
Based on these Big Five scores: {scores_text}

Provide a 2-sentence personality snapshot that captures the essence of this personality profile.
"""
            
            short_response = self.model.generate_content(short_prompt)
            short_summary = short_response.text
            
            return {
                'full_summary': full_summary,
                'short_summary': short_summary,
                'generated_at': 'AI-generated'
            }
            
        except Exception as e:
            print(f"❌ Error generating AI summary: {e}")
            return self._generate_fallback_summary(scores, scores_text)
    
    def _generate_fallback_summary(self, scores: Dict[str, Dict], scores_text: str) -> Dict[str, str]:
        """Generate a rule-based summary when AI is unavailable"""
        
        # Calculate statistics
        trait_scores = {trait: data['score'] for trait, data in scores.items()}
        avg_score = sum(trait_scores.values()) / len(trait_scores)
        highest_trait = max(trait_scores.items(), key=lambda x: x[1])
        lowest_trait = min(trait_scores.items(), key=lambda x: x[1])
        
        # Trait descriptions
        trait_descriptions = {
            'Openness': {
                'high': 'creative, curious, and open to new experiences',
                'medium': 'moderately open to new ideas with practical considerations',
                'low': 'practical, conventional, and prefers familiar routines'
            },
            'Conscientiousness': {
                'high': 'organized, disciplined, and goal-oriented',
                'medium': 'reasonably organized with balanced spontaneity',
                'low': 'spontaneous, flexible, and adaptable'
            },
            'Extraversion': {
                'high': 'outgoing, energetic, and socially engaged',
                'medium': 'balanced social engagement with alone time',
                'low': 'reserved, introspective, and values solitude'
            },
            'Agreeableness': {
                'high': 'compassionate, cooperative, and empathetic',
                'medium': 'cooperative with assertiveness when needed',
                'low': 'direct, competitive, and values honesty'
            },
            'Neuroticism': {
                'high': 'emotionally sensitive and aware of feelings',
                'medium': 'emotionally balanced with normal stress responses',
                'low': 'emotionally stable and resilient'
            }
        }
        
        def get_level(score):
            return 'high' if score > 6.5 else 'medium' if score > 3.5 else 'low'
        
        # Build comprehensive summary
        full_summary = f"""## Overall Personality Summary

Your personality profile shows an average score of {avg_score:.1f}/10 across all traits. You are particularly strong in {highest_trait[0]} ({highest_trait[1]}/10), which suggests you are {trait_descriptions[highest_trait[0]][get_level(highest_trait[1])]}. Your profile indicates a {'well-balanced' if 3 < avg_score < 7 else 'distinctive'} personality with unique strengths.

## Trait-by-Trait Analysis

### Openness to Experience: {trait_scores['Openness']}/10
You show {get_level(trait_scores['Openness'])} openness, meaning you are {trait_descriptions['Openness'][get_level(trait_scores['Openness'])]}.

### Conscientiousness: {trait_scores['Conscientiousness']}/10
Your conscientiousness is {get_level(trait_scores['Conscientiousness'])}, indicating you are {trait_descriptions['Conscientiousness'][get_level(trait_scores['Conscientiousness'])]}.

### Extraversion: {trait_scores['Extraversion']}/10
With {get_level(trait_scores['Extraversion'])} extraversion, you are {trait_descriptions['Extraversion'][get_level(trait_scores['Extraversion'])]}.

### Agreeableness: {trait_scores['Agreeableness']}/10
Your agreeableness is {get_level(trait_scores['Agreeableness'])}, showing you are {trait_descriptions['Agreeableness'][get_level(trait_scores['Agreeableness'])]}.

### Neuroticism: {trait_scores['Neuroticism']}/10
Your neuroticism score indicates you are {trait_descriptions['Neuroticism'][get_level(trait_scores['Neuroticism'])]}.

## Key Strengths

Based on your scores, your main strengths include:
- **{highest_trait[0]}** ({highest_trait[1]}/10): This is your strongest trait
- Balanced approach across multiple personality dimensions
- Unique combination of traits that defines your individuality

## Growth Areas

Areas for potential development:
- **{lowest_trait[0]}** ({lowest_trait[1]}/10): Consider exploring activities that build this trait
- Balance between different aspects of your personality
- Self-awareness through continuous reflection

## Career Suggestions

Based on your profile, suitable career paths might include:
- Roles that leverage your high {highest_trait[0].lower()}
- Environments that match your {get_level(trait_scores['Extraversion'])} social engagement preference
- Positions requiring {get_level(trait_scores['Conscientiousness'])} levels of structure

## Relationship Style

Your personality suggests you approach relationships with:
- {"High empathy and cooperation" if trait_scores['Agreeableness'] > 6 else "Balanced cooperation and assertiveness" if trait_scores['Agreeableness'] > 4 else "Direct communication and honesty"}
- {"Social engagement and energy sharing" if trait_scores['Extraversion'] > 6 else "Balanced social interaction" if trait_scores['Extraversion'] > 4 else "Meaningful one-on-one connections"}
- {"Emotional awareness and sensitivity" if trait_scores['Neuroticism'] > 6 else "Emotional stability with normal responses" if trait_scores['Neuroticism'] > 4 else "Calm and resilient demeanor"}
"""
        
        short_summary = f"Your personality profile (average {avg_score:.1f}/10) shows particularly strong {highest_trait[0]} ({highest_trait[1]}/10), indicating you are {trait_descriptions[highest_trait[0]][get_level(highest_trait[1])]}. This unique combination of traits shapes how you interact with the world and approach challenges."
        
        return {
            'full_summary': full_summary,
            'short_summary': short_summary,
            'generated_at': 'Rule-based (AI unavailable)'
        }
    
    def get_trait_specific_insights(self, trait: str, score: float) -> str:
        """Get specific insights for a single trait"""
        
        if self.model is None:
            return self._get_fallback_trait_insight(trait, score)
        
        try:
            prompt = f"""
For the personality trait {trait} with a score of {score}/10 ({score*10}%):

Provide:
1. What this score means in everyday behavior
2. How this manifests in work settings
3. Tips for leveraging this trait effectively

Keep it concise (3-4 sentences total).
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ Error generating trait insight: {e}")
            return self._get_fallback_trait_insight(trait, score)
    
    def _get_fallback_trait_insight(self, trait: str, score: float) -> str:
        """Generate trait insight without AI"""
        level = "high" if score > 6.5 else "moderate" if score > 3.5 else "low"
        
        insights = {
            'Openness': f"Your {level} openness ({score}/10) influences your curiosity and creativity. This affects how you approach new experiences and problem-solving in daily life.",
            'Conscientiousness': f"With {level} conscientiousness ({score}/10), you show {'strong organizational skills' if level == 'high' else 'balanced flexibility' if level == 'moderate' else 'spontaneous adaptability'}. This impacts your work ethic and goal achievement.",
            'Extraversion': f"Your {level} extraversion ({score}/10) shapes your social energy. You {'thrive in social settings' if level == 'high' else 'balance social interaction with alone time' if level == 'moderate' else 'prefer deep one-on-one connections'}.",
            'Agreeableness': f"Your {level} agreeableness ({score}/10) influences how you collaborate. You tend to be {'highly cooperative and empathetic' if level == 'high' else 'balanced in cooperation and assertiveness' if level == 'moderate' else 'direct and honest in communication'}.",
            'Neuroticism': f"With {level} emotional sensitivity ({score}/10), you {'are highly aware of emotions' if level == 'high' else 'experience normal emotional responses' if level == 'moderate' else 'maintain emotional stability'}. This affects stress management and resilience."
        }
        
        return insights.get(trait, f"Your {trait} score of {score}/10 indicates a {level} level in this trait.")
