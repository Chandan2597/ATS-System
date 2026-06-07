# TalentMatch Review

A simple Streamlit application for reviewing resumes against a job description using an ATS-aware AI assistant.

## Prerequisites

- Python 3.10 or newer
- `pip`
- A valid `GROQ_API_KEY`

## Setup

1. Open a terminal in the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following content:
   ```text
   GROQ_API_KEY=your_api_key_here
   ```

## Run the application

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Usage

1. Paste the job description into the text area.
2. Upload your resume as a PDF file.
3. Choose either:
   - `Review Resume Fit` for alignment feedback
   - `Calculate Match Score` for ATS match scoring

## Notes

- The app uses `PyPDF2` to extract text from uploaded PDF resumes.
- The AI request is sent via the `groq` client using the `compound-beta-mini` model.
