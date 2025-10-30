from nicegui import ui
import sys, os

sys.path.append(os.path.abspath("D:\\ImprovedScreening\\"))

from prompts import INQUIRY_SYSTEM_PROMPT, DOCTOR_SYSTEM_PROMPT
from recommender import RecommendationEngine

engine = RecommendationEngine("D:\\ImprovedScreening\\assets\\Drs Data.xlsx")

results = {}  # global results storage


def get_recommendation(patient_data):
    """Run engine and return inquiry + doctors"""
    inquiry, doctor_data = engine.get_recommendation(
        patient_data=patient_data,
        system_prompt=INQUIRY_SYSTEM_PROMPT,
    )
    doctors, _ = engine.get_recommendation(
        patient_data=patient_data,
        system_prompt=DOCTOR_SYSTEM_PROMPT,
        doctor_data=doctor_data,
    )
    return {"inquiry": inquiry, "doctors": doctors}


# ---------------- PAGE 1: FORM ----------------
@ui.page('/')
def form_page():
    with ui.column().classes('w-full items-center bg-[#f8f5f2] min-h-screen p-6'):
        # Header with logo on the left
        with ui.row().classes('w-full items-center justify-between mb-6'):
            ui.image("C:\\Users\\doha.ramadan\\Downloads\\ag-logo-en.42bbc5d.png").classes("w-64")
        with ui.column().classes('items-center'):
            ui.html('<h3 style="font-size: 1.5rem; font-weight: bold; color: #7c4c24; text-align: center; margin-top: 1.5rem;">PATIENT MEDICAL FORM</h3>')
        
        # ui.separator().classes('w-full my-4 bg-[#B87C4C]')

        # Personal Information Section - Using your original fields
        with ui.card().classes('w-full max-w-4xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):
            ui.label("PERSONAL INFORMATION").classes("text-xl font-bold text-[#B87C4C] mb-4")
            with ui.grid(columns=2).classes("gap-4 w-full"):
                age = ui.input("Age (years)").classes("w-full")
                gender = ui.select(["Male", "Female"], value="Male", label="Gender").classes("w-full")
                marital_status = ui.select(["Married", "Single", "Divorced", "Widowed"], value="Single", label="Marital Status").classes("w-full")
        
        # Lifestyle Information Section
        with ui.card().classes('w-full max-w-4xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):
            ui.label("LIFESTYLE INFORMATION").classes("text-xl font-bold text-[#B87C4C] mb-4")
            with ui.grid(columns=2).classes("gap-4 w-full"):
                smoke = ui.input("Smoking history").classes("w-full")
                caff = ui.input("Caffeine consumption").classes("w-full")
                alcohol = ui.input("Alcohol consumption").classes("w-full")
        
        # Medical Information Section
        with ui.card().classes('w-full max-w-4xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):
            ui.label("MEDICAL INFORMATION").classes("text-xl font-bold text-[#B87C4C] mb-4")
            with ui.grid(columns=2).classes("gap-4 w-full"):
                meds = ui.input("Current medications").classes("w-full")
                symptoms = ui.input("Current symptoms").classes("w-full")
                allergies = ui.input("Allergies").classes("w-full")
        
        # Family Medical History Section
        with ui.card().classes('w-full max-w-4xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):
            ui.label("FAMILY MEDICAL HISTORY").classes("text-xl font-bold text-[#B87C4C] mb-4")
            with ui.grid(columns=2).classes("gap-4 w-full"):
                patient = ui.input("Patient's medical history").classes("w-full")
                father = ui.input("Father's medical history").classes("w-full")
                mother = ui.input("Mother's medical history").classes("w-full")
                grandparent = ui.input("Grandparents' medical history").classes("w-full")
                sibling = ui.input("Siblings' medical history").classes("w-full")
                children = ui.input("Children's medical history").classes("w-full")

        def on_submit():
            global results
            patient_data = {
                "gender": gender.value,
                "age": age.value,
                "marital_status": marital_status.value,
                "smoke": smoke.value,
                "alcohol": alcohol.value,
                "caff": caff.value,
                "meds": meds.value,
                "symptoms": symptoms.value,
                "allergies": allergies.value,
                "patient": patient.value,
                "father": father.value,
                "mother": mother.value,
                "grandparent": grandparent.value,
                "sibling": sibling.value,
                "children": children.value,
            }
            results = get_recommendation(patient_data)
            ui.navigate.to('/results')

        ui.button("SUBMIT", on_click=on_submit).classes(
            "max-w-4xl mt-4 text-white py-4 px-6 font-medium text-sm "
            "bg-[#B87C4C]! hover:bg-[#A36A40]! rounded"
        )


# ---------------- PAGE 2: RESULTS ----------------
@ui.page('/results')
def results_page():
    with ui.column().classes('w-full items-center bg-[#f8f5f2] min-h-screen p-6'):
        # Header with logo on the left
        with ui.row().classes('w-full items-center justify-between mb-6'):
            ui.image("C:\\Users\\doha.ramadan\\Downloads\\ag-logo-en.42bbc5d.png").classes("w-64")
        with ui.column().classes('items-center'):
            ui.html('<h3 style="font-size: 1.5rem; font-weight: bold; color: #7c4c24; text-align: center; margin-top: 1.5rem;">According to your Data...</h3>')
        
        # Specialty & Diagnosis
        inquiry = results["inquiry"]
        with ui.card().classes('w-full max-w-4xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):
            with ui.row().classes('items-center mb-2'):
                ui.html('<span style="color: #B87C4C; font-weight: bold;">Recommended Specialty: </span>')
                ui.label(f"{inquiry.SPECIALTY}").classes("text-lg")
            with ui.row().classes('items-center'):
                ui.html('<span style="color: #B87C4C; font-weight: bold;">Possible Diagnosis: </span>')
                ui.label(f"{inquiry.DIAGNOSIS}").classes("text-lg")
        
        with ui.card().classes("mt-6 mb-6 p-4 max-w-screen-lg bg-[#EBD9D1] border-l-4 border-[#EBD9D1]"):
            ui.label(f"Visit your Doctor Now").classes(
                "text-lg font-semibold text-[#7c4c24]"
            )

        # Doctors:
        # with ui.card().classes('w-full max-w-6xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):            
        # Create a grid for doctor cards (3 columns)
        with ui.grid(columns=3).classes("gap-6 w-full items-stretch"):
            for doc in results["doctors"]:
                with ui.card().classes("p-0 w-full bg-[#f8f4f0] border-b-4 border-b-[#7c4c24] overflow-hidden shadow-xl h-full"):
                    # Doctor header with name and degree
                    with ui.row().classes("w-full bg-[#7c4c24] p-4 items-center justify-between"):
                        with ui.row().classes("items-center gap-3"):
                            # Gender icon - using different icons for male/female
                            if doc.GENDER == "Male":
                                ui.image("C:\\Users\\doha.ramadan\\Downloads\\1021799.png").classes("w-14 h-14")
                            else:
                                ui.image("C:\\Users\\doha.ramadan\\Downloads\\1361330.png").classes("w-14 h-14")
                            
                            with ui.column().classes("gap-1"):
                                ui.label(f"{doc.NAME}").classes("text-xl font-bold text-[#EBD9D1]")
                                ui.label(f"{doc.DEGREE}").classes("text-md text-white font-medium")

                    # Doctor details - Scope of Service
                    with ui.column().classes("p-4 gap-3"):
                        # Scope of Service section
                        ui.label("Scope of Service:").classes("text-md font-semibold text-black")
                        
                        # Service badges
                        with ui.column().classes("gap-2 mt-2"):
                            for service in doc.SCOPE_OF_SERVICE:
                                ui.label(f"- {service}").classes("text-[#7c4c24] text-sm")

        # Doctor without Doctor Skills:
        # with ui.grid(columns=3).classes("gap-8 justify-center"):
        #     for i, doc in enumerate(results["doctors"]):
        #         with ui.card().classes(
        #             "p-6 bg-[#7c4c24] text-white rounded-xl shadow-2xl "
        #             "w-[320px] min-h-[180px] flex items-center justify-center"
        #         ):
        #             with ui.column().classes("items-center gap-4"):
        #                     if doc.GENDER == "Male":
        #                         ui.image("C:\\Users\\doha.ramadan\\Downloads\\1021799.png").classes("w-16 h-16")
        #                     else:
        #                         ui.image("C:\\Users\\doha.ramadan\\Downloads\\1361330.png").classes("w-16 h-16")

        #                     ui.label(f"{doc.NAME}").classes("text-xl font-bold text-[#EBD9D1]")
        #                     ui.label(f"{doc.DEGREE}").classes("text-md font-medium text-white break-words whitespace-normal")


        ui.button("⬅ BACK TO FORM", on_click=lambda: ui.navigate.to('/')).classes(
            "max-w-4xl mt-4 text-white py-4 px-6 font-medium text-sm "
            "bg-gray-600! hover:bg-gray-700! rounded"
        )


ui.run(port=1972, reload=True)