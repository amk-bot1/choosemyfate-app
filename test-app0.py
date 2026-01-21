import streamlit as st
import pandas as pd
import random
import time

st.title("Anti-Venom for Decision Paralysis 🗄️")

task_input = st.text_area("Enter your tasks (one per line):", "Read book\nCall grandma\nClean room")
task_list = [t.strip() for t in task_input.split('\n') if t.strip()]


if st.button("🧞 Choose My Fate"):
    if task_list:
        chosen_task = random.choice(task_list)
        st.subheader(f"Amor Fati, my dear. The 25-minute mission you've been assigned is:")
        st.header(f"🎲 {chosen_task} 🎲")
        
        ph = st.empty()
        for i in range(25 * 60, 0, -1):
            mins, secs = divmod(i, 60)
            ph.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        st.balloons()
    else:
        st.warning("Add some tasks first!")