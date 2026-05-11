from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_resume(resume_text,user_goal):
    prompt=f"""
    you are a senior software engineer and hiring manager.
    
    
    Evaluate the resume based on the users's goal.
    
    User goal:"{user_goal }"
    
    STRICT RULES:
    -Extractonly relevant skills for this goal
    -REMOVE irrelevant tools[excel for backend,etc]
    -Identify real gaps
    - Generate roadmap only for missing fields
    -Make output DIFFERENT based on goal
    
    Return only JSON:
    {{
        "skills":[],
        "missing_skills":[],
        "roadmap":[]
        "interview_questions":[]
        
    }}
    Resume:
    {resume_text}
    
    Goal:
    {user_goal}
    """
    try:
        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            temperature = 0.3,
            messages =[
                {"role":"system","content":"you are a strict hiring manager and senior software engineer"},
                {"role":"user","content":prompt}
                
            ]
        )
        
        content = response.choices[0].message.content.strip()
        
        start = content.find("{")
        end  = content.rfind("}") + 1
        
        return json.loads(content[start:end])
    
    except Exception as e:
        return{
            "skills":[],
            "missing_skills":[],
            "roadmap":[],
            "interview_questions":[],
            "error":str(e)
            
            
        }