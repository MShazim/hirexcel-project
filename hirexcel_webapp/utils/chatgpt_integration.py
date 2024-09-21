import openai

class ChatGPTIntegration:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_candidate_status(self, personality_report_fields, job_position):
        prompt = f"Based on the following personality assessment data: {personality_report_fields} and the job position '{job_position}', is the candidate recommended or not recommended for the job?"
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",  # Using GPT-4-turbo for performance
            messages=[{"role": "system", "content": prompt}],
            max_tokens=10
        )
        return response['choices'][0]['message']['content'].strip()

    def generate_profile_synopsis(self, personality_report_fields):
        prompt = f"Create a concise 100-word professional summary based on the following personality assessment data: {personality_report_fields}"
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",  # Using GPT-4-turbo
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150  # Set for approximately 100 words
        )
        return response['choices'][0]['message']['content'].strip()

    def generate_optimal_job_matches(self, personality_report_fields):
        prompt = f"Based on the following personality assessment data: {personality_report_fields}, recommend up to 5 optimal job matches in the domain of 'Software Engineering/Computer Science'."
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",  # Using GPT-4-turbo
            messages=[{"role": "system", "content": prompt}],
            max_tokens=50
        )
        return response['choices'][0]['message']['content'].strip()
