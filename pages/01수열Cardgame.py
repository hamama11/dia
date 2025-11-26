import streamlit as st
import streamlit.components.v1 as components

st.title("🧩 Limit Trinity - 수열 매칭 게임")
st.caption("Github Pages에 배포된 게임을 그대로 Streamlit 안에서 실행합니다.")

components.iframe(
    src="https://hamama11.github.io/boostcamp/limit.html",
    width=1200,
    height=2200,
    scrolling=True
)
