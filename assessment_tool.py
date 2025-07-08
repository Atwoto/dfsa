import streamlit as st

# --- Logic Functions for Sentence Generation ---

def generate_sentence_1(service_type, prudential_cat, legal_status, clients):
    if not any([service_type, prudential_cat, legal_status, clients]):
        return "_Please provide input for at least one field._"
    parts = []
    if service_type: parts.append(f"provide **{service_type}** services")
    else: parts.append("provide financial services")
    if prudential_cat: parts.append(f"under a **{prudential_cat}** Prudential classification")
    if legal_status: parts.append(f"as a **{legal_status}**")
    if clients: parts.append(f"targeting **{clients}** clients")
    return "The firm is seeking authorization to " + ", ".join(parts) + "."

def generate_sentence_2(model_desc, markets, geo_scope, channels):
    if not model_desc: return "_The 'Business Model Description' is required._"
    parts = [f"a **{model_desc}**"]
    if markets: parts.append(f"focused on **{markets}**")
    if geo_scope: parts.append(f"across **{geo_scope}**")
    if channels: parts.append(f"delivered via **{channels}**")
    return "The applicant describes its business model as " + ", ".join(parts) + "."

def generate_sentence_3(structure, parent_name, parent_jurisdiction, controller_name, controller_perc):
    if not structure: return "_The 'Ownership Structure' is required._"
    parts = [f"The firm is **{structure}**"]
    if parent_name and parent_jurisdiction: parts.append(f", **{parent_name}**, incorporated in **{parent_jurisdiction}**")
    elif parent_name: parts.append(f", **{parent_name}**")
    if controller_name and controller_perc: parts.append(f"with ultimate control resting with **{controller_name}** holding **{controller_perc}** equity")
    elif controller_name: parts.append(f"with ultimate control resting with **{controller_name}**")
    return " ".join(parts) + "."

def generate_sentence_4(key_individuals, experience_summary):
    if not key_individuals: return "_'Key Individuals' field is required._"
    sentence = f"The business will be run by **{key_individuals}**"
    if experience_summary: sentence += f", who has **{experience_summary}**."
    else: sentence += "."
    return sentence

def generate_sentence_5(adverse_history, previous_regulators):
    if not adverse_history and not previous_regulators:
        return "The firm and its key individuals have no adverse regulatory history and are not currently regulated."
    
    parts = ["The firm and its key individuals have **no adverse regulatory history**."]
    if adverse_history:
        parts[0] = f"The firm has an adverse history involving: **{adverse_history}**."

    if previous_regulators:
        parts.append(f"Key personnel are known to other regulators, including the **{previous_regulators}**.")
    
    return " ".join(parts)

def generate_sentence_6(systems_overview, outsourcing_arrangements):
    if not systems_overview: return "_'Systems Overview' field is required._"
    sentence = f"The applicant has documented systems for **{systems_overview}**"
    if outsourcing_arrangements: sentence += f", with key outsourced support from **{outsourcing_arrangements}**."
    else: sentence += "."
    return sentence

def generate_sentence_7(compliance_officer, mlro, screening_tools):
    if not compliance_officer and not mlro: return "_At least a CO or MLRO must be specified._"
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
    if not capital_requirement or not source_of_funds: return "_Capital Requirement and Source of Funds are required._"
    return f"The firm will meet the **{capital_requirement}** capital requirement through **{source_of_funds}**."

def generate_sentence_9(disclosures):
    if not disclosures: return "No other material matters or disclosures were noted."
    return f"The firm disclosed the following: **{disclosures}**."

def generate_sentence_10(recommendation, conditions):
    if not recommendation: return "_A 'Recommendation' is required._"
    sentence = f"Recommendation: **{recommendation}**."
    if conditions: sentence += f" This is subject to the following conditions: **{conditions}**."
    return sentence

# --- Streamlit User Interface ---
st.set_page_config(layout="wide")
st.title("Automated 10 Key Points Assessment Tool")

# --- The Main Form ---
with st.form("assessment_form"):
    
    col1, col2 = st.columns(2)

    with col1:
        st.header("1. Financial Services, Legal Status, etc.")
        p1_service_type = st.text_input("Primary Financial Service Type", "Advisory and Arranging", key="p1_service")
        p1_prudential_cat = st.text_input("Prudential Category", "Category 3C", key="p1_prudential")
        p1_legal_status = st.text_input("Legal Status", "Private Company Limited by Shares", key="p1_legal")
        p1_clients = st.text_input("Proposed Client Types", "Retail and Professional", key="p1_clients")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_1(p1_service_type, p1_prudential_cat, p1_legal_status, p1_clients)}")
        st.divider()

        st.header("2. Business Overview")
        p2_model_desc = st.text_area("Business Model Description", "A regional wealth management firm", key="p2_desc")
        p2_markets = st.text_input("Target Markets", "HNW clients", key="p2_markets")
        p2_geo_scope = st.text_input("Geographic Scope", "the GCC", key="p2_geo")
        p2_channels = st.text_input("Delivery Channels", "face-to-face meetings", key="p2_channels")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_2(p2_model_desc, p2_markets, p2_geo_scope, p2_channels)}")
        st.divider()

        st.header("3. Who Controls")
        p3_structure = st.text_input("Ownership Structure", "wholly owned by a holding company", key="p3_structure")
        p3_parent_name = st.text_input("Parent Company Name (if any)", "XYZ Holdings Ltd.", key="p3_parent")
        p3_parent_jurisdiction = st.text_input("Jurisdiction of Parent", "the Cayman Islands", key="p3_jurisdiction")
        p3_controller_name = st.text_input("Primary Controller Name", "a single individual shareholder", key="p3_controller")
        p3_controller_perc = st.text_input("Primary Controller Percentage", "100%", key="p3_perc")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_3(p3_structure, p3_parent_name, p3_parent_jurisdiction, p3_controller_name, p3_controller_perc)}")
        st.divider()

        st.header("4. Who will run the business?")
        p4_key_individuals = st.text_input("Key Individuals (e.g., Mr. John Doe (CEO))", "Mr. John Doe (CEO)", key="p4_ind")
        p4_experience = st.text_input("Experience Summary", "20+ years of experience in regulated financial services", key="p4_exp")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_4(p4_key_individuals, p4_experience)}")
        st.divider()

        st.header("5. Background checks/other regulators")
        p5_adverse_history = st.text_input("Adverse History (leave blank if none)", key="p5_adv")
        p5_previous_reg = st.text_input("Previous Regulators (e.g., FCA (UK))", "FCA (UK)", key="p5_reg")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_5(p5_adverse_history, p5_previous_reg)}")
        st.divider()

    with col2:
        st.header("6. Systems and Controls")
        p6_systems = st.text_input("Systems Overview (e.g., onboarding, transaction monitoring)", "client onboarding, transaction monitoring, and internal audit", key="p6_sys")
        p6_outsourcing = st.text_input("Outsourcing Arrangements (leave blank if none)", "regulated vendor in the UAE", key="p6_out")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_6(p6_systems, p6_outsourcing)}")
        st.divider()

        st.header("7. Compliance/Financial Crime Arrangements")
        p7_co = st.text_input("Compliance Officer Name", "Mr. Smith", key="p7_co")
        p7_mlro = st.text_input("MLRO Name (can be same as CO)", "Mr. Smith", key="p7_mlro")
        p7_tools = st.text_input("Screening Tools Used", "WorldCheck", key="p7_tools")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_7(p7_co, p7_mlro, p7_tools)}")
        st.divider()
        
        st.header("8. Capital requirements and sources of wealth/funds")
        p8_capital = st.text_input("Capital Requirement", "$500,000", key="p8_cap")
        p8_sof = st.text_input("Source of Funds", "shareholder injection backed by audited statements", key="p8_sof")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_8(p8_capital, p8_sof)}")
        st.divider()

        st.header("9. Any other disclosures/considerations")
        p9_disclosures = st.text_area("Disclosures (leave blank if none)", "Ongoing civil litigation involving a minority shareholder.", key="p9_disc")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_9(p9_disclosures)}")
        st.divider()
        
        st.header("10. Recommendation/IP conditions")
        p10_rec = st.text_input("Recommendation", "Approval with standard conditions", key="p10_rec")
        p10_cond = st.text_input("Conditions (leave blank if none)", "Satisfactory review of the IT infrastructure audit.", key="p10_cond")
        st.subheader("Generated Output:")
        st.markdown(f"> {generate_sentence_10(p10_rec, p10_cond)}")
        st.divider()

    st.form_submit_button("Update Report", disabled=True) # Button is not needed for live demo