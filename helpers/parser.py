import re
import json
from helpers import Inquiry, Doctor
from typing import List

class Parser:
    def __init__(self):
        pass

    def clean_inquiry_output(self, text: str):
        """Clean and validate inquiry output into an Inquiry model."""
        # Remove ```json ... ``` or ``` ... ```
        cleaned_inquiry = re.sub(r"^```(?:json)?\n|\n```$", "", text.strip())
        inquiry = Inquiry.model_validate_json(cleaned_inquiry)
        return inquiry

    def clean_doctor_output(self, text: str) -> List["Doctor"]:
        """Clean and validate doctor output into a list of Doctor models."""
        # Remove ```json ... ``` or ``` ... ```
        cleaned_doctor = re.sub(r"^```(?:json)?\n|\n```$", "", text.strip())

        parsed_json = json.loads(cleaned_doctor)

        validated_doctors = []
        for doc in parsed_json:
            validated_doctor = Doctor(**doc)
            validated_doctors.append(validated_doctor)

        return validated_doctors