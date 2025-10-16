# backend/model_loader.py - FIXED FOR XGBOOST JSON
import joblib
from nltk import pos_tag
import json
import numpy as np
from typing import List, Dict
import pandas as pd
import re
import string
from sentence_transformers import SentenceTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.multioutput import MultiOutputRegressor
import xgboost as xgb
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

class Big5ModelLoader:
    def __init__(self, model_path: str, lda_path: str = None, vectorizer_path: str = None):
        """Load the trained Big Five personality model"""
        
        # Load XGBoost model from JSON
        if model_path.endswith('.json'):
            print("Loading XGBoost model from JSON...")
            # Load as XGBoost Booster
            booster = xgb.Booster()
            booster.load_model(model_path)
            
            # Wrap in MultiOutputRegressor if needed
            # For now, we'll use the booster directly
            self.model = booster
            self.is_xgboost_json = True
            print("✓ XGBoost JSON model loaded")
        else:
            # Load pickled model
            print("Loading pickled model...")
            self.model = joblib.load(model_path)
            self.is_xgboost_json = False
            print("✓ Pickled model loaded")
        
        self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Load LDA and vectorizer
        if lda_path and os.path.exists(lda_path):
            self.lda = joblib.load(lda_path)
            print("✓ LDA model loaded")
        else:
            print("⚠ LDA model not found, creating default")
            self.lda = LatentDirichletAllocation(n_components=5)
            self.lda_available = False
            
        if vectorizer_path and os.path.exists(vectorizer_path):
            self.vectorizer = joblib.load(vectorizer_path)
            print("✓ Vectorizer loaded")
        else:
            print("⚠ Vectorizer not found, creating default")
            self.vectorizer = CountVectorizer(max_features=1000)
            self.vectorizer_available = False
        
        self.trait_names = [
            'Openness',
            'Conscientiousness',
            'Extraversion',
            'Agreeableness',
            'Neuroticism'
        ]
        
        # POS tags for feature extraction
        self.pos_tags_of_interest = ['JJ', 'RB', 'NN', 'VB']

    def get_sentiment_features(self, text: str) -> np.ndarray:
        """Extract sentiment analysis features using VADER"""
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        sentiment_vector = np.array([
            sentiment_scores['compound'],
            sentiment_scores['pos'],
            sentiment_scores['neg'],
            sentiment_scores['neu']
        ])
        return sentiment_vector

    def get_embedding_features(self, text: str) -> np.ndarray:
        """Extract Sentence-BERT embeddings"""
        embeddings = self.embedding_model.encode([text])
        return embeddings[0]

    def get_lda_features(self, text: str) -> np.ndarray:
        """Extract LDA topic distribution features"""
        try:
            text_counts = self.vectorizer.transform([text])
            lda_vector = self.lda.transform(text_counts)
            return lda_vector.flatten()
        except:
            # Return zero vector if LDA fails
            n_components = getattr(self.lda, 'n_components', 5)
            return np.zeros(n_components)

    def preprocess_input(self, text:str) -> np.ndarray:
        """Preprocess user comments for model input"""
        # Combine all comments
        text=text.lower()
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"@\w+", "", text)
        text = re.sub(r"#\w+", "", text)
        text = re.sub(r"\d+", "", text)
        text = text.encode("ascii", "ignore").decode()
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        embeddings=self.get_embedding_features(text)
        sentiment=self.get_sentiment_features(text)
        lda=self.get_lda_features(text)
        pos=self.extract_pos_features([text])[0]
        features = np.concatenate([embeddings, sentiment, lda,pos])
        return features

    def extract_pos_features(self, texts):
            """
            Extract normalized part-of-speech tag frequencies as features.
            JJ: adjectives, RB: adverbs, NN: nouns, VB: verbs
            """
            pos_features = []
            
            for text in texts:
                # Tokenize
                tokens = word_tokenize(text.lower())
                
                # Get POS tags
                tags = pos_tag(tokens)
                
                # Count tags
                tag_counts = {tag: 0 for tag in self.pos_tags_of_interest}
                for _, tag in tags:
                    if tag in tag_counts:
                        tag_counts[tag] += 1
                
                # Normalize by total words
                total_words = len(tokens) if tokens else 1
                pos_vec = [tag_counts[tag] / total_words for tag in self.pos_tags_of_interest]
                pos_features.append(pos_vec)
            
            return np.array(pos_features)


    def predict(self, comments: List[str]) -> dict:
        """Predict Big Five scores by averaging per-post predictions."""
        try:
            per_post_predictions = []

            for comment in comments:
                features = self.preprocess_input(comment)
                features = features.reshape(1, -1)
                prediction = self.model.predict(features)[0]  # shape (5,)
                per_post_predictions.append(prediction)

            # Convert list to np.ndarray for easy averaging
            per_post_predictions = np.array(per_post_predictions)  # shape (n_posts, 5)
            avg_prediction = np.mean(per_post_predictions, axis=0) 
            
            # Convert to dictionary with trait names
            results = {}
            for i, trait in enumerate(self.trait_names):
                score = float(avg_prediction[i])
                results[trait] = {
                    'score': round(score, 2),
                    'percentage': round(score * 10, 2)
                }
            return results

        except Exception as e:
            print(f"❌ Prediction error: {e}")
            import traceback
            traceback.print_exc()
            
            # Return default values
            return {
                trait: {'score': 5.0, 'percentage': 50.0}
                for trait in self.trait_names
            }

    def get_trait_interpretation(self, trait: str, score: float) -> str:
        """Get basic interpretation for a trait score"""
        interpretations = {
            'Openness': {
                'low': 'Prefers routine and familiar experiences',
                'medium': 'Balanced approach to new experiences',
                'high': 'Very open to new ideas and experiences'
            },
            'Conscientiousness': {
                'low': 'Spontaneous and flexible',
                'medium': 'Moderately organized and reliable',
                'high': 'Highly organized and disciplined'
            },
            'Extraversion': {
                'low': 'Reserved and introspective',
                'medium': 'Balanced social engagement',
                'high': 'Outgoing and energetic'
            },
            'Agreeableness': {
                'low': 'Direct and competitive',
                'medium': 'Cooperative when needed',
                'high': 'Warm and compassionate'
            },
            'Neuroticism': {
                'low': 'Emotionally stable and calm',
                'medium': 'Moderate emotional sensitivity',
                'high': 'Emotionally reactive and sensitive'
            }
        }

        if score < 0.4:
            level = 'low'
        elif score < 0.7:
            level = 'medium'
        else:
            level = 'high'

        return interpretations.get(trait, {}).get(level, 'No interpretation available')
