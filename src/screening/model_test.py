from llm import fireworks_llm
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

def get_recommendation(data: dict):
    user_prompt = USER_PROMPT_TEMPLATE.format(**data)
    system_prompt = SYSTEM_PROMPT
    
    # Call Fireworks with system + user messages
    response = fireworks_llm._call(user_prompt, system_prompt)
    return response

# Example use
if __name__ == "__main__":
    patient_data = {
        "gender": "Male",
        "age": "45",
        "marital_status": "Married",
        "smoke": "Yes, 10 cigarettes/day",
        "alcohol": "Occasional",
        "caff": "2 cups coffee/day",
        "meds": "Metformin",
        "symptoms": "Chest pain",
        "allergies": "Penicillin",
        "patient": "Diabetes",
        "father": "Heart disease",
        "mother": "None",
        "grandparent": "Hypertension",
        "sibling": "Asthma",
        "children": "Healthy"
    }

    print(get_recommendation(patient_data))