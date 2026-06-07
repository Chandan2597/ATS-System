from dotenv import load_dotenv
import streamlit as st
import os
import PyPDF2
from groq import Client
from groq import APIStatusError

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Please add it to your .env file or environment.")

client = Client(api_key=api_key)


def get_groq_response(prompt_text, resume_text, prompt):
    model = "compound-beta-mini"
    messages = [
        {"role": "system", "content": "You are an expert ATS resume reviewer."},
        {"role": "user", "content": prompt_text},
        {"role": "user", "content": f"Resume text: {resume_text}"},
        {"role": "user", "content": prompt},
    ]
    try:
        response = client.chat.completions.create(messages=messages, model=model)
        if response.choices:
            return response.choices[0].message.content
        return str(response)
    except APIStatusError as api_err:
        status = api_err.response.status_code if api_err.response is not None else "unknown"
        body = api_err.response.text if api_err.response is not None else str(api_err)
        return f"Groq API error {status}: {body}"
    except Exception as err:
        return f"Groq request failed: {type(err).__name__}: {err}"

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        uploaded_file.seek(0)
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if not text:
            raise ValueError("Unable to extract text from the uploaded PDF.")

        return text
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="TalentMatch Review", page_icon="📄", layout="centered")

st.markdown(
    "<div style='text-align:center; margin-bottom: 1rem;'>"
    "<h1 style='color:#1f4e78; margin: 0;'>TalentMatch Review</h1>"
    "<p style='color:#4a4a4a; font-size:18px; margin: 0.5rem 0 0;'>Analyze your resume against a job description with ATS-aware feedback.</p>"
    "</div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("About TalentMatch")
    st.write(
        "Upload your resume as a PDF, paste the target job description, and choose how you want the ATS review delivered."
    )
    st.markdown("---")
    st.write("- Resume review alignment")
    st.write("- ATS match percentage")
    st.write("- Strengths, weaknesses, and next steps")

input_text = st.text_area("Job description", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully.")

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("Review Resume Fit")
with col2:
    submit3 = st.button("Calculate Match Score")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description.
Give me the percentage match if the resume matches the job description.
First the output should be the percentage, then keywords missing, and finally overall recommendations.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_groq_response(input_prompt1, pdf_content, input_text)
        st.subheader("Review Output")
        st.write(response)
    else:
        st.warning("Please upload your resume before running the review.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_groq_response(input_prompt3, pdf_content, input_text)
        st.subheader("Match Score Output")
        st.write(response)
    else:
        st.warning("Please upload your resume before calculating match score.")




