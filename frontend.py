import streamlit as st
import requests
import base64


st.set_page_config(page_title="Resume Evaluator", layout="centered")


st.image("ai-resume-landing.png", use_container_width=True)


st.title("📄 Resume Evaluator using Gemini AI")
st.markdown("Upload a Resume (PDF or Image) and provide the Job Description to get an evaluation.")


with st.form("resume_form"):
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "png", "jpg", "jpeg"])
    job_description = st.text_area("Enter Job Description", height=200)
    submitted = st.form_submit_button("Evaluate Resume")


if submitted and uploaded_file and job_description:
    with st.spinner("Evaluating..."):
        files = {"file": (uploaded_file.name, uploaded_file)}
        data = {"job_description": job_description}

        try:
            response = requests.post("http://localhost:5000/evaluate-resume", files=files, data=data)
            response.raise_for_status()
            result = response.json()

            st.success("✅ Evaluation Completed")


            st.markdown("### 📄 Uploaded Resume Preview:")

            file_ext = uploaded_file.name.split('.')[-1].lower()

            if file_ext == "pdf":

                uploaded_file.seek(0)
                base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            elif file_ext in ["png", "jpg", "jpeg"]:

                uploaded_file.seek(0)
                st.image(uploaded_file, use_container_width=True)


            st.markdown(f"### ✅ Skill Match Score: {result.get('skill_match_score', 0)}%")


            st.markdown("### ✔️ Matched Keywords")
            st.write(", ".join(result.get("matched_keywords", [])) or "None")


            st.markdown("### ❌ Missing Keywords")
            st.write(", ".join(result.get("missing_keywords", [])) or "None")


            st.markdown("### 🧠 Custom Evaluation")
            for category, summary in result.get("categories", {}).items():
                st.markdown(f"{category}: {summary}")


            st.markdown("### 🤖 Gemini AI Summary")
            summary = result.get("evaluation_summary", "No summary returned")

            custom_box = f"""
            <div style="background-color: #e6f4f1; padding: 20px; border-radius: 10px;
                         border-left: 6px solid #2c8cff; height: 300px; overflow-y: auto;
                         color: #1c1c1c; font-size: 16px; line-height: 1.5;">
                {summary}
            </div>
            """
            st.markdown(custom_box, unsafe_allow_html=True)

            # Improvement Suggestions (if applicable)
            if "improvement_resources" in result:
                st.markdown("### 🚀 Improvement Suggestions (Skill Match < 80%)")

                st.markdown("#### 📚 Certification Courses")
                for course in result["improvement_resources"].get("certification_courses", []):
                    course_title = course.get("title", "Untitled Course")
                    course_desc = course.get("description", "No description available.")
                    course_link = course.get("link", "#")

                    course_box = f"""
                    <div style="background-color: #e6f4f1; padding: 15px; border-radius: 10px;
                                 border-left: 5px solid #2c8cff; margin-bottom: 15px;
                                 color: #1c1c1c; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin-bottom: 5px; font-size: 18px;">{course_title}</h4>
                        <p style="margin: 8px 0; font-size: 15px;">{course_desc}</p>
                        <a href="{course_link}" target="_blank" style="color: #0077cc; text-decoration: none; font-weight: bold;">
                            🔗 Visit Course
                        </a>
                    </div>
                    """
                    st.markdown(course_box, unsafe_allow_html=True)

                st.markdown("#### ▶️ YouTube Video Suggestions")

                yt = result["improvement_resources"].get("youtube_link")
                if yt:
                    yt_box = f"""
                    <div style="background-color: #e6f4f1; padding: 15px; border-radius: 10px;
                                 border-left: 5px solid #ff0000; margin-bottom: 15px;
                                 color: #1c1c1c; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin-bottom: 5px; font-size: 18px;">Improve your skills with YouTube</h4>
                        <p style="margin: 8px 0; font-size: 15px;">Curated videos to boost your knowledge.</p>
                        <a href="{yt}" target="_blank" style="color: #e62117; text-decoration: none; font-weight: bold;">
                            ▶️ Watch on YouTube
                        </a>
                    </div>
                    """
                    st.markdown(yt_box, unsafe_allow_html=True)

                st.markdown("#### 📄 Resume Templates")

                for example_link in result["improvement_resources"].get("resume_examples", []):
                    resume_box = f"""
                    <div style="background-color: #e6f4f1; padding: 15px; border-radius: 10px;
                                 border-left: 5px solid #6a1b9a; margin-bottom: 15px;
                                 color: #1c1c1c; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin-bottom: 5px; font-size: 18px;">Professional Resume Template</h4>
                        <p style="margin: 8px 0; font-size: 15px;">Use this resume layout to improve your presentation.</p>
                        <a href="{example_link}" target="_blank" style="color: #6a1b9a; text-decoration: none; font-weight: bold;">
                            📄 View Template
                        </a>
                    </div>
                    """
                    st.markdown(resume_box, unsafe_allow_html=True)


        except requests.exceptions.RequestException as e:
            st.error(f"Error contacting backend: {e}")
else:
    st.markdown("👉 Please upload a resume and enter a job description to begin.")