
import streamlit as st
import openai
import os
from fpdf import FPDF
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual key for testing

st.set_page_config(page_title="Startup 2-Pager Generator", layout="centered")
st.title("🚀 Startup 2-Pager Generator")

company = st.text_input("Enter Company Name")
industry = st.text_input("Enter Industry")
region = st.text_input("Enter Region")

if st.button("Generate 2-Pager Report"):
    if not company or not industry or not region:
        st.warning("Please enter Company, Industry, and Region.")
    else:
        with st.spinner("Generating Report..."):
            prompt = f"""
            You are a professional investment analyst. Create a clear, concise, and structured 2-page report on the startup '{company}' in the '{industry}' industry, operating in '{region}'.

            Structure the report as follows:
            1. Business Overview
            2. Key Products and Business Model
            3. Key Financial Metrics (if available)
            4. Key Operating Metrics (if available)
            5. Fundraising History
            6. Industry Outlook – Headwinds & Tailwinds
            7. Private Credit Use Case – applicability, risks, collateral

            Write in a professional tone. Use bullet points where helpful.
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a professional startup analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1800
                )

                report = response["choices"][0]["message"]["content"]
                st.success("2-Pager Report Generated!")
                st.text_area("Generated Report", report, height=500)

                # Export as PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in report.split('\n'):
                    pdf.multi_cell(0, 10, line)

                filename = f"{company} - Intro.pdf"
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    pdf.output(tmp_file.name)
                    tmp_file.flush()
                    with open(tmp_file.name, "rb") as f:
                        st.download_button(
                            label="📄 Download PDF",
                            data=f,
                            file_name=filename,
                            mime="application/pdf"
                        )

            except Exception as e:
                st.error(f"Error: {e}")
