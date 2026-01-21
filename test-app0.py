import streamlit as st
import random
import time
import json
import os
from datetime import date, datetime

DATA_FILE = "tasks_data.json"

def save_to_disk():
    data = {
        "tasks": st.session_state.tasks,
        "completed_count": st.session_state.completed_count,
        "last_date": st.session_state.last_date,
        "current_task": st.session_state.current_task,
        "end_time": st.session_state.end_time
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        st.error(f"Could not save data: {e}")

def load_from_disk():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None

if 'initialized' not in st.session_state:
    saved_data = load_from_disk()
    if saved_data:
        st.session_state.tasks = saved_data.get("tasks", [])
        st.session_state.completed_count = saved_data.get("completed_count", 0)
        st.session_state.last_date = saved_data.get("last_date", str(date.today()))
        st.session_state.current_task = saved_data.get("current_task", None)
        st.session_state.end_time = saved_data.get("end_time", None)
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
    save_to_disk()

st.title("The Antivenom for Decision Paralysis 🗄️ v2.1")
st.metric("🕵🏾‍♀️ Missions completed today", st.session_state.completed_count)

with st.expander("🤔💭📋 What do you plan on doing today, babe?"):
    current_text = "\n".join(st.session_state.tasks)
    input_text = st.text_area("📝 Jot down your tasks:", value=current_text, height=200)
    if st.button("🔄 Save/Update List"):
        st.session_state.tasks = [t.strip() for t in input_text.split('\n') if t.strip()]
        save_to_disk()
        st.toast("💽 Saved to long-term memory!")
        time.sleep(1)
        st.rerun()

if st.session_state.current_task is None and st.session_state.tasks:
    if st.button("🧞 Choose My Fate"):
        st.session_state.current_task = random.choice(st.session_state.tasks)
        st.session_state.end_time = time.time() + (25 * 60) 
        save_to_disk()
        st.rerun()

if st.session_state.current_task and st.session_state.end_time:
    st.markdown("---")
    st.subheader("👁️‍🗨️ Amor Fati, my dear. \n 📂 The 25-minute mission you've been assigned is:")
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
            save_to_disk()
            st.balloons()
            time.sleep(1)
            st.rerun()
    with col2:
        if st.button("🆘 Shit I got sidetracked!"):
            st.session_state.current_task = None
            st.session_state.end_time = None
            save_to_disk()
            st.rerun()

    timer_placeholder = st.empty()
    
    if remaining > 0:
        mins, secs = divmod(int(remaining), 60)
        timer_placeholder.metric("⏲️ Time left", f"{mins:02d}:{secs:02d}")
        time.sleep(1) 
        st.rerun()
    else:
        timer_placeholder.error("🏁 Time is up! Did you finish?")

elif not st.session_state.tasks:
    st.info("📨 Add some tasks above to get started!")