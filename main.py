# main.py
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Evolving Logic", layout="wide")

st.title("✨ EVOLVING LOGIC – 반례가 논리를 완성한다")

# 이 파일(main.py)와 같은 위치의 main.html 읽기
html_path = Path(__file__).resolve().parent / "main.html"
html_code = html_path.read_text(encoding="utf-8")

# Streamlit 안에 그대로 삽입
components.html(
    html_code,
    height=900,      # 애니메이션 세로 크기, 필요하면 조절
    scrolling=False  # 내부 스크롤 필요하면 True로
)
