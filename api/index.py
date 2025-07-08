import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# --- Initialize Supabase Client ---
# Fetches the credentials securely from Vercel's Environment Variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Create the FastAPI app object
app = FastAPI(title="10 Key Points Assessment API v1.1")

# --- Add CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Re-usable Logic Functions (all 10) ---
# (These functions are the same as before)
def generate_sentence_1(service_type, prudential_cat, legal_status, clients):
    if not any([service_type, prudential_cat, legal_status, clients]): return None
    parts = [f"provide **{service_type}** services", f"under a **{prudential_cat}** Prudential classification", f"as a **{legal_status}**", f"targeting **{clients}** clients"]
    return "The firm is seeking authorization to " + ", ".join(p for p in parts if p.split()[-1] != "**None**") + "."
def generate_sentence_2(model_desc, markets, geo_scope, channels):
    if not model_desc: return None
    parts = [f"a **{model_desc}**", f"focused on **{markets}**", f"across **{geo_scope}**", f"delivered via **{channels}**"]
    return "The applicant describes its business model as " + ", ".join(p for p in parts if p.split()[-1] != "**None**") + "."
def generate_sentence_3(structure, parent_name, parent_jurisdiction, controller_name, controller_perc):
    if not structure: return None
    parts = [f"The firm is **{structure}**"]
    if parent_name and parent_jurisdiction: parts.append(f", **{parent_name}**, incorporated in **{parent_jurisdiction}**")
    if controller_name and controller_perc: parts.append(f"with ultimate control resting with **{controller_name}** holding **{controller_perc}** equity")
    return " ".join(parts) + "."
def generate_sentence_4(key_individuals, experience_summary):
    if not key_individuals: return None
    sentence = f"The business will be run by **{key_individuals}**"
    if experience_summary: sentence += f", who has **{experience_summary}**."
    return sentence
def generate_sentence_5(adverse_history, previous_regulators):
    if not adverse_history: return f"The firm and its key individuals have no adverse regulatory history. Key personnel are known to other regulators, including the **{previous_regulators}**."
    return f"The firm has an adverse history involving: **{adverse_history}**. Key personnel are known to other regulators, including the **{previous_regulators}**."
def generate_sentence_6(systems_overview, outsourcing_arrangements):
    if not systems_overview: return None
    sentence = f"The applicant has documented systems for **{systems_overview}**"
    if outsourcing_arrangements: sentence += f", with key outsourced support from **{outsourcing_arrangements}**."
    return sentence
def generate_sentence_7(compliance_officer, mlro, screening_tools):
    if not compliance_officer and not mlro: return None
    parts = []
    if compliance_officer == mlro and compliance_officer: parts.append(f"has appointed **{compliance_officer}** as the combined Compliance Officer and MLRO")
    else:
        if compliance_officer: parts.append(f"has appointed **{compliance_officer}** as the Compliance Officer")
        if mlro: parts.append(f"and **{mlro}** as the MLRO")
    sentence = "The firm " + " ".join(parts)
    if screening_tools: sentence += f", and will use **{screening_tools}** for screening purposes."
    return sentence
def generate_sentence_8(capital_requirement, source_of_funds):
    if not capital_requirement or not source_of_funds: return None
    return f"The firm will meet the **{capital_requirement}** capital requirement through **{source_of_funds}**."
def generate_sentence_9(disclosures):
    if not disclosures: return "No other material matters or disclosures were noted."
    return f"The firm disclosed the following: **{disclosures}**."
def generate_sentence_10(recommendation, conditions):
    if not recommendation: return None
    sentence = f"Recommendation: **{recommendation}**."
    if conditions: sentence += f" This is subject to the following conditions: **{conditions}**."
    return sentence

# --- Pydantic Model for Full Assessment Input ---
class FullAssessmentIn(BaseModel):
    applicant_name: Optional[str] = None
    p1_service_type: Optional[str] = None
    p1_prudential_cat: Optional[str] = None
    p1_legal_status: Optional[str] = None
    p1_clients: Optional[str] = None
    p2_model_desc: Optional[str] = None
    p2_markets: Optional[str] = None
    p2_geo_scope: Optional[str] = None
    p2_channels: Optional[str] = None
    p3_structure: Optional[str] = None
    p3_parent_name: Optional[str] = None
    p3_parent_jurisdiction: Optional[str] = None
    p3_controller_name: Optional[str] = None
    p3_controller_perc: Optional[str] = None
    p4_key_individuals: Optional[str] = None
    p4_experience: Optional[str] = None
    p5_adverse_history: Optional[str] = None
    p5_previous_reg: Optional[str] = None
    p6_systems: Optional[str] = None
    p6_outsourcing: Optional[str] = None
    p7_co: Optional[str] = None
    p7_mlro: Optional[str] = None
    p7_tools: Optional[str] = None
    p8_capital: Optional[str] = None
    p8_sof: Optional[str] = None
    p9_disclosures: Optional[str] = None
    p10_rec: Optional[str] = None
    p10_cond: Optional[str] = None

class SubmissionResponse(BaseModel):
    message: str

# --- API Endpoints ---
@app.post("/submit_assessment", response_model=SubmissionResponse, tags=["Assessment Actions"])
def submit_full_assessment(assessment: FullAssessmentIn):
    """
    Receives all form data, generates all 10 sentences,
    and saves the entire record to the Supabase database.
    """
    # Create a dictionary of the inputs to save
    db_record = assessment.dict()

    # Generate all sentences and add them to the record
    db_record['p1_output'] = generate_sentence_1(assessment.p1_service_type, assessment.p1_prudential_cat, assessment.p1_legal_status, assessment.p1_clients)
    db_record['p2_output'] = generate_sentence_2(assessment.p2_model_desc, assessment.p2_markets, assessment.p2_geo_scope, assessment.p2_channels)
    db_record['p3_output'] = generate_sentence_3(assessment.p3_structure, assessment.p3_parent_name, assessment.p3_parent_jurisdiction, assessment.p3_controller_name, assessment.p3_controller_perc)
    db_record['p4_output'] = generate_sentence_4(assessment.p4_key_individuals, assessment.p4_experience)
    db_record['p5_output'] = generate_sentence_5(assessment.p5_adverse_history, assessment.p5_previous_reg)
    db_record['p6_output'] = generate_sentence_6(assessment.p6_systems, assessment.p6_outsourcing)
    db_record['p7_output'] = generate_sentence_7(assessment.p7_co, assessment.p7_mlro, assessment.p7_tools)
    db_record['p8_output'] = generate_sentence_8(assessment.p8_capital, assessment.p8_sof)
    db_record['p9_output'] = generate_sentence_9(assessment.p9_disclosures)
    db_record['p10_output'] = generate_sentence_10(assessment.p10_rec, assessment.p10_cond)

    try:
        # Insert the completed record into the 'assessments' table
        supabase.table('assessments').insert(db_record).execute()
        return {"message": "Assessment submitted successfully!"}
    except Exception as e:
        # Return a more specific error if possible
        return {"message": f"Error saving to database: {str(e)}"}

@app.get("/", summary="API Root", include_in_schema=False)
async def read_root():
    return {"message": "Welcome to the 10 Key Points Assessment API. Go to /docs for details."}