# **📄 AI-Powered Resume Evaluator & Skill Gap Analyzer**

An advanced, full-stack application that acts as an intelligent bridge between candidates and modern recruitment standards. Leveraging **Google Gemini 2.0 Flash**, this tool performs deep semantic analysis on resumes (PDFs and images) against specific job descriptions to assess candidate compatibility, calculate a precise skill-match score, and provide highly-personalized educational pathways to bridge discovered gaps.

## **✨ Features**

* **Multi-Format Processing:** Automatically extracts and sanitizes text from text-rich .pdf documents as well as visual formats (.png, .jpg, .jpeg) using Optical Character Recognition (OCR).  
* **Deep Semantic Analysis:** Evaluates resumes based on **Technical Fit**, **Communication Skills**, **Soft Skills**, and **Work Experience Relevance** using Generative AI.  
* **Accurate Keyword Extraction:** Compares resume vocabulary with job description expectations to explicitly list matched and missing skills/keywords.  
* **Smart Skill-Gap Recommendation:** If a candidate matches below an **80% threshold**, the system dynamically builds custom search queries and generates hyperlinked recommendation cards for:  
  * **Udemy** and **Coursera** certification courses.  
  * **YouTube** video learning pathways.  
  * Optimized professional resume template layouts.  
* **Decoupled & Modern Architecture:** Clean client-server separation using a lightweight Flask REST API on the backend and an elegant Streamlit dashboard on the frontend.

## **🛠️ Tech Stack & Prerequisites**

### **Core Prerequisites**

Ensure you have the following software installed on your local machine:

* **Python 3.8+**  
* **Tesseract OCR Engine** (Required for processing image-based resumes):  
  * *Windows:* Install via [UB-Mannheim installer](https://github.com/UB-Mannheim/tesseract/wiki) and add the installation folder (usually C:\\Program Files\\Tesseract-OCR) to your system environment variables.  
  * *macOS:* Run brew install tesseract using Homebrew.  
  * *Linux:* Run sudo apt-get install tesseract-ocr and sudo apt-get install libtesseract-dev.

## **🚀 Installation & Local Setup**

### **1\. Clone the Repository**

git clone https://github.com/yourusername/ai-resume-evaluator.git  
cd ai-resume-evaluator

### **2\. Set Up a Virtual Environment (Recommended)**

\# Install virtualenv globally  
pip install virtualenv

\# Create the environment  
virtualenv .venv

\# Activate environment (Windows)  
.\\.venv\\Scripts\\activate

\# Activate environment (macOS/Linux)  
source .venv/bin/activate

### **3\. Install Python Dependencies**

pip install \-r requirements.txt

### **4\. Configure Your API Key**

Set up your Google Gemini API key as an environment variable:

\# Windows  
set GOOGLE\_API\_KEY="your-api-key-here"

\# macOS/Linux  
export GOOGLE\_API\_KEY="your-api-key-here"

## **🖥️ Running the Application**

To run the full stack, start both servers in separate terminals (ensure your .venv is activated in both).

### **Step 1: Start the Flask Backend Server**

python app.py

*This launches the server at http://127.0.0.1:5000/.*

### **Step 2: Start the Streamlit Frontend Client**

streamlit run frontend.py

*The client will automatically launch in your default web browser at http://localhost:8501/.*

## **📂 Project Directory Structure**

ai-resume-evaluator/  
├── app.py                      \# Flask API Gateway & Upload Coordinator  
├── frontend.py                 \# Streamlit UI Interface and styling  
├── evaluator.py                \# Gemini prompt structures and evaluation logic  
├── extractor.py                \# Document reading & PyTesseract OCR utility  
├── requirements.txt            \# Project dependencies  
└── README.md                   \# Project Documentation

## **🔌 API Endpoint Reference**

### **Evaluate Resume (POST /evaluate-resume)**

**Request Payload (multipart/form-data):**

* file (File): The resume file (.pdf, .png, .jpg, .jpeg).  
* job\_description (String): Text representing the targeted Job Description.

**Example Response:**

{  
  "skill\_match\_score": 85.0,  
  "matched\_keywords": \["Python", "Flask", "SQL"\],  
  "missing\_keywords": \["Docker", "AWS"\],  
  "categories": {  
    "Communication Skills": "Well-structured descriptions showing excellent professional communication.",  
    "Technical Fit": "Strong Python experience aligned directly with requirements."  
  },  
  "evaluation\_summary": "The candidate matches the technical scope of the job very well."  
}  
