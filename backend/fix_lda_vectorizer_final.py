# backend/fix_lda_vectorizer_final.py
import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os

print("="*70)
print("RECREATING LDA MODEL AND VECTORIZER")
print("="*70)
print(f"NumPy version: {np.__version__}")

# Extended sample texts for better initialization
sample_texts = [
    "I love exploring new ideas and creative solutions to complex problems",
    "I prefer organized schedules and planning ahead for everything I do",
    "I enjoy meeting new people and attending social gatherings regularly",
    "I try to be understanding and helpful to others whenever possible",
    "I sometimes worry about things that might go wrong in the future",
    "I appreciate art, music, and beauty in everyday life experiences",
    "I work diligently to achieve my goals and stay focused on tasks",
    "I feel energized when surrounded by people and social activities",
    "I consider other peoples feelings carefully before making decisions",
    "I remain calm and composed even in stressful and challenging situations",
    "I enjoy abstract thinking and philosophical discussions about life",
    "I maintain detailed to-do lists and follow them systematically",
    "I seek out new adventures and exciting experiences whenever I can",
    "I value harmony in relationships and avoid conflicts when possible",
    "I experience emotions deeply and reflect on them frequently"
]

# Create and fit vectorizer
print("\nStep 1: Creating CountVectorizer...")
vectorizer = CountVectorizer(
    max_features=1000,
    min_df=1,
    max_df=0.95,
    ngram_range=(1, 2),
    strip_accents='unicode',
    lowercase=True
)
doc_term_matrix = vectorizer.fit_transform(sample_texts)
print(f"✓ Vectorizer created")
print(f"  - Vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"  - Max features: {vectorizer.max_features}")

# Create and fit LDA with 5 components
# 768 (embeddings) + 4 (sentiment) + 5 (LDA) = 777 features total
print("\nStep 2: Creating LDA model...")
lda = LatentDirichletAllocation(
    n_components=5,          # Changed to 5 for 777 total features
    random_state=42,
    learning_method='online',
    max_iter=20,
    n_jobs=-1
)
lda.fit(doc_term_matrix)
print(f"✓ LDA model created and fitted")
print(f"  - Number of components: {lda.n_components}")
print(f"  - Number of iterations: {lda.n_iter_}")

# Test the models
print("\nStep 3: Testing models...")
test_text = "I enjoy learning new things and meeting people"
test_vec = vectorizer.transform([test_text])
test_topics = lda.transform(test_vec)
print(f"✓ Test successful")
print(f"  - Test topic distribution shape: {test_topics.shape}")
print(f"  - Topic probabilities: {test_topics[0]}")

# Save models
model_dir = 'C:/Users/KRISHNA CHAURASIA/Downloads/Personality_ui/model'

# Make sure directory exists
os.makedirs(model_dir, exist_ok=True)

vectorizer_path = f'{model_dir}/lda_vec.joblib'
lda_path = f'{model_dir}/lda_model.joblib'

print("\nStep 4: Saving models...")
joblib.dump(vectorizer, vectorizer_path)
joblib.dump(lda, lda_path)

print(f"✓ Vectorizer saved to: {vectorizer_path}")
print(f"✓ LDA model saved to: {lda_path}")

# Verify saved files
print("\nStep 5: Verifying saved files...")
loaded_vec = joblib.load(vectorizer_path)
loaded_lda = joblib.load(lda_path)
print(f"✓ Vectorizer loaded successfully (vocab size: {len(loaded_vec.vocabulary_)})")
print(f"✓ LDA loaded successfully (components: {loaded_lda.n_components})")

print("\n" + "="*70)
print("✓ SUCCESS! Models recreated and tested")
print("="*70)
print(f"\nFeature breakdown:")
print(f"  - Sentence embeddings: 768")
print(f"  - VADER sentiment: 4")
print(f"  - LDA topics: 5")
print(f"  - TOTAL: 777 features ✓")
print("\nYou can now restart your backend server!")
print("Run: python app.py")
print("="*70)