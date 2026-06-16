import os
import json
from typing import List
from pydantic import BaseModel, Field
import streamlit as str_ui
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load local environment variables
load_dotenv()

# Ensure API key is configured
if not os.getenv("GEMINI_API_KEY"):
    str_ui.error("Missing GEMINI_API_KEY environment variable. Please check your .env file.")

# Initialize the official Google GenAI client
client = genai.Client()

# =====================================================================
# DATA SCHEMA (Designed for Scalability)
# =====================================================================
class TestScenario(BaseModel):
    id: str = Field(description="Unique identifier, e.g., TS_001")
    title: str = Field(description="Short descriptive name of the test scenario")
    type: str = Field(description="Scenario classification: Positive, Negative, Edge Case, Security, SQL Injection, or Network Latency")
    preconditions: List[str] = Field(description="Setup actions or criteria needed before executing steps")
    steps: List[str] = Field(description="Sequential execution instructions for the test")
    expected_result: str = Field(description="The mandatory validation checkpoint or outcome")

class TestSuite(BaseModel):
    extracted_acceptance_criteria: List[str] = Field(description="Structured acceptance criteria parsed out from the requirement description")
    scenarios: List[TestScenario] = Field(description="Complete suite of calculated test cases across functional and technical bounds")

# =====================================================================
# CORE AGENT ENGINE
# =====================================================================
def run_qa_agent(user_story_input: str) -> TestSuite:
    """
    Processes the raw user story using an expert QA persona and
    forces structured output validation.
    """
    system_instruction = (
        "You are an expert Senior Staff SDET and specialized QA Automation Agent.\n"
        "Your goal is to parse a raw User Story and generate clean Acceptance Criteria "
        "alongside an exhaustive, professional test suite.\n\n"
        "You must analyze the input across these specific testing boundaries:\n"
        "1. Positive Scenarios (Happy path validations)\n"
        "2. Negative Scenarios (Error handling, invalid inputs, flow breaking)\n"
        "3. Edge Cases (Boundary conditions, data limits)\n"
        "4. Security Scenarios (Access control, role permissions)\n"
        "5. SQL Injection (Payload safety injections, data sanity checks)\n"
        "6. Network Latency (Timeouts, degraded network speeds, race conditions)\n\n"
        "Ensure all steps and expected results are technical, clear, and actionable."
    )

    # Invoke Gemini utilizing the fast, high-performance flash model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Analyze the following requirements and produce the test suite:\n\n{user_story_input}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            # Force the model to return data structured exactly to the Pydantic classes
            response_mime_type="application/json",
            response_schema=TestSuite,
            temperature=0.1,  # Low temperature forces predictable, logical behavior
        ),
    )
    
    # Safely convert the JSON string back into a Pydantic object
    return TestSuite.model_validate_json(response.text)

# =====================================================================
# STREAMLIT USER INTERFACE
# =====================================================================
str_ui.set_page_config(page_title="AI QA Agent Engine", layout="wide")

str_ui.title("🧠 AI Quality Engineering Agent Studio")
str_ui.caption("Generate functional and security test matrices directly from raw User Stories using Gemini 2.5")

# Sidebar detailing capabilities
with str_ui.sidebar:
    str_ui.header("Agent Capabilities")
    str_ui.markdown("""
    - [x] Extracted Acceptance Criteria
    - [x] Functional (Positive / Negative)
    - [x] Edge Case Verification
    - [x] AppSec (SQL Injection checks)
    - [x] Infrastructure (Network Latency mitigation)
    """)
    str_ui.divider()
    str_ui.info("Next Modular Phase: Automated Test Code Translation (Playwright/Pytest)")

# Main user input area
user_story_box = str_ui.text_area(
    "Paste your User Story and any rough design notes below:",
    height=200,
    placeholder="Example:\nAs a user, I want to login to my dashboard using an email and password..."
)

if str_ui.button("Execute QA Analysis Agent", type="primary"):
    if not user_story_box.strip():
        str_ui.warning("Please provide a user story prompt before execution.")
    else:
        with str_ui.spinner("Agent running deep analysis across business and system vectors..."):
            try:
                # Call our core generation engine
                results = run_qa_agent(user_story_box)
                
                # Display parsed Acceptance Criteria
                str_ui.subheader("📋 Extracted Acceptance Criteria")
                for ac in results.extracted_acceptance_criteria:
                    str_ui.markdown(f"- {ac}")
                
                str_ui.divider()
                
                # Display calculated Test Scenarios grouped neatly in a grid layout
                str_ui.subheader("⚡ Generated Test Matrix")
                
                for scenario in results.scenarios:
                    # Dynamically color code tags depending on classification type
                    type_colors = {
                        "Positive": "blue", "Negative": "orange", "Edge Case": "violet",
                        "Security": "red", "SQL Injection": "red", "Network Latency": "gray"
                    }
                    badge_color = type_colors.get(scenario.type, "blue")
                    
                    with str_ui.expander(f"**[{scenario.id}]** {scenario.title}"):
                        str_ui.markdown(f":{badge_color}[**Classification Type:** {scenario.type}]")
                        
                        str_ui.markdown("**Preconditions:**")
                        for pre in scenario.preconditions:
                            str_ui.markdown(f"  - {pre}")
                            
                        str_ui.markdown("**Execution Steps:**")
                        for idx, step in enumerate(scenario.steps, 1):
                            str_ui.markdown(f"  {idx}. {step}")
                            
                        str_ui.markdown(f"**Expected Result:**\n`{scenario.expected_result}`")
                
                # Export option to verify data output can be fed downstream
                str_ui.divider()
                json_string = json.dumps(results.model_dump(), indent=2)
                str_ui.download_button(
                    label="Download Test Suite Dataset (JSON)",
                    file_name="ai_generated_test_suite.json",
                    mime="application/json",
                    data=json_string
                )
                
            except Exception as error:
                str_ui.error(f"An error occurred during runtime operation: {error}")