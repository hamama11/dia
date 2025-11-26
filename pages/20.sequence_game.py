# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("🎮 수열 스무고개: 조건으로 맞혀라!")

st.caption(
    "출제자는 수열의 정체를 숨기고, "
    "학생들은 표·그래프와 YES/NO 질문만으로 "
    "수렴/발산과 구조를 추론합니다."
)

# -----------------------------
# 0. 숨겨진 수열 데이터 준비
# -----------------------------
# 각 수열은 흥미로운 성질을 갖도록 일부러 골랐음
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
        "n_times_conv": False,    # n*a_n = 1 → 수렴이지만 0이 아님
        "abs_conv": True,
        "piecewise2": False,
        "explain": "a_n = 1/n 은 단조 감소하고 유계인 수열로, 0으로 수렴합니다."
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
        "n_times_conv": None,     # n*a_n = ±n → 발산
        "abs_conv": False,        # |a_n|=1 → 수렴(X), 상수지만 극한=1 (선생님이 설명용)
        "piecewise2": True,
        "explain": "a_n = (-1)^n 은 부호가 계속 바뀌며 두 값 사이를 진동하여 수렴하지 않습니다."
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
        "n_times_conv": None,     # n*a_n = n^2 → 발산
        "abs_conv": False,
        "piecewise2": False,
        "explain": "a_n = n 은 단조 증가하지만 위로 유계가 아니므로 발산합니다."
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
        "n_times_conv": False,    # n*a_n = (-1)^n → 발산
        "abs_conv": True,         # |a_n|=1/n → 0으로 수렴
        "piecewise2": True,
        "explain": "a_n = (-1)^n / n 은 부호는 바뀌지만 크기는 0으로 가까워져서 수렴합니다."
    },
    {
        "name": "ln(n)",
        "expr": r"a_n = \ln n",
        "preview_n": 40,
        "seq": lambda n: np.log(n),
        "convergent": False,
        "limit_value": None,
        "bounded": False,
        "monotone": True,
        "sign_changes": False,
        "n_times_conv": None,     # n*ln(n) → 발산
        "abs_conv": False,
        "piecewise2": False,
        "explain": "a_n = ln n 은 매우 느리지만 계속 증가하여 발산합니다."
    },
    {
        "name": "sin(n)",
        "expr": r"a_n = \sin n",
        "preview_n": 60,
        "seq": lambda n: np.sin(n),
        "convergent": False,
        "limit_value": None,
        "bounded": True,
        "monotone": False,
        "sign_changes": True,
        "n_times_conv": None,     # n*sin n → 보통 발산(제한 없음)
        "abs_conv": False,
        "piecewise2": False,
        "explain": "a_n = sin n 은 -1과 1 사이에서 복잡하게 진동하며 수렴하지 않습니다."
    },
]

# 질문 목록 정의
QUESTIONS = [
    ("convergent", "이 수열은 **수렴**하는가?"),
    ("bounded", "이 수열은 **위·아래로 유계**인가?"),
    ("monotone", "어느 시점부터 **단조**(계속 증가 또는 계속 감소)인가?"),
    ("sign_changes", "항의 **부호가 무한히 자주 바뀌는가?**"),
    ("n_times_conv", "**n·a_n** 은 수렴하는가?"),
    ("abs_conv", r"**|a_n|** 은 수렴하는가?"),
    ("piecewise2", "짝수/홀수 등 **두 개의 식으로 정의되는 수열**인가?")
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
    if st.button("🔄 새 라운드 시작하기"):
        st.session_state.seq_idx = int(np.random.randint(0, len(SEQUENCES)))
        st.session_state.asked = {}
        st.session_state.q_count = 0
        st.session_state.show_answer = False

with col_info:
    if st.session_state.seq_idx is None:
        st.info("👉 먼저 **'새 라운드 시작하기'** 버튼을 눌러 수열을 하나 뽑으세요.")
    else:
        st.success("새 라운드가 진행 중입니다. 질문을 던져보세요!")

if st.session_state.seq_idx is None:
    st.stop()

seq_data = SEQUENCES[st.session_state.seq_idx]

# -----------------------------
# 3. 표 & 그래프 (초기 정보)
# -----------------------------
st.markdown("## 1️⃣ 공개된 정보: 표와 그래프 (초기 몇 항만)")

N_PREVIEW = seq_data["preview_n"]
n_values = np.arange(1, N_PREVIEW + 1)
a_values = np.array([seq_data["seq"](k) for k in n_values], dtype=float)

df = pd.DataFrame({"n": n_values, "a_n": a_values})

col_table, col_plot = st.columns(2)
with col_table:
    st.subheader("표 (일부 항)")
    st.dataframe(df.head(10), use_container_width=True)
    st.caption("※ 출제자는 뒤에 어떤 일이 일어나는지 알고 있지만, 학생은 여기까지만 볼 수 있다고 가정합니다.")

with col_plot:
    st.subheader("그래프")
    fig = px.line(df, x="n", y="a_n", markers=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# 4. 질문 라운드
# -----------------------------
st.markdown("## 2️⃣ YES / NO 질문하기")

st.write(
    f"- 이 라운드에서 질문할 수 있는 총 횟수: **{MAX_QUESTIONS}회**"
)
st.write(
    f"- 지금까지 사용한 질문 수: **{st.session_state.q_count}회**"
)

remaining_q = [q for q in QUESTIONS if q[0] not in st.session_state.asked]

if st.session_state.q_count >= MAX_QUESTIONS:
    st.warning("질문 사용 한도에 도달했습니다. 이제 가진 정보로 추론해 보세요!")
else:
    if not remaining_q:
        st.info("더 이상 새로 물어볼 수 있는 질문이 없습니다.")
    else:
        q_key, q_label = st.selectbox(
            "질문을 하나 선택하세요 (아직 묻지 않은 것만 표시됩니다)",
            remaining_q,
            format_func=lambda x: x[1]
        )

        if st.button("❓ 이 질문 하기"):
            # 실제 답 찾기
            ans = seq_data[q_key]  # True / False / None
            st.session_state.asked[q_key] = ans
            st.session_state.q_count += 1

# 이미 물어본 질문과 답 요약
if st.session_state.asked:
    st.markdown("### 💬 지금까지 얻은 YES/NO 정보")
    for key, ans in st.session_state.asked.items():
        label = dict(QUESTIONS)[key]
        if ans is True:
            txt = "YES"
        elif ans is False:
            txt = "NO"
        else:
            txt = "판단 불가 / 애매함 (출제자가 미리 정의한 값 없음)"
        st.write(f"- **{label}** ➜ **{txt}**")

st.markdown("---")

# -----------------------------
# 5. 수렴/발산 추론 구역
# -----------------------------
st.markdown("## 3️⃣ 이제 당신의 추론을 적어보세요")

col_judge1, col_judge2 = st.columns(2)
with col_judge1:
    verdict = st.radio(
        "이 수열은…",
        ["수렴한다", "발산한다", "판단 보류"],
        index=2
    )
with col_judge2:
    guess_limit = st.text_input(
        "극한값을 추측한다면? (없으면 비워두기)",
        value=""
    )

reason = st.text_area(
    "당신의 판단 근거를 적어보세요.",
    placeholder="예: 표를 보면 점점 줄어들고, 출제자의 답변으로 단조·유계임을 알게 되었으므로 0으로 수렴한다고 추측한다 등"
)

st.markdown("---")

# -----------------------------
# 6. 정답 공개
# -----------------------------
if st.button("📢 정답 공개"):
    st.session_state.show_answer = True

if st.session_state.show_answer:
    st.markdown("## ✅ 정답 & 해설")

    st.write(f"**숨겨진 수열 이름:** `{seq_data['name']}`")
    st.latex(seq_data["expr"])

    if seq_data["convergent"]:
        st.write(f"- 이 수열은 **수렴**합니다. 극한값은 **{seq_data['limit_value']}** 입니다.")
    else:
        st.write("- 이 수열은 **수렴하지 않습니다. (발산 / 진동)**")

    st.write("- 유계 여부:", "✅ 유계" if seq_data["bounded"] else "❌ 유계 아님")
    st.write("- 단조성:", "✅ 어느 시점부터 단조" if seq_data["monotone"] else "❌ 단조 아님")
    st.write("- 부호 변화:", "✅ 부호가 무한히 자주 바뀜" if seq_data["sign_changes"] else "❌ 부호 변화 없음 또는 제한적")
    st.write("- n·a_n 수렴 여부:", "✅ 수렴" if seq_data["n_times_conv"] else "❌ 수렴하지 않거나 정의 안 함")
    st.write("- |a_n| 수렴 여부:", "✅ 수렴" if seq_data["abs_conv"] else "❌ 수렴하지 않음")
    st.write("- 두 개의 식으로 정의되는가:", "✅ 예(짝수/홀수 등)" if seq_data["piecewise2"] else "❌ 아니오")

    st.markdown("### 🧾 해설 요약")
    st.write(seq_data["explain"])

    st.markdown("### 🧠 되돌아보기 질문")
    st.write("- 내가 던진 질문들 중, **결정적으로 도움이 된 질문**은 무엇이었는가?")
    st.write("- 지금 돌아보면, **쓸데없이 쓴 질문**은 무엇이었는가?")
    st.write("- 같은 수열을 다시 출제한다면, 나는 어떤 순서로 질문을 던질 것인가?")

