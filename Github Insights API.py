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
    pulls_button = st.button("Show Pulls")


if repo_button:
    url = f"http://127.0.0.1:8000/{owner}/{repo}/overview"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        st.subheader(f"⭐ Number of Stars: {data["stars"]}")
        st.subheader(f"👀 Number of Watchers: {data["watchers"]}")
        st.subheader(f"🗒️ Main Language: {data["main_language"]}")
        st.subheader(f"🍴 Number of Forks: {data["forks"]}")
    else:
        st.error("Failed to fetch data 😢")

if contr_button:
    url = f"http://127.0.0.1:8000/{owner}/{repo}/contributors"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        df = pd.DataFrame(list(data.items()), columns=["Contributors", "Number of commits"])
        st.subheader("Contributors and their number of Commits")
        st.bar_chart(df, x='Contributors', y='Number of commits', x_label='Number of commits', y_label='Contributors', horizontal=True)
    else:
        st.error("Failed to fetch data 😢")

if lang_button:
    url = f"http://127.0.0.1:8000/{owner}/{repo}/languages"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        df = pd.DataFrame(list(data.items()), columns=["Language", "Count"])
        st.subheader("Most used Languages")
        st.bar_chart(df, x='Language', y='Count', x_label='Languages used', y_label='Number of bytes of code')
    else:
        st.error("Failed to fetch data 😢")


def transform_pull_data(data: dict):
    df = pd.DataFrame(data, columns=["Pull", "Created", "Closed"])
    df["Created"] = pd.to_datetime(df["Created"], utc=True)
    df["Closed"] = pd.to_datetime(df["Closed"], utc=True)

    events = []
    for _, row in df.iterrows():
        events.append((row["Created"], +1, row["Pull"]))
        if pd.notnull(row["Closed"]):
            events.append((row["Closed"], -1, row["Pull"]))

    events_df = pd.DataFrame(events, columns=["Timestamp", "Change", "Pull"])

    events_df = events_df.sort_values("Timestamp").reset_index(drop=True)

    events_df["Currently open"] = events_df["Change"].cumsum()

    df["Duration"] = df["Closed"] - df["Created"]
    avg_close_time = df["Duration"].dropna().mean()

    currently_open_final = events_df["Currently open"].iloc[-1]
    
    return events_df,  avg_close_time, currently_open_final

if pulls_button:
    # Call your FastAPI backend
    url = f"http://127.0.0.1:8000/{owner}/{repo}/pulls"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Data loaded!")
        data, avg_close_time, curr_open = transform_pull_data(data)
        st.subheader("Open Pulls Timeline")
        st.line_chart(data=data, x='Timestamp', y='Currently open', x_label='Time', y_label='Open Pulls', color=None, width=None, height=None, use_container_width=True)
        st.text(f'Average time to close a Pull: {avg_close_time}')
        st.text(f'Currently open pulls: {curr_open}')
    else:
        st.error("Failed to fetch data 😢")