import streamlit as st
import pandas as pd
import random
import time

if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'current_task' not in st.session_state:
    st.session_state.current_task = None

st.title("The Antivenom for Decision Paralysis 🗄️")

with st.expander("🤔💭📋 What do you plan on doing today, babe?"):

    current_text = "\n".join(st.session_state.tasks)
    input_text = st.text_area("📝 Jot down your tasks (enter for new line):", value=current_text, height=200)
    
    if st.button("🔄 Save/Update List"):
        st.session_state.tasks = [t.strip() for t in input_text.split('\n') if t.strip()]
        st.success(f"🔒 To-do list updated! {len(st.session_state.tasks)} tasks ready 🌟")


if st.button("🧞 Choose My Fate") and st.session_state.tasks:
    st.session_state.current_task = random.choice(st.session_state.tasks)

if st.session_state.current_task:
    st.markdown("---")
    st.subheader("👁️‍🗨️ Amor Fati, my dear. \n 📂 The 25-minute missin you've been assigned is:")
    st.header(f"🎲 {st.session_state.current_task} 🎲")
    
    timer_placeholder = st.empty()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎉 Task Complete"):
            st.session_state.tasks.remove(st.session_state.current_task)
            st.session_state.current_task = None
            st.success("Mission Accomplished 🤝 🥂")
            st.balloons()
            time.sleep(2)
            st.rerun()

    with col2:
        if st.button("🆘 Shit I got sidetracked!"):
            st.session_state.current_task = None
            st.warning("Exfiltrating... The task has been HALO dropped back into the list 🪂")
            time.sleep(2)
            st.rerun()

    for i in range(25 * 60, 0, -1):
        mins, secs = divmod(i, 60)
        timer_placeholder.metric("⏲️ Time left", f"{mins:02d}:{secs:02d}")
        time.sleep(1)
    
    st.error("Did you finish 🏁? (pause) ")

elif not st.session_state.tasks:
    st.info("📨 Add some tasks above to get started!")