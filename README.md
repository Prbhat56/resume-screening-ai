# 🤖 AI Resume Screening Agent

An intelligent AI-powered resume screening system that automatically analyzes and ranks candidates based on job requirements using Google's Gemini AI.

![Demo](https://img.shields.io/badge/Status-Functional-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)

## 🎯 What It Does

The AI Resume Screening Agent automates the initial resume screening process by:
- **Analyzing** resumes (PDF/DOCX) against job descriptions
- **Scoring** candidates based on skills, experience, education, and relevance
- **Ranking** applicants from best to worst fit
- **Providing** detailed insights and improvement suggestions

## ✨ Key Features

- 📄 **Multi-format Support**: PDF and DOCX resume parsing
- 🤖 **AI-Powered Analysis**: Google Gemini AI for intelligent scoring
- 📊 **Visual Dashboard**: Interactive charts and rankings
- ⚡ **Real-time Processing**: Instant analysis and results
- 🎯 **Detailed Insights**: Strengths, concerns, and missing skills
- 📱 **Responsive Design**: Works on desktop and mobile

## 🛠️ Tools & APIs Used

### **Frontend & Framework**
- **Streamlit** - Web application framework
- **Plotly** - Interactive data visualization

### **AI & Processing**
- **Google Gemini API** - AI analysis and scoring
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing

### **Utilities**
- **python-dotenv** - Environment configuration
- **JSON** - Data serialization

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.8+
- Google Gemini API key ([Get free key](https://makersuite.google.com/app/apikey))

### **Quick Start**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/resume-screening-agent.git
cd resume-screening-agent