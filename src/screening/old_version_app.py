from nicegui import ui
from llm import fireworks_llm
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
import json
import os

# Global variable to store results between pages
results = {}

def get_recommendation(data: dict):
    user_prompt = USER_PROMPT_TEMPLATE.format(**data)
    reply = fireworks_llm._call(user_prompt, system_prompt=SYSTEM_PROMPT)

    cleaned = reply.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")  # remove all backticks
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):].strip()

    try:
        parsed = json.loads(cleaned)  # safe JSON parsing
    except Exception as e:
        parsed = {"error": f"Model did not return valid JSON: {e}", "raw": reply}

    return parsed

# ---------- Helper to render sections ----------
def render_section(title: str, items, fmt_dict, fmt_str):
    """Render a recommendation section that may be a list of dicts or a newline string"""
    with ui.card().classes("mb-6 p-6 w-full max-w-screen-lg bg-white border-b-4 border-b-[#7c4c24] shadow-md"):
        ui.label(title).classes("text-2xl font-semibold text-[#B87C4C] mb-4")

        if isinstance(items, str):
            for line in items.split("\n"):
                if line.strip():
                    ui.markdown(f"- {line.strip()}")
        elif isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    line = fmt_dict(item)
                    ui.markdown(line)
                elif isinstance(item, str):
                    ui.markdown(f"- {item.strip()}")

# ---------------- PAGE 1: FORM ----------------
@ui.page('/')
def form_page():
    # Header with Andalusian Health branding
    with ui.column().classes('w-full items-center bg-[#EBD9D1] min-h-screen p-6'):
        # Header section with logo
        with ui.column().classes('w-full items-center mb-6'):
            # logo
            ui.image("C:\\Users\\doha.ramadan\\Downloads\\ag-logo-en.42bbc5d.png").classes("w-64 mb-4")
            ui.html('<h3 style="font-size: 1.5rem; font-weight: bold; color: #7c4c24; text-align: center; margin-top: 1rem;">PATIENT MEDICAL FORM</h3>')
            ui.separator().classes('w-full my-4 bg-[#B87C4C]')
        
        # Personal Information Section - Using your original fields
        with ui.card().classes('w-full max-w-4xl mb-6 p-6 bg-white shadow-md border border-[#B87C4C]'):
            ui.label("PERSONAL INFORMATION").classes("text-xl font-bold text-[#B87C4C] mb-4")
            with ui.grid(columns=2).classes("gap-4 w-full"):
                age = ui.input("Age (years)").classes("w-full")
                gender = ui.select(["Male", "Female"], value="Male", label="Gender").classes("w-full")
                marital_status = ui.select(["Married", "Single"], value="Single", label="Marital Status").classes("w-full")
        
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
    with ui.column().classes("w-full items-center bg-[#EBD9D1] min-h-screen p-6"):
        # Header section with logo
        with ui.column().classes('w-full items-center mb-6'):
            ui.image("C:\\Users\\doha.ramadan\\Downloads\\ag-logo-en.42bbc5d.png").classes("w-64 mb-4")
            ui.html('<h3 style="font-size: 1.5rem; font-weight: bold; color: #7c4c24; text-align: center; margin-top: 1rem;">MEDICAL RECOMMENDATIONS</h3>')
            ui.separator().classes('w-full my-4 bg-[#B87C4C]')

        if not results:
            ui.label("⚠️ No results available. Please go back and submit the form.").classes(
                "text-red-600 text-lg"
            )
            ui.button("Back", on_click=lambda: ui.navigate.to('/')).classes("mt-4 bg-[#B87C4C] text-white")
            return

        if "error" in results:
            ui.label(results["error"]).classes("text-red-500 font-semibold")
            ui.textarea(value=results["raw"], label="Raw Output").props("readonly").classes(
                "w-full h-40 max-w-screen-lg"
            )

        else:
            # 🔹 Add specialty line 
            specialty = results.get("MostSuitableSpecialty")
            if specialty:
                with ui.card().classes("mt-3 mb-6 p-4 max-w-screen-lg bg-[#7c4c24] border-l-4 border-[#7c4c24]"):
                    ui.label(f"The most appropriate specialty for you is: {specialty}").classes(
                        "text-lg font-semibold text-white"
                    )

            render_section(
                "🩺 Medication",
                results.get("medication", []),
                lambda med: f"- **{med.get('name','')}**: {med.get('dosage','')} {med.get('frequency','')} ({med.get('reason','')})",
                lambda s: f"- {s.strip()}",
            )

            render_section(
                "🔬 Labs and Scans",
                results.get("labsAndScans", []),
                lambda lab: f"- **{lab.get('test','')}** ({lab.get('reason','')})",
                lambda s: f"- {s.strip()}",
            )

            render_section(
                "📘 Patient Education",
                results.get("patientEducation", []),
                lambda edu: f"- **{edu.get('topic','')}**: {edu.get('details','')}",
                lambda s: f"- {s.strip()}",
            )

        with ui.row().classes("gap-4 w-full max-w-screen-lg mt-8"):
            ui.button("⬅️ Back to Form", on_click=lambda: ui.navigate.to('/')).classes(
                "flex-1 text-lg text-white bg-[#B87C4C] hover:bg-[#A36A40] rounded"
            )
            ui.button("👨‍⚕️ Recommended Doctors", on_click=lambda: ui.navigate.to('/doctors')).classes(
                "flex-1 text-lg text-white bg-[#B87C4C] hover:bg-[#A36A40] rounded"
            )


# ---------------- PAGE 3: DOCTORS ----------------
@ui.page('/doctors')
def doctors_page():
    with ui.column().classes("w-full items-center bg-[#EBD9D1] min-h-screen p-6"):
        # Header section with logo
        with ui.column().classes('w-full items-center mb-6'):
            ui.image("C:\\Users\\doha.ramadan\\Downloads\\ag-logo-en.42bbc5d.png").classes("w-64 mb-4")
            ui.html('<h3 style="font-size: 1.5rem; font-weight: bold; color: #7c4c24; text-align: center; margin-top: 1rem;">RECOMMENDED DOCTORS</h3>')
            ui.separator().classes('w-full my-4 bg-[#B87C4C]')

        doctors = [
            {"name": "Dr. Sarah Mohamed", "specialty": "Professor in Cardiology", "rating": 4.8, "gender": "female",
             "phone": "055-123-4567", "dates": ["Mon 10:00-14:00", "Wed 12:00-16:00", "Fri 09:00-13:00"]},
            {"name": "Dr. Ahmed Hassan", "specialty": "Consultant in Cardiology", "rating": 4.6, "gender": "male",
             "phone": "055-234-5678", "dates": ["Tue 09:00-13:00", "Thu 14:00-18:00"]},
            {"name": "Dr. Dina Mustafa", "specialty": "Specialist in Cardiology", "rating": 4.9, "gender": "female",
             "phone": "055-345-6789", "dates": ["Mon 08:00-12:00", "Wed 14:00-18:00", "Sat 10:00-14:00"]},
        ]

        with ui.column().classes("gap-6 w-full items-center"):  # Changed to center items
            for doc in doctors:
                # Added max-w-lg to limit card width while keeping everything else the same
                with ui.card().classes("p-0 max-w-lg w-full bg-[#f8f4f0] border-b-4 border-b-[#7c4c24] overflow-hidden shadow-xl"):  # Changed shadow to shadow-xl
                    # Doctor header with name, specialty and gender image
                    with ui.row().classes("w-full bg-[#7c4c24] p-4 items-center justify-between"):
                        with ui.row().classes("items-center gap-3"):
                            # Gender icon - using different icons for male/female
                            if doc["gender"] == "male":
                                ui.image("C:\\Users\\doha.ramadan\\Downloads\\1021799.png").classes("w-14 h-14")  # Smaller size
                            else:
                                ui.image("C:\\Users\\doha.ramadan\\Downloads\\1361330.png").classes("w-14 h-14")  # Smaller size
                            
                            with ui.column().classes("gap-1"):
                                ui.label(doc["name"]).classes("text-xl font-bold text-[#EBD9D1]")
                                ui.label(doc["specialty"]).classes("text-md text-white font-medium")
                        
                        # Rating badge
                        with ui.column().classes("items-center bg-[#EBD9D1] p-2 rounded-lg"):
                            ui.label("⭐").classes("text-[#7c4c24] text-sm")
                            ui.label(f"{doc['rating']}").classes("text-[#7c4c24] font-bold text-md")
                    
                    # Doctor details
                    with ui.column().classes("p-4 gap-3"):
                        # Phone number
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("phone", color="#7c4c24").classes("text-lg")
                            ui.label(doc["phone"]).classes("text-[#7c4c24] font-medium")
                        
                        # Availability section
                        ui.label("Available Dates & Times:").classes("text-md font-semibold text-[#7c4c24] mt-2")
                        
                        # Date badges
                        with ui.row().classes("flex-wrap gap-2 mt-2"):
                            for date in doc["dates"]:
                                ui.label(date).classes("bg-[#EBD9D1] text-[#7c4c24] px-3 py-1 rounded-full text-sm")


# ---------------- RUN APP ----------------
ui.run(port=1234, reload=True)