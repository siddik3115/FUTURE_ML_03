1. Overview

This project is an AI-powered system that automatically screens and ranks resumes based on a given job description. It helps recruiters quickly identify the most suitable candidates by analyzing skills, experience, and qualifications using NLP techniques.

2. Objective
Automate resume screening process
Match candidate profiles with job requirements
Rank candidates based on relevance
Reduce manual effort in recruitment
3. Dataset

The dataset consists of resumes in PDF or text format along with job descriptions. It includes information such as:

Candidate Name
Skills
Education
Work Experience
4. Features
Resume parsing (PDF/Text extraction)
Text preprocessing (cleaning, tokenization, stopword removal)
Skill extraction using NLP
Resume-job matching
Candidate ranking and scoring
Highlighting matched and missing skills
5. Technologies Used
Python
NLTK / spaCy – NLP processing
Scikit-learn – TF-IDF & similarity models
Pandas & NumPy – Data handling
PyPDF2 / pdfplumber – Resume parsing
Streamlit / Flask (optional) – Web interface
6. Workflow
Resume Upload / Data Collection
Text Extraction from resumes
Data Preprocessing
Feature Extraction (TF-IDF)
Similarity Calculation (Cosine Similarity)
Candidate Scoring & Ranking
Result Display
7. Output
Ranked list of candidates
Matching score for each resume
Extracted skills from resumes
Missing skills based on job description
8. Key Benefits
Faster hiring process
Reduced manual screening effort
Improved candidate-job matching
Better decision-making for recruiters
9. How to Run
# Clone the repository
git clone https://github.com/your-username/resume-screening-system.git

# Navigate to project folder
cd resume-screening-system

# Install dependencies
pip install -r requirements.txt

# Run the project
python app.py
10. Applications
HR recruitment systems
Job portals
Corporate hiring processes
11. Contribution

Contributions are welcome! Feel free to fork the repository and submit a pull request.

12. License

This project is open-source and available under the MIT License.
