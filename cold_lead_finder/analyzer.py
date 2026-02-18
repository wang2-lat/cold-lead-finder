from openai import OpenAI
from typing import Dict

class LeadAnalyzer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def analyze(self, post: Dict) -> Dict:
        """Analyze post and generate personalized email."""
        
        prompt = f"""Analyze this social media post and extract:
1. The main pain point (1 sentence)
2. A personalized cold email template (3-4 sentences max)

Post Title: {post['title']}
Post Content: {post['content'][:500]}

Format response as:
PAIN_POINT: <pain point>
EMAIL: <email template>"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sales expert analyzing potential customer pain points."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse response
            pain_point = ""
            email_template = ""
            
            if "PAIN_POINT:" in content:
                pain_point = content.split("PAIN_POINT:")[1].split("EMAIL:")[0].strip()
            if "EMAIL:" in content:
                email_template = content.split("EMAIL:")[1].strip()
            
            return {
                "pain_point": pain_point,
                "email_template": email_template
            }
        
        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                "pain_point": "Unable to analyze",
                "email_template": "Unable to generate"
            }