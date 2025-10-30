import os
import sys
from typing import Optional, Tuple, List

sys.path.append(os.path.abspath("D:\\ImprovedScreening\\"))

from llm import fireworks_llm
from prompts import INQUIRY_SYSTEM_PROMPT, DOCTOR_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
import preprocessing
from helpers import Inquiry, Doctor, Parser


class RecommendationEngine:
    """Handles patient-to-specialty and doctor recommendation flow using LLM outputs."""

    def __init__(self, data_path: str):
        # Preprocess data once and store it
        self.preprocessed_df = preprocessing.preprocessing(data_path)
        self.parser = Parser()
        self.llm = fireworks_llm

    def _get_specialties(self) -> List[str]:
        """Extract unique specialties from preprocessed data."""
        return list(self.preprocessed_df['Specialty'].unique())

    def _generate_prompt(self, patient_data: dict) -> str:
        """Generate user prompt based on patient data."""
        return USER_PROMPT_TEMPLATE.format(**patient_data)

    def _call_llm(self, user_prompt: str, system_prompt: str) -> str:
        """Wrapper to call LLM."""
        return self.llm._call(user_prompt, system_prompt)

    def get_recommendation(
        self, patient_data: dict, system_prompt: str, doctor_data: Optional[str] = None
    ) -> Tuple[Inquiry, Optional[List[Doctor]]]:
        """
        Recommend specialty and/or doctors for the given patient data.

        Args:
            patient_data: Patient information dict.
            system_prompt: Either INQUIRY_SYSTEM_PROMPT or DOCTOR_SYSTEM_PROMPT.
            doctor_data: Pre-formatted doctor data if already available.

        Returns:
            A tuple of (parsed inquiry/doctors, doctor_data if applicable).
        """
        user_prompt = self._generate_prompt(patient_data)

        if system_prompt == INQUIRY_SYSTEM_PROMPT:
            system_prompt = system_prompt.format(
                specialties=self._get_specialties(),
                Inquiry=Inquiry.model_json_schema()
            )
            reply = self._call_llm(user_prompt, system_prompt)
            parsed_inquiry = self.parser.clean_inquiry_output(reply)

            doctor_data = preprocessing.format_doctors(
                self.preprocessed_df, parsed_inquiry.SPECIALTY
            )
            return parsed_inquiry, doctor_data

        elif system_prompt == DOCTOR_SYSTEM_PROMPT:
            if not doctor_data:
                raise ValueError("doctor_data must be provided for doctor recommendation step")

            system_prompt = system_prompt.format(
                doctors_data=doctor_data,
                Doctor=Doctor.model_json_schema()
            )
            reply = self._call_llm(user_prompt, system_prompt)
            parsed_doctors = self.parser.clean_doctor_output(reply)
            return parsed_doctors, None

        else:
            raise ValueError("Invalid system prompt provided. Must be INQUIRY_SYSTEM_PROMPT or DOCTOR_SYSTEM_PROMPT.")


engine = RecommendationEngine("D:\\ImprovedScreening\\assets\\Drs Data.xlsx")

patient_data = {
                "gender": "male",
                "age": 45,
                "marital_status": "Single",
                "smoke": "Yes, 10 cigarettes/day",
                "alcohol": "2 CUPS COFFE/DAY",
                "caff": "OCCASIONAL",
                "meds": "OCCASIONAL",
                "symptoms": "Chest Pain",
                "allergies": "Penicillin",
                "patient": "Diabetes",
                "father": "Heart Disease",
                "mother": "None",
                "grandparent": "Hypertension",
                "sibling": "Asthma",
                "children": "Healthy",
            }

inquiry, doctor_data = engine.get_recommendation(
    patient_data,
    system_prompt=INQUIRY_SYSTEM_PROMPT
)

doctors, _ = engine.get_recommendation(
    patient_data,
    system_prompt=DOCTOR_SYSTEM_PROMPT,
    doctor_data=doctor_data
)

for doc in doctors:
    print(doc)