import streamlit as st
import pandas as pd
import random
import time
from datetime import date

if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'current_task' not in st.session_state:
    st.session_state.current_task = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'completed_count' not in st.session_state:
    st.session_state.completed_count = 0
if 'last_date' not in st.session_state:
    st.session_state.last_date = str(date.today())

if st.session_state.last_date != str(date.today()):
    st.session_state.completed_count = 0
    st.session_state.last_date = str(date.today())

st.title("The Antivenom for Decision Paralysis 🗄️")

st.metric("🕵🏾‍♀️ Mission's completed today", st.session_state.completed_count)

with st.expander("🤔💭📋 What do you plan on doing today, babe?"):

    current_text = "\n".join(st.session_state.tasks)
    input_text = st.text_area("📝 Jot down your tasks:", value=current_text, height=200)
    
    if st.button("🔄 Save/Update List"):
        st.session_state.tasks = [t.strip() for t in input_text.split('\n') if t.strip()]
        st.toast(f"🔐 To-do list updated! {len(st.session_state.tasks)} tasks ready 🌟")
        time.sleep(1)
        st.rerun()


if st.button("🧞 Choose My Fate") and st.session_state.tasks:
    st.session_state.current_task = random.choice(st.session_state.tasks)
    st.session_state.end_time = time.time() + (25 * 60)
    st.rerun()

if st.session_state.current_task and st.session_state.end_time:
    st.markdown("---")
    st.subheader("👁️‍🗨️ Amor Fati, my dear. \n 📂 The 25-minute missin you've been assigned is:")
    st.header(f"🎲 {st.session_state.current_task} 🎲")

    remaining = st.session_state.end_time - time.time()
        
    if remaining > 0:
        mins, secs = divmod(int(remaining), 60)
        st.metric("⏲️ Time left", f"{mins:02d}:{secs:02d}")
        if st.button("🔂 Refresh Timer"):
            st.rerun()
    else:
        st.error("🏁 Did you finish? (pause)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎉 Task Complete"):
            st.session_state.completed_count += 1
            st.session_state.tasks.remove(st.session_state.current_task)
            st.session_state.current_task = None
            st.session_state.end_time = None
            st.balloons()
            time.sleep(2)
            st.rerun()

    with col2:
        if st.button("🆘 Shit I got sidetracked!"):
            st.session_state.current_task = None
            st.session_state.end_time = None
            st.rerun()
elif not st.session_state.tasks:
    st.info("📨 Add some tasks above to get started!")