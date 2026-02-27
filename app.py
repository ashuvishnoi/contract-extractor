# import uvicorn
# from fastapi import FastAPI, UploadFile, File
# from contract_extractor.core.extractor import extract
#
# app = FastAPI()
#
# @app.post("/extract")
# async def extract_endpoint(file: UploadFile = File(...), query: str = "", output_type: str = "string"):
#     pdf_bytes = await file.read()
#     result = extract(pdf_bytes, query, output_type)
#     return result
#
#
# pdf = "/Users/ashutosh/Documents/project/CUAD-project/CUAD_v1/full_contract_pdf/Part_I/Affiliate_Agreements/CybergyHoldingsInc_20140520_10-Q_EX-10.27_8605784_EX-10.27_Affiliate Agreement.pdf"
# query = "What is Agreement Date of this contract?"
# output_type = "date"
# response = extract(pdf, query, output_type)
# print(response)
#
# # run the API
# # uvicorn.run(app, host="localhost", port=8090)



import streamlit as st
from contract_extractor.core.extractor import extract
import tempfile

st.set_page_config(page_title="Contract Extractor", layout="wide")

st.title("📄 Contract Extractor (RAG + LLM)")

# Upload PDF
uploaded_file = st.file_uploader("Upload Contract PDF", type=["pdf"])

# Query input
query = st.text_input(
    "Enter your question",
    placeholder="e.g., What is Agreement Date of this contract?"
)

# Output type selector
output_type = st.selectbox(
    "Select Output Type",
    ["string", "date", "number"]
)

if st.button("Extract"):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        result = extract(tmp_path, query, output_type)

        st.success("Extraction Complete")
        st.subheader("Result:")
        st.write(result)
