import streamlit as st
import pandas as pd
import requests

# ✅ Set Streamlit page config
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

# ✅ URL of your deployed FastAPI backend on Render
API_URL = "https://shl-fastapi.onrender.com/recommend"

# ✅ UI Header
st.title("🧠 SHL Assessment Recommender")
st.markdown("Enter a job description or relevant keyword to get assessment recommendations:")

# ✅ Input box
user_input = st.text_area("📄 Job description or keyword:", height=200)

# ✅ Button click
if st.button("🔍 Recommend Assessments"):
    if not user_input.strip():
        st.warning("Please enter something to search.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                # ✅ Send POST request to FastAPI backend
                response = requests.post(
                    API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "accept": "application/json"
                    },
                    json={"query": user_input}
                )

                # ✅ Handle successful response
                if response.status_code == 200:
                    data = response.json()

                    # ✅ Correct response key from FastAPI
                    recommendations = data.get("recommended_assessments", [])

                    if recommendations:
                        st.success(f"✅ Found {len(recommendations)} assessment(s)")
                        st.dataframe(pd.DataFrame(recommendations))
                    else:
                        st.warning("❌ No recommendations found. Try rephrasing the job description or using clearer keywords.")

                else:
                    st.error(f"🚨 Server error: {response.status_code}")
                    try:
                        st.json(response.json())
                    except:
                        st.write(response.text)

            except Exception as e:
                st.error("❌ Something went wrong while connecting to the backend.")
                st.exception(e)
