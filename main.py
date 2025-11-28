# main.py
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Evolving Logic", layout="wide")

# 상단 제목
st.title("✨ EVOLVING LOGIC – 반례로 논리를 완성한다")

# 안내 문구 
st.markdown(
    """
    <div style="padding:12px; 
                background-color:#f5f5f5; 
                border-left:4px solid #475569; 
                margin-top:10px; 
                margin-bottom:20px;
                font-size:1rem;">
        <strong>※ 안내</strong><br>
        화면 왼편 상단의 <strong>“>>” 표시</strong>를 누르면  
        이어지는 활동 목록으로 건너갈 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 이 파일(main.py)와 같은 위치의 main.html 읽기
html_path = Path(__file__).resolve().parent / "main.html"
html_code = html_path.read_text(encoding="utf-8")

# Streamlit 안에서 애니메이션 렌더링
components.html(
    html_code,
    height=900,
    scrolling=False
)
