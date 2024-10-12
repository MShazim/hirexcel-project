from django.conf import settings
from openai import OpenAI

class ChatGPTIntegration:
    def __init__(self):
        # Instantiate the OpenAI client
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_candidate_status(self, personality_report_fields, job_position):
        prompt = f"""
        Based on the following personality assessment data: {personality_report_fields},
        and the job position '{job_position}', determine whether the candidate is either "Recommended" or "Not Recommended" 
        for this role. Please only provide one of these two responses, and nothing else.
        """
        response = self.client.chat.completions.create(  # New client-based method
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        return response.choices[0].message.content.strip()

    def generate_profile_synopsis(self, personality_report_fields):
        prompt = f"""
        Based on the following personality assessment data: {personality_report_fields},
        generate a concise, complete, and professional summary of exactly 100 words.
        Ensure the summary is well-aligned with the provided data and does not exceed or fall short of the 100-word requirement.
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def generate_optimal_job_matches(self, personality_report_fields):
        prompt = f"""
        Based on the following personality assessment data: {personality_report_fields},
        provide exactly 1 to 5 optimal job matches in the domain of 'Software Engineering/Computer Science' that perfectly align with the data.
        Only list the job titles without any additional details or descriptions.
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=50,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()



