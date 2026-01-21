import streamlit as st
import random
import time
import json
import os
from datetime import date

DATA_FILE = "tasks_data.json"

def save_to_disk():
    data = {
        "tasks": st.session_state.tasks,
        "completed_count": st.session_state.completed_count,
        "last_date": st.session_state.last_date
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_from_disk():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return None

if 'tasks' not in st.session_state:
    saved_data = load_from_disk()
    if saved_data:
        st.session_state.tasks = saved_data.get("tasks", [])
        st.session_state.completed_count = saved_data.get("completed_count", 0)
        st.session_state.last_date = saved_data.get("last_date", str(date.today()))
    else:
        st.session_state.tasks = []
        st.session_state.completed_count = 0
        st.session_state.last_date = str(date.today())

if 'current_task' not in st.session_state:
    st.session_state.current_task = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

if st.session_state.last_date != str(date.today()):
    st.session_state.completed_count = 0
    st.session_state.last_date = str(date.today())
    save_to_disk()

st.title("The Antivenom for Decision Paralysis 🗄️ v2")
st.metric("🕵🏾‍♀️ Mission's completed today", st.session_state.completed_count)

with st.expander("🤔💭📋 What do you plan on doing today, babe?"):
    current_text = "\n".join(st.session_state.tasks)
    input_text = st.text_area("📝 Jot down your tasks:", value=current_text, height=200)
    if st.button("🔄 Save/Update List"):
        st.session_state.tasks = [t.strip() for t in input_text.split('\n') if t.strip()]
        save_to_disk()
        st.toast("💽 Saved to long-term memory!")
        st.rerun()

if st.button("🧞 Choose My Fate") and st.session_state.tasks:
    st.session_state.current_task = random.choice(st.session_state.tasks)
    st.session_state.end_time = time.time() + (25 * 60)
    st.rerun()

if st.session_state.current_task and st.session_state.end_time:
    st.markdown("---")
    st.subheader("👁️‍🗨️ Amor Fati, my dear. \n 📂 The 25-minute mission you've been assigned is:")
    st.header(f"🎲 {st.session_state.current_task} 🎲")
    
    timer_display = st.empty()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎉 Task Complete"):
            st.session_state.completed_count += 1
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
            st.rerun()

    while st.session_state.current_task is not None:
        remaining = st.session_state.end_time - time.time()
        if remaining <= 0:
            timer_display.error("🏁 Did you finish? (pause)")
            break
        mins, secs = divmod(int(remaining), 60)
        timer_display.metric("⏲️ Time left", f"{mins:02d}:{secs:02d}")
        time.sleep(1)

elif not st.session_state.tasks:
    st.info("📨 Add some tasks above to get started!")