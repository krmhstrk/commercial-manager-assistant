# prompts.py

def get_contract_analysis_prompt(contract_text, contract_type):
    """
    Creates a detailed, role-specific prompt for AI contract analysis,
    focusing on telecom industry risks as per the research report.
    """
    return f"""
    You are a meticulous AI Legal Assistant specializing in telecommunications contracts for a Commercial Manager.
    Your task is to analyze the following '{contract_type}' and provide a structured risk and key terms report.

    Contract Text:
    ---
    {contract_text}
    ---

    Based on your expertise in telecom agreements, perform the following analysis and provide the output in a valid JSON format only.

    1.  **Risk Analysis**: Identify and score critical risk factors. Focus specifically on:
        - **Service Level Agreements (SLAs)**: Are the performance guarantees and penalty structures clear and reasonable?
        - **Liability Caps & Indemnification**: Is the limitation of damages clear? Are the indemnification clauses balanced?
        - **Intellectual Property (IP) Rights**: How is the ownership and licensing of software and technology handled?
        - **Data Protection & Privacy**: Does it comply with relevant regulations (e.g., GDPR)?
        - **Termination Provisions**: Are the notice periods and termination fees clearly defined and fair?
        - **Exclusivity Clauses**: Are there any geographic or product-based exclusivity terms?

    2.  **Key Commercial Terms Extraction**: Extract the following specific terms from the contract text. If a term is not present, indicate "Not Found".
        - **Renewal Term**: e.g., "Auto-renews for 1 year"
        - **Notice Period for Non-Renewal**: e.g., "90 days"
        - **Payment Terms**: e.g., "Net 30"
        - **Governing Law & Jurisdiction**: e.g., "State of New York, USA"

    Structure your JSON response with these exact keys: "risk_analysis", "key_terms".
    For "risk_analysis", each item should have "clause_category", "risk_level" (Low, Medium, High), and "summary".
    For "key_terms", use the term name as the key.
    """

def get_tco_pricing_prompt(segment, tco_components, historical_data_summary):
    """
    Creates a comprehensive prompt for AI-driven TCO and pricing strategy recommendations,
    incorporating business context as per the research report.
    """
    return f"""
    You are a Strategic Commercial Advisor to a "Commercial Manager Assistant" tool.
    Your goal is to provide a pricing and TCO strategy for a software-based mobile network solution targeting the '{segment}' customer segment.

    **Input Data:**
    - **TCO Components Provided**: {tco_components}
    - **Summary of Historical Deals for this Segment**: {historical_data_summary}

    **Your Task:**
    Based on the provided data, generate a strategic recommendation in a valid JSON format.

    1.  **TCO Analysis Insight**: Provide a brief, one-sentence insight based on the provided TCO components. What is the likely key cost driver?
    2.  **Recommended Commercial Model**: Based on the customer segment and TCO structure, recommend one primary commercial model from these options: "Tiered-Feature Subscription", "Usage-Based Pricing", or "Hybrid Model". Provide a brief justification.
    3.  **Suggested Pricing Strategy**: Propose a starting price point or structure for the recommended model.
    4.  **Key Value Propositions**: List three key value propositions to emphasize during negotiation that justify the price and align with the customer's likely priorities.

    Structure your JSON response with these exact keys: "tco_insight", "recommended_model", "pricing_strategy", "value_propositions".
    """

# Placeholders for future enhancements
def get_partner_insight_prompt():
    """Placeholder prompt for partner performance analysis."""
    return "Analyze the provided partner performance data and provide strategic recommendations."

def get_rfx_risk_prompt():
    """Placeholder prompt for RFx risk assessment."""
    return "Analyze the provided RFx requirements and identify key commercial, technical, and legal risks."