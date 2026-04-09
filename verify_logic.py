from processor import parse_resume, clean_text
from matcher import match_resume
import os

def test_screening():
    # Load JD
    with open("data/job_description.txt", "r") as f:
        jd = f.read()
    
    clean_jd = clean_text(jd)
    
    resumes = ["data/resume_john_doe.txt", "data/resume_jane_smith.txt"]
    
    print(f"Testing screening with JD from data/job_description.txt\n")
    
    results = []
    for res_path in resumes:
        with open(res_path, "rb") as f:
            file_bytes = f.read()
            raw_text = parse_resume(file_bytes, os.path.basename(res_path))
            clean_res = clean_text(raw_text)
            match_data = match_resume(clean_res, clean_jd)
            
            results.append({
                "name": os.path.basename(res_path),
                "score": match_data["score"],
                "matched": match_data["matched_skills"],
                "missing": match_data["missing_skills"]
            })
            
    # Sort by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    for r in results:
        print(f"Candidate: {r['name']}")
        print(f"Score: {r['score']}%")
        print(f"Matched Skills: {r['matched']}")
        print(f"Missing Skills: {r['missing']}")
        print("-" * 30)

if __name__ == "__main__":
    test_screening()
