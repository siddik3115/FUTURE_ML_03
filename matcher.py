import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # Fallback if model load fails (though we installed it)
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# A comprehensive list of technical skills
TECHNICAL_SKILLS = [
    "python", "java", "c++", "javascript", "typescript", "html", "css", "react", "angular", "vue",
    "node.js", "express", "django", "flask", "fastapi", "spring boot", "hibernate", "sql", "postgresql",
    "mysql", "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp", "git", "jenkins",
    "terraform", "ansible", "machine learning", "deep learning", "nlp", "computer vision", "statistics",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "tableau", "power bi", "excel",
    "pyspark", "hadoop", "spark", "kafka", "elasticsearch", "graphql", "rest api", "microservices",
    "agile", "scrum", "devops", "ci/cd", "selenium", "pytest", "unit testing", "linux", "bash", "shell",
    "go", "rust", "php", "ruby", "rails", "swift", "kotlin", "objective-c", "flutter", "react native",
    "c#", ".net", "azure devops", "solidity", "blockchain", "web3", "cybersecurity", "ui/ux", "figma"
]

def extract_skills(text):
    """Extract skills from text based on a predefined list."""
    text = text.lower()
    found_skills = set()
    
    # We use a simple keyword matching for speed, but could use spaCy NER or pattern matching
    for skill in TECHNICAL_SKILLS:
        # Match skill as a whole word to avoid partial matches (e.g., 'go' in 'good')
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
            
    return sorted(list(found_skills))

def calculate_similarity(resume_text, job_description):
    """Calculate cosine similarity between resume and job description."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(similarity[0][0])

def match_resume(resume_text, job_description):
    """Perform full matching logic."""
    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    # Calculate similarity score
    score = calculate_similarity(resume_text, job_description)
    
    # Identify matches and gaps
    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]
    
    return {
        "score": round(score * 100, 2),
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
