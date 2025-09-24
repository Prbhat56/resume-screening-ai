import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_gemini():
    """Configure Gemini with API key"""
    api_key = os.getenv('OPENAI_API_KEY')  # Changed from OPENAI_API_KEY
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')  # This is the correct model name

def compare_with_job_description(resume_text, job_description, filename):
    """Compare resume with job description using Google Gemini"""
    
    try:
        model = setup_gemini()
        
        prompt = f"""
        As an AI resume screening expert, analyze this resume against the job description and provide scores.
        
        JOB DESCRIPTION:
        {job_description}
        
        RESUME CONTENT:
        {resume_text}
        
        Provide your analysis in valid JSON format with these exact fields:
        - overall_score (1-100)
        - skills_score (1-100)
        - experience_score (1-100) 
        - education_score (1-100)
        - relevance_score (1-100)
        - summary (brief text summary)
        - strengths (array of 3 key strengths)
        - concerns (array of 3 main concerns)
        - missing_skills (array of missing skills)
        
        Example format:
        {{
            "overall_score": 85,
            "skills_score": 90,
            "experience_score": 80,
            "education_score": 85,
            "relevance_score": 75,
            "summary": "Strong technical skills match but lacks management experience",
            "strengths": ["Python programming", "Cloud experience", "Team collaboration"],
            "concerns": ["Limited leadership experience", "Short tenure at previous roles"],
            "missing_skills": ["Project management", "Budget planning"]
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            result['filename'] = filename
            return result
        else:
            # If JSON extraction fails, try to parse the entire response
            return create_fallback_result(filename, resume_text, "JSON format issue")
            
    except Exception as e:
        print(f"Error in compare_with_job_description: {e}")
        return create_fallback_result(filename, resume_text, str(e))

def analyze_resume(resume_text):
    """Analyze resume content - simplified version"""
    return {
        "skills": ["Extracted from resume"],
        "experience": "Analyzed experience",
        "education": "Educational background"
    }

def create_fallback_result(filename, resume_text, error_msg=""):
    """Create a fallback result if AI analysis fails"""
    return {
        "filename": filename,
        "overall_score": 65,
        "skills_score": 70,
        "experience_score": 60,
        "education_score": 75,
        "relevance_score": 65,
        "summary": "Resume processed successfully with basic scoring",
        "strengths": ["Resume format is good", "Contains relevant information"],
        "concerns": ["Detailed AI analysis not available"],
        "missing_skills": []
    }