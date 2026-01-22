import streamlit as st
import random
import time
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/17kHRwSpoPXgoWE2_DwVJteEUA5kYmAMowPBD1ir6sNQ/edit" 

st.set_page_config(page_title="Decision Paralysis Antivenom", page_icon="🐍")

def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(spreadsheet=SPREADSHEET_URL, ttl=0, worksheet="Sheet1")
        
        if df.empty:
            return None
        
        row = df.iloc[-1] 
        
        tasks_str = str(row.get("tasks", ""))
        tasks_list = [t.strip() for t in tasks_str.split("|||") if t.strip() and t != "nan"]
        
        return {
            "tasks": tasks_list,
            "completed_count": int(row.get("completed_count", 0)),
            "last_date": str(row.get("last_date", str(date.today()))),
            "current_task": str(row.get("current_task", "")) if str(row.get("current_task", "")) != "nan" and row.get("current_task", "") else None,
            "end_time": float(row.get("end_time", 0.0)) if row.get("end_time", 0.0) > 0 else None
        }
    except Exception as e:
        return None

def save_data(state_dict):
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.spinner("💾 Saving to Cloud... Don't lock your screen!"):
        tasks_str = "|||".join(state_dict["tasks"])
        
        new_df = pd.DataFrame([{
            "tasks": tasks_str,
            "completed_count": state_dict["completed_count"],
            "last_date": state_dict["last_date"],
            "current_task": state_dict["current_task"] if state_dict["current_task"] else "",
            "end_time": state_dict["end_time"] if state_dict["end_time"] else 0.0
        }])
        
        conn.update(spreadsheet=SPREADSHEET_URL, data=new_df, worksheet="Sheet1")
        st.toast("🪂 Cloud Sync Complete!")

if 'initialized' not in st.session_state:
    cloud_data = get_data()
    if cloud_data:
        st.session_state.tasks = cloud_data["tasks"]
        st.session_state.completed_count = cloud_data["completed_count"]
        st.session_state.last_date = cloud_data["last_date"]
        st.session_state.current_task = cloud_data["current_task"]
        st.session_state.end_time = cloud_data["end_time"]
    else:
        st.session_state.tasks = []
        st.session_state.completed_count = 0
        st.session_state.last_date = str(date.today())
        st.session_state.current_task = None
        st.session_state.end_time = None
    st.session_state.initialized = True

if st.session_state.last_date != str(date.today()):
    st.session_state.completed_count = 0
    st.session_state.last_date = str(date.today())

def sync_to_cloud():
    current_state = {
        "tasks": st.session_state.tasks,
        "completed_count": st.session_state.completed_count,
        "last_date": st.session_state.last_date,
        "current_task": st.session_state.current_task,
        "end_time": st.session_state.end_time
    }
    save_data(current_state)

st.title("The Antivenom for Decision Paralysis 🗄️ v3.0 (Cloud)")
st.metric("🕵🏾‍♀️ Mission's completed today", st.session_state.completed_count)

with st.expander("🤔💭📋 What do you plan on doing today, babe?"):
    current_text = "\n".join(st.session_state.tasks)
    input_text = st.text_area("📝 Jot down your tasks here:", value=current_text, height=200)
    if st.button("🔄 Save/Update"):
        st.session_state.tasks = [t.strip() for t in input_text.split('\n') if t.strip()]
        sync_to_cloud()
        st.toast("☁️ Synced to the cloud!")
        time.sleep(5)
        st.rerun()

if st.session_state.current_task is None and st.session_state.tasks:
    if st.button("🧞 Choose My Fate"):
        st.session_state.current_task = random.choice(st.session_state.tasks)
        st.session_state.end_time = time.time() + (25 * 60)
        sync_to_cloud()
        st.rerun()

if st.session_state.current_task and st.session_state.end_time:
    st.markdown("---")
    st.subheader("👁️‍🗨️ Amor Fati, my dear.\n📂 The 25-minute mission you've been assigned is:")
    st.header(f"🎲 {st.session_state.current_task} 🎲")
    
    remaining = st.session_state.end_time - time.time()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎉 Task Complete"):
            st.session_state.completed_count += 1
            if st.session_state.current_task in st.session_state.tasks:
                st.session_state.tasks.remove(st.session_state.current_task)
            st.session_state.current_task = None
            st.session_state.end_time = None
            sync_to_cloud()
            st.balloons()
            time.sleep(1)
            st.rerun()
    with col2:
        if st.button("🆘 Shit I got sidetracked!"):
            st.session_state.current_task = None
            st.session_state.end_time = None
            sync_to_cloud()
            st.rerun()

    timer_placeholder = st.empty()
    if remaining > 0:
        mins, secs = divmod(int(remaining), 60)
        timer_placeholder.metric("⏲️ Time left", f"{mins:02d}:{secs:02d}")
        time.sleep(1)
        st.rerun()
    else:
        timer_placeholder.error("🏁 Did you finish (pause)?")

elif not st.session_state.tasks:
    st.info("📨 Add some tasks above to get started!")