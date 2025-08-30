import streamlit as st
import requests
import pandas as pd

st.title("📊 GitHub Insights Dashboard")

# User inputs
owner = st.text_input("Repository owner", "octocat")
repo = st.text_input("Repository name", "hello-world")

col1, col2, col3, col4 = st.columns(4)

with col1:
    repo_button = st.button("Repo Overview")

with col2:
    contr_button = st.button("Show Contributors")

with col3:
    lang_button = st.button("Show Languages")

with col4:
    issues_button = st.button("Show Pulls")


if repo_button:
    # Call your FastAPI backend
    url = f"http://127.0.0.1:8000/{owner}/{repo}/languages"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        df = pd.DataFrame(list(data.items()), columns=["Language", "Count"])
        st.bar_chart(df, x='Language', y='Count', x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
    else:
        st.error("Failed to fetch data 😢")

if contr_button:
    # Call your FastAPI backend
    url = f"http://127.0.0.1:8000/{owner}/{repo}/languages"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        df = pd.DataFrame(list(data.items()), columns=["Language", "Count"])
        st.bar_chart(df, x='Language', y='Count', x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
    else:
        st.error("Failed to fetch data 😢")

if lang_button:
    # Call your FastAPI backend
    url = f"http://127.0.0.1:8000/{owner}/{repo}/languages"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        df = pd.DataFrame(list(data.items()), columns=["Language", "Count"])
        st.bar_chart(df, x='Language', y='Count', x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
    else:
        st.error("Failed to fetch data 😢")

if issues_button:
    # Call your FastAPI backend
    url = f"http://127.0.0.1:8000/{owner}/{repo}/languages"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        df = pd.DataFrame(list(data.items()), columns=["Language", "Count"])
        st.bar_chart(df, x='Language', y='Count', x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
    else:
        st.error("Failed to fetch data 😢")