from models import JobOpening, Candidate
import PyPDF2
import docx
import spacy
from extensions import db  # Import db from extensions.py

nlp = spacy.load("en_core_web_lg")

def validate_resume(filepath, job_id, candidate_experience):
    # Load job details from the database
    print("Validating resume for job_id:", job_id)
    job = JobOpening.query.get(job_id)  # Fetch job details from the database

    if not job:  
        raise ValueError(f"No job found for job_id: {job_id}")

    # Extract job attributes safely
    job_description = job.description or ""
    role_text = job.role or ""
    required_experience = job.experience or 0

    # Extract must-have and good-to-have skills
    must_have_skills = set(skill.lower() for skill in (job.must_have or "").split(",") if skill)
    good_to_have_skills = set(skill.lower() for skill in (job.good_to_have or "").split(",") if skill)

    # Process job text using SpaCy
    job_role_doc = nlp(role_text)

    # Extract text from resume
    resume_text = extract_text_from_resume(filepath)
    resume_doc = nlp(resume_text)

    # Extract keywords from resume
    resume_words = set(token.text.lower() for token in resume_doc if not token.is_stop)

    # Must-Have Skills Matching (instead of similarity)
    matched_must_have_skills = must_have_skills.intersection(resume_words)
    print("matched_must_have_skills", matched_must_have_skills)
    must_have_score = len(matched_must_have_skills) / len(must_have_skills) if must_have_skills else 0

    # Good-to-Have Skills Matching
    matched_good_to_have_skills = good_to_have_skills.intersection(resume_words)
    print("matched_good_to_have_skills", matched_good_to_have_skills)
    good_to_have_score = len(matched_good_to_have_skills) / len(good_to_have_skills) if good_to_have_skills else 0

    # Semantic Similarity for Description & Role
    description_score = compute_description_score(resume_doc, job_description)
    print("description_score", description_score)
    role_score = resume_doc.similarity(job_role_doc)
    print("role_score", role_score)

    # Compute Experience Score
    experience_score = compute_experience_score(candidate_experience, required_experience)
    print("experience_score", experience_score)
    # Final Weighted Score Calculation
    total_score = (
        (experience_score * 0.3) +  # Experience weight increased
        (must_have_score * 0.5) +          # Must-have skills weight increased
        (good_to_have_score * 0.1) +
        (description_score * 0.05) +
        (role_score * 0.05)
    )

    return total_score > 0.6, total_score  # Match threshold at 60%


def compute_description_score(resume_doc, job_description):
    job_description_doc = nlp(job_description)

    # Extract important keywords from job description
    job_keywords = {token.text.lower() for token in job_description_doc if not token.is_stop and token.is_alpha}
    resume_words = {token.text.lower() for token in resume_doc if not token.is_stop and token.is_alpha}

    # Keyword matching score
    matched_keywords = job_keywords.intersection(resume_words)
    keyword_score = len(matched_keywords) / len(job_keywords) if job_keywords else 0

    # Semantic similarity score (only if keywords are found)
    similarity_score = resume_doc.similarity(job_description_doc) if keyword_score > 0 else 0

    # Weighted scoring
    return (keyword_score * 0.7) + (similarity_score * 0.3)  # More weight to keyword match

def compute_experience_score(candidate_experience, required_experience):
    required_experience = float(required_experience)
    candidate_experience = float(candidate_experience)
    if not required_experience or required_experience <= 0:
        return 1.0  # If no experience requirement is given, assume full score

    return min(candidate_experience / required_experience, 1.0)

def extract_text_from_resume(filepath):
    """Extract text from a PDF or DOCX resume."""
    if filepath.endswith(".pdf"):
        return extract_text_from_pdf(filepath)
    elif filepath.endswith(".docx"):
        return extract_text_from_docx(filepath)
    else:
        return "Unsupported file format."

def extract_text_from_pdf(filepath):
    """Extract text from a PDF file."""
    try:
        with open(filepath, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(filepath):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {e}"
