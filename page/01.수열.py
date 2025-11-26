# 01_sequence.py
# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import sympy as sp

st.set_page_config(page_title="수열의 극한 탐구실", layout="wide")

st.title("📈 수열의 극한 탐구실")
st.caption("Simple is structural. — 한 문장, 전체 구조")

# 공통 심볼
n = sp.symbols('n')

# 유틸: 수열 생성 함수
def generate_sequence(expr_str, n_min=1, n_max=50):
    """
    expr_str: '1/n' 같은 문자열
    n_min ~ n_max: 정수 범위
    반환: 리스트(float), 오류시 None
    """
    try:
        expr = sp.sympify(expr_str)
    except Exception:
        return None

    seq = []
    for k in range(n_min, n_max + 1):
        try:
            val = expr.subs(n, k)
            seq.append(float(val))
        except Exception:
            seq.append(np.nan)
    return seq

# 유틸: 간단한 수렴/발산 힌트
def rough_limit_hint(seq):
    arr = np.array(seq, dtype=float)
    # NaN 제거
    arr = arr[~np.isnan(arr)]
    if len(arr) < 10:
        return "데이터가 충분하지 않습니다."

    tail = arr[-10:]
    std_tail = np.nanstd(tail)
    mean_tail = np.nanmean(tail)

    if np.any(np.abs(arr) > 1e6):
        return "값이 매우 커지고 있습니다 → 발산 가능성이 큽니다."
    if std_tail < 1e-3:
        return f"꼬리 부분이 거의 변하지 않습니다 → 수렴할 가능성이 큽니다 (근사값 ≈ {mean_tail:.4f})"
    if np.nanmean(np.abs(tail)) < 1e-2:
        return f"0 근처에서 진동하거나 서서히 접근하는 것처럼 보입니다 (평균 ≈ {mean_tail:.4f})"
    return "진동하거나 불규칙해 보입니다 → 극한이 존재하지 않을 수 있습니다."

# 사이드바
mode = st.sidebar.radio(
    "탐구 카테고리 선택",
    [
        "① 표현 실험실 (표·그래프)",
        "② 유사성 & 구조 (a, a')",
        "③ 연산 & 조건 (ab, a'b)",
        "④ 반례 & 일반화 메모"
    ]
)

# =========================
# ① 표현 실험실
# =========================
if mode == "① 표현 실험실 (표·그래프)":
    st.header("① 표현 실험실 : 표 · 그래프 · 식")

    st.markdown(
        """
        - **목표**: 같은 수열이 여러 표현(표, 그래프, 식)로 나타날 때,  
          *무엇이 같고 무엇이 다르게 보이는지* 스스로 탐색해 보는 공간입니다.
        - 아래에 일반항 `a(n)`을 입력하고, 표와 그래프를 비교해 보세요.
        """
    )

    expr_str = st.text_input("일반항 a(n)을 입력하세요 (예: 1/n, (-1)**n, (3*n+1)/(2*n-1))", value="1/n")

    seq = generate_sequence(expr_str, 1, 50)
    if seq is None:
        st.error("수식을 해석할 수 없습니다. n을 포함한 올바른 수학식을 입력해 주세요.")
        st.stop()

    df = pd.DataFrame({"n": range(1, 51), "a_n": seq})

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("표(일부)")
        st.dataframe(df.head(10), use_container_width=True)
    with col2:
        st.subheader("그래프")
        fig = px.line(df, x="n", y="a_n", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 표현별 관찰 기록")
    st.write("- 같은 수열인데, **표**와 **그래프**에서 어떻게 다르게 느껴지나요?")
    st.write("- 이 수열이 **수렴/발산/진동**하는지, 표현마다 판단이 달라질까요?")

    st.markdown("#### 메모")
    note = st.text_area("표 vs 그래프 비교해서 느낀 점을 적어보세요.")
    if st.button("메모 저장(로컬에 복사해서 사용하세요)"):
        st.success("이 텍스트 박스의 내용을 복사해 보고서나 활동지에 붙여넣으세요!")

    st.markdown("#### 간단한 극한 직관 힌트")
    st.info(rough_limit_hint(seq))


# =========================
# ② 유사성 & 구조
# =========================
elif mode == "② 유사성 & 구조 (a, a')":
    st.header("② 유사성 & 구조 : a와 a' 비교")

    st.markdown(
        """
        - **목표**: 수열 a와 a'가 '닮았다'는 것이 어떤 의미인지 탐구합니다.  
        - a(n)을 하나 정하고, 변형 방법을 골라 a'(n)을 만들어 보세요.
        """
    )

    expr_a = st.text_input("기본 수열 a(n)을 입력하세요", value="1/n")
    seq_a = generate_sequence(expr_a, 1, 50)
    if seq_a is None:
        st.error("a(n) 수식을 해석할 수 없습니다.")
        st.stop()

    transform = st.selectbox("a'(n) 생성 방식 선택", ["k배 하기: a' = k·a", "상수 더하기: a' = a + c"])
    col_kc1, col_kc2 = st.columns(2)
    with col_kc1:
        k = st.number_input("k 값 (배수)", value=2.0)
    with col_kc2:
        c = st.number_input("c 값 (더하는 상수)", value=1.0)

    if transform.startswith("k배"):
        seq_ap = list(k * np.array(seq_a, dtype=float))
        desc = f"a'(n) = {k} · a(n)"
    else:
        seq_ap = list(np.array(seq_a, dtype=float) + c)
        desc = f"a'(n) = a(n) + {c}"

    df2 = pd.DataFrame(
        {
            "n": range(1, 51),
            "a_n": seq_a,
            "a_n_prime": seq_ap
        }
    )

    st.markdown(f"**생성된 a'(n):** {desc}")

    fig2 = px.line(
        df2,
        x="n",
        y=["a_n", "a_n_prime"],
        markers=True,
        labels={"value": "값", "variable": "수열"},
        title="a(n) vs a'(n) 비교"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🧠 유사성에 대한 질문")
    st.write("- 그래프를 보았을 때, a와 a'가 **어떤 점에서 닮았다고** 말할 수 있나요?")
    st.write("- 두 수열의 **극한값**은 어떻게 될까요? 같을까요, 다를까요? 왜 그렇게 생각하나요?")

    st.markdown("#### 메모")
    note2 = st.text_area("a와 a'의 유사성을 말로 설명해 보세요.")
    st.caption("예: '두 수열은 모두 0으로 수렴하지만, a'는 항상 a보다 1만큼 크다.' 등")


# =========================
# ③ 연산 & 조건
# =========================
elif mode == "③ 연산 & 조건 (ab, a'b)":
    st.header("③ 연산 & 조건 : ab와 a'b 비교")

    st.markdown(
        """
        - **목표**: a, a', b 세 수열의 구조와 조건에 따라  
          **곱 수열 ab, a'b의 극한이 어떻게 달라지는지** 실험합니다.
        """
    )

    col_a, col_b = st.columns(2)
    with col_a:
        expr_a3 = st.text_input("a(n)을 입력하세요", value="1/n")
    with col_b:
        expr_b3 = st.text_input("b(n)을 입력하세요", value="n")

    seq_a3 = generate_sequence(expr_a3, 1, 50)
    seq_b3 = generate_sequence(expr_b3, 1, 50)

    if seq_a3 is None or seq_b3 is None:
        st.error("a(n) 또는 b(n) 수식을 해석할 수 없습니다.")
        st.stop()

    # a' 생성
    transform3 = st.selectbox("a'(n) 생성 방식", ["k배: a' = k·a", "상수 더하기: a' = a + c"], key="op_transform")
    col_kc3a, col_kc3b = st.columns(2)
    with col_kc3a:
        k3 = st.number_input("k 값 (배수)", value=2.0, key="op_k")
    with col_kc3b:
        c3 = st.number_input("c 값 (상수)", value=1.0, key="op_c")

    if transform3.startswith("k배"):
        seq_ap3 = list(k3 * np.array(seq_a3, dtype=float))
        desc3 = f"a'(n) = {k3} · a(n)"
    else:
        seq_ap3 = list(np.array(seq_a3, dtype=float) + c3)
        desc3 = f"a'(n) = a(n) + {c3}"

    # 곱 수열
    arr_a3 = np.array(seq_a3, dtype=float)
    arr_ap3 = np.array(seq_ap3, dtype=float)
    arr_b3 = np.array(seq_b3, dtype=float)

    ab = arr_a3 * arr_b3
    apb = arr_ap3 * arr_b3

    df3 = pd.DataFrame(
        {
            "n": range(1, 50 + 1),
            "ab": ab,
            "a'b": apb
        }
    )

    st.markdown(f"**a'(n):** {desc3}")

    st.subheader("ab vs a'b 그래프 비교")
    fig3 = px.line(df3, x="n", y=["ab", "a'b"], labels={"value": "값", "variable": "수열"})
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 🧠 조건에 대한 질문")
    st.write("- a와 a'가 '유사'하다고 해도, b가 발산하면 **ab와 a'b는 어떻게 달라질 수 있을까요?**")
    st.write("- ab가 수렴한다고 해서 **항상 a와 b가 각각 수렴한다고 말할 수 있을까요?**")

    st.markdown("#### ab에 대한 간단한 극한 힌트")
    st.info("ab에 대한 직관: " + rough_limit_hint(ab))
    st.markdown("#### a'b에 대한 간단한 극한 힌트")
    st.info("a'b에 대한 직관: " + rough_limit_hint(apb))

    st.markdown("#### 내 언어로 정리해 보기")
    st.text_area(
        "위 상황에서 '연산의 안정성(조건부 성립)'에 대해 느낀 점을 적어보세요.",
        placeholder="예: 'a와 a'는 닮았지만, b가 너무 빠르게 커지면 ab와 a'b의 거리가 함께 커진다.' 등"
    )


# =========================
# ④ 반례 & 일반화 메모
# =========================
elif mode == "④ 반례 & 일반화 메모":
    st.header("④ 반례 & 일반화 : 조건을 다시 쓰다")

    st.markdown(
        """
        - **목표**: 수열의 극한 단원에서 등장하는 여러 **반례 상황**을 정리하고,  
          그 반례들을 더 이상 깨지 않게 만드는 **조건/일반화 문장**을 스스로 만들어 봅니다.
        """
    )

    st.subheader("예시 반례 카드 모음 (텍스트 버전)")
    examples = {
        "① ab → 0 이지만 a, b는 둘 다 0으로 가지 않는 예":
            "예: a(n) = 1/n, b(n) = (-1)^n · n  →  ab(n) = (-1)^n",
        "② a, b는 둘 다 발산하지만 ab는 수렴하는 예":
            "예: a(n) = n, b(n) = 1/n  →  ab(n) = 1",
        "③ 그래프만 보면 수렴처럼 보이지만 실제로는 발산":
            "예: a(n) = ln(n), sqrt(n) 등",
        "④ 유사한 구조인데 극한이 다른 수열 쌍":
            "예: a(n) = 1/n,  a'(n) = (n+1)/(n^2) 등 (둘 다 0으로 가지만 패턴이 다름)"
    }

    selected = st.selectbox("관심 있는 반례 유형을 선택하세요", list(examples.keys()))
    st.markdown(f"**설명:** {examples[selected]}")

    st.markdown("### 1) 이 반례가 깨뜨리는 '원리'는 무엇인가요?")
    wrong_rule = st.text_input("예: 'ab가 수렴하면 a와 b도 수렴한다' 등")

    st.markdown("### 2) 이 반례를 막기 위해 어떤 조건이 필요할까요?")
    cond_text = st.text_area("조건을 덧붙여 문장을 다시 써보세요.")

    st.markdown("### 3) 더 이상 깨지지 않는 '일반화 문장' 만들기")
    generalization = st.text_area(
        "조건을 포함한 '최종 원리'를 한 문장으로 써보세요.",
        placeholder="예: '두 수열 a, b가 모두 수렴하고, 그 극한 중 하나가 0이 아니면, 곱의 극한은 각 극한의 곱과 같다.'"
    )

    st.markdown("---")
    st.markdown("#### ✍️ 정리용 복사본")
    st.write("아래 내용을 복사해서 활동지/보고서에 활용할 수 있습니다.")
    st.code(
        f"[반례 유형]\n{selected}\n\n"
        f"[깨지는 원리]\n{wrong_rule}\n\n"
        f"[필요 조건]\n{cond_text}\n\n"
        f"[최종 일반화 문장]\n{generalization}",
        language="text"
    )
