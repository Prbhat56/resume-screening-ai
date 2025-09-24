# AI Resume Screening Agent - Architecture

```mermaid
graph TD
    A[User Interface<br>Streamlit Web App] --> B[File Upload<br>PDF/DOCX]
    B --> C[Text Extraction<br>PyPDF2/python-docx]
    C --> D[AI Analysis<br>Google Gemini API]
    D --> E[Scoring Engine<br>JSON Processing]
    E --> F[Results Dashboard<br>Plotly Charts]
    F --> G[Candidate Ranking<br>Visualization]
    
    H[Job Description<br>User Input] --> D
    I[Google Gemini API<br>AI Model] --> D
    J[Environment Variables<br>.env config] --> D
    
    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style F fill:#e8f5e8