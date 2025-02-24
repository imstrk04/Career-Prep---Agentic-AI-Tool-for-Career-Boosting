import pdfplumber
import json
import requests

# LLaMA 3 API Configuration
LLAMA_API_URL = "http://localhost:12000/api/generate"
MODEL_NAME = "llama3.1:latest"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(filter(None, [page.extract_text() for page in pdf.pages]))
        return text.strip() if text else None
    except Exception as e:
        print(f"Error: Failed to extract text from PDF - {e}")
        return None

def query_llama3(prompt):
    """Sends text data to LLaMA 3 and extracts JSON from the response."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(LLAMA_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        raw_output = response.json().get("response", "").strip()
        
        # Extract JSON from the response
        start_idx = raw_output.find("{")
        end_idx = raw_output.rfind("}") + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = raw_output[start_idx:end_idx]
            return json.loads(json_str)
        return None
    except requests.RequestException as e:
        print(f"Error: Failed to query LLaMA 3 API - {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON from LLaMA response.")
    
    return None

def format_prompt(text):
    """Creates a structured prompt with a sample JSON format for better parsing."""
    sample_json = json.dumps({
        "name": "John Doe",
        "contact": {
            "email": "johndoe@example.com",
            "phone": "+1 234-567-8901",
            "linkedin": "https://linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe"
        },
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "university": "MIT",
                "start_year": 2018,
                "end_year": 2022
            }
        ],
        "experience": [
            {
                "position": "Software Engineer",
                "company": "Google",
                "start_date": "2022-06",
                "end_date": "Present",
                "responsibilities": [
                    "Developed scalable web applications",
                    "Optimized backend performance"
                ]
            }
        ],
        "skills": ["Python", "Machine Learning", "SQL", "Docker"],
        "projects": [
            {
                "title": "AI Chatbot",
                "description": "Built a chatbot using GPT-3 and Flask.",
                "technologies": ["Python", "Flask", "OpenAI API"],
                "link": "https://github.com/johndoe/chatbot"
            }
        ],
        "awards": ["Best AI Project Award - 2021"],
        "certifications": ["AWS Certified Solutions Architect"]
    }, indent=4)

    return f"""
    Extract structured resume details from the following text.
    Return the JSON data in the exact format shown below.
    
    Format:
    {sample_json}
    
    Resume Text:
    {text}
    """

def parse_resume_with_llama(pdf_path):
    """Parses resume from PDF using LLaMA 3."""
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Error: No text found in PDF.")
        return None

    prompt = format_prompt(text)
    return query_llama3(prompt)

def parser_main(pdf_path):
    """Main function that processes the resume and returns the JSON output."""
    # Parse the resume
    parsed_resume = parse_resume_with_llama(pdf_path)
    
    if parsed_resume:
        # Save to file
        json_filename = "parsed_resume_canva.json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(parsed_resume, json_file, indent=4)
        print(f"✅ Resume successfully parsed and saved as {json_filename}")
        
        # Return the parsed JSON
        return parsed_resume
    else:
        print("Error: Failed to parse resume.")
        return None

# Example usage
pdf_path = r"C:\Users\ASUS\Downloads\sadakopa2210221@ssn.edu.in_resume_downloaded.pdf"
result = parser_main(pdf_path)
if result:
    print(json.dumps(result, indent=4))