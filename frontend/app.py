import streamlit as st
import requests
import os

st.set_page_config(page_title="HR Resource Chatbot", page_icon="🤖", layout="centered")

API_URL = os.environ.get("HR_CHATBOT_API", "http://localhost:8000")

st.title("🤖 HR Resource Query Chatbot")
st.caption("Ask for people by skills, experience, projects, availability.")

query = st.text_input("Enter your query", placeholder="Find Python developers with 3+ years who worked on healthcare", value="")
top_k = st.slider("Top K candidates", min_value=1, max_value=10, value=5)

col1, col2 = st.columns(2)
with col1:
    run = st.button("Search", use_container_width=True)
with col2:
    st.write("")

if run and query.strip():
    try:
        resp = requests.post(f"{API_URL}/chat", json={"query": query, "top_k": top_k}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        st.success(data.get("response", ""))
        cands = data.get("candidates", [])
        for c in cands:
            with st.container(border=True):
                st.subheader(c["name"]
                )
                st.write(f"Experience: {c['experience_years']} years | Availability: {c['availability']}")
                st.write("**Skills:** " + ", ".join(c["skills"]))
                st.write("**Projects:** " + ", ".join(c["projects"]))
    except Exception as e:
        st.error(f"Request failed: {e}")

st.divider()
st.subheader("Quick Filters (direct API)")
with st.form("filters"):
    f_skill = st.text_input("skill", placeholder="Python")
    f_project = st.text_input("project", placeholder="Healthcare Dashboard")
    f_avail = st.selectbox("availability", ["", "available", "unavailable"])
    f_min_years = st.number_input("min_years", min_value=0, value=0, step=1)
    submitted = st.form_submit_button("Filter")
    if submitted:
        try:
            params = {}
            if f_skill: params["skill"] = f_skill
            if f_project: params["project"] = f_project
            if f_avail: params["availability"] = f_avail
            if f_min_years: params["min_years"] = int(f_min_years)
            r = requests.get(f"{API_URL}/employees/search", params=params, timeout=60)
            r.raise_for_status()
            rows = r.json()
            st.write(f"Found {len(rows)} result(s)." )
            for c in rows:
                with st.container(border=True):
                    st.subheader(c["name"]
                    )
                    st.write(f"Experience: {c['experience_years']} years | Availability: {c['availability']}")
                    st.write("**Skills:** " + ", ".join(c["skills"]))
                    st.write("**Projects:** " + ", ".join(c["projects"]))
        except Exception as e:
            st.error(f"Filter request failed: {e}")
