import os
import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title="Resume + Cover Letter Generator", page_icon="📝", layout="wide")

st.title("📝 AI Resume + Cover Letter Generator")

st.markdown(
    """
    Fill the details below and get a **professional Resume & Cover Letter** instantly.  
    🚀 Powered by **Groq AI (LLaMA-3)**  
    """
)

# Sidebar instructions + API key input
with st.sidebar:
    st.header("📌 Instructions")
    st.write("1. Enter your details\n2. Add your Groq API Key\n3. Click **Generate**\n4. View Resume + Cover Letter\n5. Download if needed")
    
    # API key input
    GROQ_API_KEY = st.text_input("🔑 Enter your Groq API Key", type="password")

    st.write("---")
    st.write("👩‍💻 Developed by Bushra")

# Input form
with st.form("resume_form"):
    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email Address")
    phone = st.text_input("📱 Phone Number")
    skills = st.text_area("🛠️ Skills (comma-separated)")
    experience = st.text_area("💼 Work Experience")
    education = st.text_area("🎓 Education (Degrees, Institutes)")
    certifications = st.text_area("🏆 Certifications & Achievements")
    job_role = st.text_input("🎯 Target Job Role")
    languages = st.text_area("🌐 Languages Known (comma-separated)")

    submitted = st.form_submit_button("🚀 Generate Resume & Cover Letter")

if submitted:
    if not GROQ_API_KEY:
        st.error("❌ Please enter your Groq API Key in the sidebar to continue.")
    else:
        with st.spinner("⏳ Generating... Please wait..."):

            # Initialize Groq LLM with user-provided API key
            llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

            # Prompts
            resume_prompt = f"""
            Generate a highly professional and well-structured resume for {name}.
            Name: {name}
            Email: {email}
            Phone: {phone}

            Include the following sections:
            ▪️ Summary
            ▪️ Work Experience: {experience}
            ▪️ Skills: {skills}
            ▪️ Education: {education}
            ▪️ Certifications: {certifications}
            ▪️ Languages: {languages}

            ➡️ Use bullet points where needed.
            ➡️ Avoid extra spaces and keep formatting clean.
            """

            cover_letter_prompt = f"""
            Generate a professional and structured cover letter for {name}, applying for the role of {job_role}.
            Name: {name}
            Email: {email}
            Phone: {phone}

            Cover Letter Format:
            ▪️ Date
            ▪️ Greeting (Dear Hiring Manager,)
            ▪️ Introduction paragraph (who you are + purpose of letter)
            ▪️ Body paragraph (highlight Education: {education}, Experience: {experience}, Skills: {skills})
            ▪️ Closing paragraph (show enthusiasm + availability)
            ▪️ Formal closing (Sincerely, {name})

            ➡️ Keep it formal, concise, and professional.
            ➡️ Avoid unnecessary blank lines/spaces.
            """

            resume_output = llm.invoke(resume_prompt).content.strip()
            cover_letter_output = llm.invoke(cover_letter_prompt).content.strip()

        # ---------------- UI ENHANCEMENT ---------------- #
        st.success("✅ Resume & Cover Letter Generated Successfully!")

        col1, col2 = st.columns(2)

        # Resume Box
        with col1:
            st.subheader("📄 Generated Resume")
            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:12px;
                    background-color:white;
                    color:#222;
                    box-shadow:0px 2px 8px rgba(0,0,0,0.15);
                    max-height:500px;
                    overflow-y:auto;
                    font-family:Arial, sans-serif;
                    line-height:1.6;
                ">
                <h2 style="color:#2E86C1; margin-bottom:5px;">📌 Resume</h2>
                <h3 style="color:#000; margin:0;">{name}</h3>
                <p style="margin:2px 0;"><b>Email:</b> {email} | <b>Phone:</b> {phone}</p>
                <hr style="margin:5px 0;">
                <div style="white-space:normal; font-size:15px;">{resume_output}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Resume Download Button
            st.download_button(
                label="⬇️ Download Resume",
                data=resume_output,
                file_name=f"{name}_Resume.txt",
                mime="text/plain"
            )

        # Cover Letter Box
        with col2:
            st.subheader("💌 Generated Cover Letter")
            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:12px;
                    background-color:white;
                    color:#222;
                    box-shadow:0px 2px 8px rgba(0,0,0,0.15);
                    max-height:500px;
                    overflow-y:auto;
                    font-family:Arial, sans-serif;
                    line-height:1.6;
                ">
                <h2 style="color:#2E86C1; margin-bottom:5px;">📌 Cover Letter</h2>
                <hr style="margin:5px 0;">
                <div style="white-space:normal; font-size:15px;">
                    {cover_letter_output.replace(cover_letter_output.splitlines()[-1], f"<b>{cover_letter_output.splitlines()[-1]}</b>")}
                </div>   
                </div>
                """,
                unsafe_allow_html=True
            )
            # Cover Letter Download Button
            st.download_button(
                label="⬇️ Download Cover Letter",
                data=cover_letter_output,
                file_name=f"{name}_CoverLetter.txt",
                mime="text/plain"
            )
