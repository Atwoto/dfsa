from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Create the FastAPI app object
app = FastAPI(
    title="10 Key Points Assessment API",
    description="An API to generate standardized assessment sentences based on input data.",
    version="1.0.0",
)

# --- Re-usable Logic Functions ---

def generate_sentence_1(service_type, prudential_cat, legal_status, clients):
    if not any([service_type, prudential_cat, legal_status, clients]): return None
    parts = []
    if service_type: parts.append(f"provide **{service_type}** services")
    else: parts.append("provide financial services")
    if prudential_cat: parts.append(f"under a **{prudential_cat}** Prudential classification")
    if legal_status: parts.append(f"as a **{legal_status}**")
    if clients: parts.append(f"targeting **{clients}** clients")
    return "The firm is seeking authorization to " + ", ".join(parts) + "."

def generate_sentence_2(model_desc, markets, geo_scope, channels):
    if not model_desc: return None
    parts = [f"a **{model_desc}**"]
    if markets: parts.append(f"focused on **{markets}**")
    if geo_scope: parts.append(f"across **{geo_scope}**")
    if channels: parts.append(f"delivered via **{channels}**")
    return "The applicant describes its business model as " + ", ".join(parts) + "."

def generate_sentence_3(structure, parent_name, parent_jurisdiction, controller_name, controller_perc):
    if not structure: return None
    parts = [f"The firm is **{structure}**"]
    if parent_name and parent_jurisdiction: parts.append(f", **{parent_name}**, incorporated in **{parent_jurisdiction}**")
    elif parent_name: parts.append(f", **{parent_name}**")
    if controller_name and controller_perc: parts.append(f"with ultimate control resting with **{controller_name}** holding **{controller_perc}** equity")
    elif controller_name: parts.append(f"with ultimate control resting with **{controller_name}**")
    return " ".join(parts) + "."

def generate_sentence_4(key_individuals, experience_summary):
    if not key_individuals: return None
    sentence = f"The business will be run by **{key_individuals}**"
    if experience_summary: sentence += f", who has **{experience_summary}**."
    else: sentence += "."
    return sentence

def generate_sentence_5(adverse_history, previous_regulators):
    if not adverse_history and not previous_regulators: return "The firm and its key individuals have no adverse regulatory history and are not currently regulated."
    parts = ["The firm and its key individuals have **no adverse regulatory history**."]
    if adverse_history: parts[0] = f"The firm has an adverse history involving: **{adverse_history}**."
    if previous_regulators: parts.append(f"Key personnel are known to other regulators, including the **{previous_regulators}**.")
    return " ".join(parts)

def generate_sentence_6(systems_overview, outsourcing_arrangements):
    if not systems_overview: return None
    sentence = f"The applicant has documented systems for **{systems_overview}**"
    if outsourcing_arrangements: sentence += f", with key outsourced support from **{outsourcing_arrangements}**."
    else: sentence += "."
    return sentence

def generate_sentence_7(compliance_officer, mlro, screening_tools):
    if not compliance_officer and not mlro: return None
    parts = []
    if compliance_officer == mlro and compliance_officer:
        parts.append(f"has appointed **{compliance_officer}** as the combined Compliance Officer and MLRO")
    else:
        if compliance_officer: parts.append(f"has appointed **{compliance_officer}** as the Compliance Officer")
        if mlro: parts.append(f"and **{mlro}** as the MLRO")
    sentence = "The firm " + " ".join(parts)
    if screening_tools: sentence += f", and will use **{screening_tools}** for screening purposes."
    else: sentence += "."
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

# --- Pydantic Models for Input Data Validation ---

class SentenceResponse(BaseModel):
    assessment_text: Optional[str]

class Point1In(BaseModel):
    service_type: Optional[str] = None
    prudential_cat: Optional[str] = None
    legal_status: Optional[str] = None
    clients: Optional[str] = None

class Point2In(BaseModel):
    model_desc: str
    markets: Optional[str] = None
    geo_scope: Optional[str] = None
    channels: Optional[str] = None

class Point3In(BaseModel):
    structure: str
    parent_name: Optional[str] = None
    parent_jurisdiction: Optional[str] = None
    controller_name: Optional[str] = None
    controller_perc: Optional[str] = None

class Point4In(BaseModel):
    key_individuals: str
    experience_summary: Optional[str] = None

class Point5In(BaseModel):
    adverse_history: Optional[str] = None
    previous_regulators: Optional[str] = None

class Point6In(BaseModel):
    systems_overview: str
    outsourcing_arrangements: Optional[str] = None

class Point7In(BaseModel):
    compliance_officer: Optional[str] = None
    mlro: Optional[str] = None
    screening_tools: Optional[str] = None

class Point8In(BaseModel):
    capital_requirement: str
    source_of_funds: str

class Point9In(BaseModel):
    disclosures: Optional[str] = None

class Point10In(BaseModel):
    recommendation: str
    conditions: Optional[str] = None

# --- API Endpoints ---

@app.get("/", summary="API Root")
async def read_root():
    return {"message": "Welcome to the 10 Key Points Assessment API. Go to /docs for details."}

@app.post("/generate/1", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_1(data: Point1In):
    sentence = generate_sentence_1(data.service_type, data.prudential_cat, data.legal_status, data.clients)
    return {"assessment_text": sentence}

@app.post("/generate/2", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_2(data: Point2In):
    sentence = generate_sentence_2(data.model_desc, data.markets, data.geo_scope, data.channels)
    return {"assessment_text": sentence}

@app.post("/generate/3", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_3(data: Point3In):
    sentence = generate_sentence_3(data.structure, data.parent_name, data.parent_jurisdiction, data.controller_name, data.controller_perc)
    return {"assessment_text": sentence}

@app.post("/generate/4", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_4(data: Point4In):
    sentence = generate_sentence_4(data.key_individuals, data.experience_summary)
    return {"assessment_text": sentence}

@app.post("/generate/5", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_5(data: Point5In):
    sentence = generate_sentence_5(data.adverse_history, data.previous_regulators)
    return {"assessment_text": sentence}

@app.post("/generate/6", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_6(data: Point6In):
    sentence = generate_sentence_6(data.systems_overview, data.outsourcing_arrangements)
    return {"assessment_text": sentence}

@app.post("/generate/7", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_7(data: Point7In):
    sentence = generate_sentence_7(data.compliance_officer, data.mlro, data.screening_tools)
    return {"assessment_text": sentence}

@app.post("/generate/8", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_8(data: Point8In):
    sentence = generate_sentence_8(data.capital_requirement, data.source_of_funds)
    return {"assessment_text": sentence}

@app.post("/generate/9", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_9(data: Point9In):
    sentence = generate_sentence_9(data.disclosures)
    return {"assessment_text": sentence}

@app.post("/generate/10", response_model=SentenceResponse, tags=["Points Assessment"])
async def create_sentence_10(data: Point10In):
    sentence = generate_sentence_10(data.recommendation, data.conditions)
    return {"assessment_text": sentence}