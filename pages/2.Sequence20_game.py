# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("🎮 수열 스무고개 : 조건으로 추론하라")

st.caption(
    "출제자는 수열의 정체를 감추어 두고, "
    "배움의 이들은 표와 그래프, 그리고 예/아니오로 답할 수 있는 질문들만으로 "
    "그 수열의 수렴·발산과 숨은 구조를 밝혀내는 놀이이옵니다."
)

st.markdown(
    """
### 🎲 이 활동은 무엇을 겨냥한 놀이인가

- 이 수업은 **스무고개의 형식**을 빌려,  
  수열의 극한과 구조를 **직접 묻고 따져 보는 탐구형 보드게임**과도 같사옵니다.
- 출제자는 하나의 수열을 정하여 **일부 항의 표와 그래프만** 드러내고,  
  나머지 정보는 감추어 둡니다.
- 학생들은 다음과 같은 두 갈래의 질문을 던질 수 있사옵니다.
  1. 이 수열 자체의 성질에 관한 질문  
     - 수렴 여부, 유계성, 단조성, 부호 변화 등
  2. **규칙을 더하거나, 다른 수열과 연산한 뒤**의 모습에 관한 질문  
     - 예: 짝수 번째 항만 모은 부분수열은 어떠한가?  
       \|aₙ\|은 수렴하는가? n·aₙ은 수렴하는가?  
       1/n과 항별 곱을 하면 수렴성이 달라지는가? 등
- 곧이곧대로 공식을 계산하기보다,  
  **“어떤 조건을 바꾸면 극한의 운명이 어떻게 달라지는지”**를 살피는 것이  
  이 놀이의 핵심이라 할 수 있사옵니다.
"""
)

# -----------------------------
# 0. 숨겨진 수열 데이터 준비
# -----------------------------
SEQUENCES = [
    {
        "name": "1/n",
        "expr": r"a_n = 1/n",
        "preview_n": 40,
        "seq": lambda n: 1 / n,
        "convergent": True,
        "limit_value": 0.0,
        "bounded": True,
        "monotone": True,         # n>=1에서 단조 감소
        "sign_changes": False,
        "n_times_conv": True,     # n*a_n = 1 → 수렴
        "abs_conv": True,         # |a_n| = 1/n → 0으로 수렴
        "piecewise2": False,
        "even_subseq_conv": True,     # a_{2n} = 1/(2n) → 0
        "odd_subseq_conv": True,      # a_{2n-1} = 1/(2n-1) → 0
        "with_1_over_n_conv": True,   # a_n * (1/n) = 1/n^2 → 0
        "explain": "a_n = 1/n 은 단조 감소하며 유계인 수열로, 0으로 수렴하옵니다."
    },
    {
        "name": "(-1)^n",
        "expr": r"a_n = (-1)^n",
        "preview_n": 20,
        "seq": lambda n: (-1) ** n,
        "convergent": False,
        "limit_value": None,
        "bounded": True,
        "monotone": False,
        "sign_changes": True,
        "n_times_conv": False,        # n*a_n = ±n → 발산
        "abs_conv": False,            # |a_n| = 1 → 상수이나 '극한 구조' 비교용으로 비수렴 처리
        "piecewise2": True,
        "even_subseq_conv": True,     # a_{2n} = 1
        "odd_subseq_conv": True,      # a_{2n-1} = -1
        "with_1_over_n_conv": True,   # (-1)^n / n → 0
        "explain": "a_n = (-1)^n 은 두 값 사이를 오르내리며 진동하므로, 한 점으로 모이지는 않사옵니다."
    },
    {
        "name": "n",
        "expr": r"a_n = n",
        "preview_n": 20,
        "seq": lambda n: n,
        "convergent": False,
        "limit_value": None,
        "bounded": False,
        "monotone": True,
        "sign_changes": False,
        "n_times_conv": False,        # n^2 → 발산
        "abs_conv": False,
        "piecewise2": False,
        "even_subseq_conv": False,    # 2n → 발산
        "odd_subseq_conv": False,     # 2n-1 → 발산
        "with_1_over_n_conv": True,   # n * (1/n) = 1 → 수렴
        "explain": "a_n = n 은 끝없이 자라나 위로 유계가 아니므로, 극한이 존재하지 않사옵니다."
    },
    {
        "name": "(-1)^n / n",
        "expr": r"a_n = (-1)^n / n",
        "preview_n": 60,
        "seq": lambda n: (-1) ** n / n,
        "convergent": True,
        "limit_value": 0.0,
        "bounded": True,
        "monotone": False,
        "sign_changes": True,
        "n_times_conv": False,        # (-1)^n → 진동
        "abs_conv": True,             # |a_n| = 1/n → 0
        "piecewise2": True,
        "even_subseq_conv": True,     # 1/(2n) → 0
        "odd_subseq_conv": True,      # -1/(2n-1) → 0
        "with_1_over_n_conv": True,   # (-1)^n / n^2 → 0
        "explain": "a_n = (-1)^n / n 은 부호는 번갈아 바뀌되, 크기가 줄어들어 마침내 0으로 모이옵니다."
    },
    {
        "name": "ln(n)",
        "expr": r"a_n = \\ln n",
        "preview_n": 40,
        "seq": lambda n: np.log(n),
        "convergent": False,
        "limit_value": None,
        "bounded": False,
        "monotone": True,
        "sign_changes": False,
        "n_times_conv": False,        # n ln n → 발산
        "abs_conv": False,
        "piecewise2": False,
        "even_subseq_conv": False,    # ln(2n) → ∞
        "odd_subseq_conv": False,     # ln(2n-1) → ∞
        "with_1_over_n_conv": True,   # (ln n)/n → 0
        "explain": "a_n = \\ln n 은 더디게 오르나, 끝내 멈추지 않고 발산하옵니다."
    },
    {
        "name": "sin(n)",
        "expr": r"a_n = \\sin n",
        "preview_n": 60,
        "seq": lambda n: np.sin(n),
        "convergent": False,
        "limit_value": None,
        "bounded": True,
        "monotone": False,
        "sign_changes": True,
        "n_times_conv": False,        # n sin n → 일반적으로 발산
        "abs_conv": False,
        "piecewise2": False,
        "even_subseq_conv": False,    # sin(2n) 진동
        "odd_subseq_conv": False,     # sin(2n-1) 진동
        "with_1_over_n_conv": True,   # sin n / n → 0
        "explain": "a_n = \\sin n 은 -1과 1 사이를 복잡히 오가며, 한 점으로 모이지 않사옵니다."
    },
]

# -----------------------------
# 질문 목록 정의
# -----------------------------
QUESTIONS = [
    # 기본 성질 질문
    ("convergent", "이 수열은 **수렴**하느냐, 아니하느냐?"),
    ("bounded", "이 수열은 위·아래로 **유계**라 할 수 있겠는가?"),
    ("monotone", "어느 시점부터 **단조로이** 한 방향으로만 나아가는가?"),
    ("sign_changes", "항의 **부호가 무한히 자주 뒤바뀌는가?**"),
    ("abs_conv", r"절댓값 수열 **|a_n|** 은 수렴하느냐?"),
    ("piecewise2", "짝수·홀수 등 **둘로 갈라 다른 식으로 정의**되는 수열이더냐?"),

    # 규칙 변경·연산에 관한 확장 질문
    ("n_times_conv", r"이 수열에 **n을 곱한 수열 n·a_n** 은 수렴하느냐?"),
    ("even_subseq_conv", "짝수 항만 모은 부분수열 (a₂, a₄, …) 은 수렴하느냐?"),
    ("odd_subseq_conv", "홀수 항만 모은 부분수열 (a₁, a₃, …) 은 수렴하느냐?"),
    ("with_1_over_n_conv", r"이 수열을 **1/n과 항별 곱한 수열 a_n·(1/n)** 은 수렴하느냐?")
]

MAX_QUESTIONS = 8  # 한 라운드 최대 질문 수

# -----------------------------
# 1. 세션 상태 초기화
# -----------------------------
if "seq_idx" not in st.session_state:
    st.session_state.seq_idx = None
if "asked" not in st.session_state:
    st.session_state.asked = {}
if "q_count" not in st.session_state:
    st.session_state.q_count = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# -----------------------------
# 2. 새 라운드 시작 버튼
# -----------------------------
col_new, col_info = st.columns([1, 3])
with col_new:
    if st.button("🔄 새 라운드 다시 여는가"):
        st.session_state.seq_idx = int(np.random.randint(0, len(SEQUENCES)))
        st.session_state.asked = {}
        st.session_state.q_count = 0
        st.session_state.show_answer = False

with col_info:
    if st.session_state.seq_idx is None:
        st.info("👉 먼저 **'새 라운드 다시 여는가'** 버튼을 눌러, 한 수열을 뽑아 보시옵소서.")
    else:
        st.success("이제 질문을 골라 던지며, 감추어진 수열의 속내를 밝혀 보시옵소서.")

if st.session_state.seq_idx is None:
    st.stop()

seq_data = SEQUENCES[st.session_state.seq_idx]

# -----------------------------
# 3. 표 & 그래프 (초기 정보)
# -----------------------------
st.markdown("## 1️⃣ 드러나 있는 단서 : 앞부분 표와 그래프")

N_PREVIEW = seq_data["preview_n"]
n_values = np.arange(1, N_PREVIEW + 1)
a_values = np.array([seq_data["seq"](k) for k in n_values], dtype=float)

df = pd.DataFrame({"n": n_values, "a_n": a_values})

col_table, col_plot = st.columns(2)
with col_table:
    st.subheader("표 (일부 항)")
    st.dataframe(df.head(10), use_container_width=True)
    st.caption("※ 출제자는 뒤에 어떤 일이 기다리는지 알지만, 질문자는 이 앞부분만 보고 추론하여야 하옵니다.")

with col_plot:
    st.subheader("그래프")
    fig = px.line(df, x="n", y="a_n", markers=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# 4. 질문 라운드
# -----------------------------
st.markdown("## 2️⃣ 예 / 아니오로만 묻는 질문들")

st.write(
    f"- 이 라운드에서 허락된 질문의 총 수는 **{MAX_QUESTIONS}회**이옵니다."
)
st.write(
    f"- 지금까지 쓰신 질문 수 : **{st.session_state.q_count}회**"
)

remaining_q = [q for q in QUESTIONS if q[0] not in st.session_state.asked]

if st.session_state.q_count >= MAX_QUESTIONS:
    st.warning("더 이상 질문은 허락되지 않사옵니다. 이제까지의 단서로 판단을 내리시옵소서.")
else:
    if not remaining_q:
        st.info("더 물어볼 만한 새 질문은 남지 않았사옵니다.")
    else:
        q_key, q_label = st.selectbox(
            "묻고자 하는 질문 하나를 고르시옵소서. (아직 하지 않은 질문만 나열되옵니다.)",
            remaining_q,
            format_func=lambda x: x[1]
        )

        if st.button("❓ 이 질문을 던지겠는가"):
            ans = seq_data[q_key]  # True / False / None
            st.session_state.asked[q_key] = ans
            st.session_state.q_count += 1

# 이미 물어본 질문과 답 요약
if st.session_state.asked:
    st.markdown("### 💬 지금까지 드러난 예/아니오의 기록")
    for key, ans in st.session_state.asked.items():
        label = dict(QUESTIONS)[key]
        if ans is True:
            txt = "YES (그러하옵니다.)"
        elif ans is False:
            txt = "NO (그렇지 않사옵니다.)"
        else:
            txt = "판단 불가 (미리 정해 두지 아니하였음)"
        st.write(f"- **{label}** ➜ **{txt}**")

st.markdown("---")

# -----------------------------
# 5. 수렴/발산 추론 구역
# -----------------------------
st.markdown("## 3️⃣ 이제 그대의 판단을 밝힐 차례")

col_judge1, col_judge2 = st.columns(2)
with col_judge1:
    verdict = st.radio(
        "이 수열의 운명은 어떠하다고 보시는가?",
        ["수렴한다", "발산한다", "아직 판단을 미루겠다"],
        index=2
    )
with col_judge2:
    guess_limit = st.text_input(
        "수렴한다고 본다면, 그 극한값은 무엇이라 여기시는가? (모르겠다면 비워 두어도 좋사옵니다.)",
        value=""
    )

reason = st.text_area(
    "어찌하여 그러한 결론에 이르렀는지, 그 근거를 적어 보시옵소서.",
    placeholder="예: 표를 보니 점점 줄어드는 듯하고, 유계·단조라는 답을 얻었으므로 0으로 수렴한다고 판단하였음 등"
)

st.markdown("---")

# -----------------------------
# 6. 정답 공개
# -----------------------------
if st.button("📢 이제 정답을 드러낼 것인가"):
    st.session_state.show_answer = True

if st.session_state.show_answer:
    st.markdown("## ✅ 정답과 해설")

    st.write(f"**숨겨져 있던 수열의 이름:** `{seq_data['name']}`")
    st.latex(seq_data["expr"])

    if seq_data["convergent"]:
        st.write(f"- 이 수열은 **수렴**하옵니다. 극한값은 **{seq_data['limit_value']}** 이옵니다.")
    else:
        st.write("- 이 수열은 한 점으로 모이지 아니하고, **수렴하지 않사옵니다.**")

    st.write("- 유계 여부 :", "✅ 유계라 할 수 있사옵니다." if seq_data["bounded"] else "❌ 위로든 아래로든 한계를 두지 아니하옵니다.")
    st.write("- 단조성 :", "✅ 어느 시점부터 한 방향으로만 나아가옵니다." if seq_data["monotone"] else "❌ 오르내림이 섞여 단조롭지 않사옵니다.")
    st.write("- 부호 변화 :", "✅ 부호가 무한히 자주 바뀌옵니다." if seq_data["sign_changes"] else "❌ 부호 변화가 없거나 제한적이옵니다.")
    st.write("- n·a_n 의 수렴성 :", "✅ n·a_n 역시 수렴하옵니다." if seq_data["n_times_conv"] else "❌ n·a_n 은 수렴하지 않거나, 이 맥락에서 의미 있게 다루기 어렵사옵니다.")
    st.write("- |a_n| 의 수렴성 :", "✅ 절댓값 수열은 수렴하옵니다." if seq_data["abs_conv"] else "❌ 절댓값 수열 또한 수렴하지 않사옵니다.")
    st.write("- 짝수 항 부분수열 :", "✅ (a₂, a₄, …) 은 수렴하옵니다." if seq_data["even_subseq_conv"] else "❌ 짝수 항들만 보아도 수렴하지 않사옵니다.")
    st.write("- 홀수 항 부분수열 :", "✅ (a₁, a₃, …) 역시 수렴하옵니다." if seq_data["odd_subseq_conv"] else "❌ 홀수 항들만 따로 보아도 수렴하지 않사옵니다.")
    st.write("- 1/n 과의 곱 a_n·(1/n) :", "✅ 항별 곱으로 얻은 새 수열은 수렴하옵니다." if seq_data["with_1_over_n_conv"] else "❌ 그러한 곱을 취해도 수렴으로 이르지 못하옵니다.")

    st.markdown("### 🧾 해설 한 줄 요약")
    st.write(seq_data["explain"])

    st.markdown("### 🧠 성찰을 위한 물음")
    st.write("- 방금 던졌던 질문들 가운데, **가장 결정적인 질문**은 어느 것이었사온지?")
    st.write("- 지금 돌이켜 보면, **굳이 물을 필요가 없었던 질문**은 무엇이었사온지?")
    st.write("- 다시 한 번 같은 수열을 출제한다면, 그대는 **어떤 순서로 질문을 배치**하겠는가?")
