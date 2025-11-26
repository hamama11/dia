import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import sympy as sp

st.set_page_config(page_title="수열의 극한 탐구", layout="wide")

st.title("📈 수열의 극한 탐구")

# -----------------------
# 1. 수열 입력
# -----------------------
st.header("1. 수열 생성하기")

user_expr = st.text_input("일반항 a(n)을 입력하세요 (예: 1/n, (-1)**n, (3*n+1)/(2*n-1))", value="1/n")

n = sp.symbols('n')
try:
    expr = sp.sympify(user_expr)
    seq = [float(expr.subs(n, i)) for i in range(1, 101)]
except:
    st.error("표현식 오류! 수학식으로 다시 입력하세요.")
    st.stop()

df = pd.DataFrame({"n": range(1,101), "a_n": seq})

st.subheader("수열 표(일부)")
st.dataframe(df.head(10))

fig = px.line(df, x="n", y="a_n", title="수열 aₙ 그래프")
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 2. 수렴/발산 분석
# -----------------------
st.header("2. 수렴 · 발산 분석")

last_vals = np.array(seq[-10:])
oscillation = np.std(last_vals)

if oscillation < 0.001:
    st.success(f"수렴할 가능성이 높습니다. (근사 극한값 ≈ {np.mean(last_vals):.4f})")
elif np.mean(np.abs(last_vals)) > 1e5:
    st.warning("값이 매우 커지고 있습니다 → 발산 가능성 큼")
else:
    st.info("진동하거나 불규칙합니다 → 극한이 없을 가능성 있음")

# -----------------------
# 3. 유사한 수열 a' 만들기
# -----------------------
st.header("3. a' 수열 생성 (유사성 실험)")

method = st.selectbox("a' 생성 방식", ["k배 하기", "c 더하기", "비율 고정"])

k = st.number_input("k 값", value=2.0)
c = st.number_input("c 값", value=1.0)

if method == "k배 하기":
    seq2 = k * np.array(seq)
elif method == "c 더하기":
    seq2 = np.array(seq) + c
else:
    seq2 = k * np.array(seq)  # 비율 고정은 k배와 동일

df2 = pd.DataFrame({"n": range(1,101), "a_n'": seq2})

col1, col2 = st.columns(2)
with col1:
    st.write("aₙ")
    st.line_chart(df.set_index("n"))
with col2:
    st.write("aₙ'")
    st.line_chart(df2.set_index("n"))

st.markdown("### 💡 **a와 a'의 극한 관계를 비교해보세요!**")

# -----------------------
# 4. ab vs a’b 실험
# -----------------------
st.header("4. ab vs a'b 비교 실험 (연산의 안정성)")

user_expr_b = st.text_input("b(n)을 입력하세요 (예: (-1)**n, n, sqrt(n))", value="n")

try:
    expr_b = sp.sympify(user_expr_b)
    seq_b = np.array([float(expr_b.subs(n, i)) for i in range(1,101)])
except:
    st.error("b(n) 수식 오류!")
    st.stop()

ab = np.array(seq) * seq_b
a_b = np.array(seq2) * seq_b

df_ab = pd.DataFrame({"n": range(1,101), "ab": ab, "a'b": a_b})

st.line_chart(df_ab.set_index("n"))

st.markdown("""
### 💡 질문
- a와 a'이 유사해도 b가 발산하면 ab와 a'b는 어떤 차이를 보이는가?  
- ab가 수렴할 때, b가 발산하더라도 a’b가 수렴할 수 있는가?  
""")
