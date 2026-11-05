import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="천체 궤도 역학 시뮬레이터", page_icon="🪐", layout="wide")

st.title("🪐 케플러 법칙 기반 천체 궤도 & 역학 시뮬레이터")
st.markdown("""
본 프로그램은 **물리학 II / 지구과학 II의 '만유인력과 행성의 운동'** 단원과 연계하여, 
케플러 3대 법칙($T^2 = a^3$, 면적 속도 일정의 법칙)을 바탕으로 천체의 타원 궤도와 속도 변화를 시각화합니다.
""")

# 프리셋 데이터 (장반경 a, 이심률 e)
PRESETS = {
    "지구 (Earth)": {"a": 1.0, "e": 0.0167},
    "수성 (Mercury)": {"a": 0.387, "e": 0.2056},
    "화성 (Mars)": {"a": 1.524, "e": 0.0934},
    "목성 (Jupiter)": {"a": 5.204, "e": 0.0489},
    "핼리 혜성 (Halley's Comet)": {"a": 17.83, "e": 0.967},
    "직접 탐구 (Custom)": {"a": 2.0, "e": 0.500}
}

# 사이드바 컨트롤러
st.sidebar.header("⚙️ 궤도 파라미터 설정")
selected_preset = st.sidebar.selectbox("천체 선택", list(PRESETS.keys()))

if selected_preset == "직접 탐구 (Custom)":
    a = st.sidebar.slider("궤도 장반경 (a, AU)", 0.1, 30.0, 2.0, 0.1)
    e = st.sidebar.slider("이심률 (e)", 0.0, 0.95, 0.5, 0.01)
else:
    a = PRESETS[selected_preset]["a"]
    e = PRESETS[selected_preset]["e"]

# 케플러 법칙 계산
# 1. 케플러 조화의 법칙 (T^2 = a^3)
period = np.sqrt(a**3)

# 2. 근일점 및 원일점 거리
r_perihelion = a * (1 - e)
r_aphelion = a * (1 + e)

# 3. 면적 속도 일정 법칙에 의한 속도 비 (v_peri / v_aph = r_aph / r_peri)
velocity_ratio = r_aphelion / r_perihelion

# 요약 메트릭 출력
col1, col2, col3, col4 = st.columns(4)
col1.metric("공전 주기 (T)", f"{round(period, 2)} 년")
col2.metric("근일점 거리", f"{round(r_perihelion, 2)} AU")
col3.metric("원일점 거리", f"{round(r_aphelion, 2)} AU")
col4.metric("근일점/원일점 속도 비", f"{round(velocity_ratio, 2)} 배")

st.divider()

# 궤도 좌표 계산 (극방정식: r = a(1-e^2) / (1 + e*cos(theta)))
theta = np.linspace(0, 2 * np.pi, 500)
r = (a * (1 - e**2)) / (1 + e * np.cos(theta))

# 직교좌표계 변환 (초점이 원점에 오도록 이동)
x = r * np.cos(theta)
y = r * np.sin(theta)

# Plotly 그래프 생성
fig = go.Figure()

# 궤도 선
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='공전 궤도', line=dict(color='cyan', width=2)))

# 중심 별 (태양 - 초점 위치)
fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', text=["태양 (초점)"], textposition="top center",
                         marker=dict(size=18, color='gold'), name='중심 별'))

# 근일점 & 원일점 표시
fig.add_trace(go.Scatter(x=[r_perihelion], y=[0], mode='markers+text', text=["근일점 (최대 속도)"], textposition="bottom right",
                         marker=dict(size=10, color='red'), name='근일점'))
fig.add_trace(go.Scatter(x=[-r_aphelion], y=[0], mode='markers+text', text=["원일점 (최저 속도)"], textposition="bottom left",
                         marker=dict(size=10, color='blue'), name='원일점'))

# 그래프 레이아웃 설정
fig.update_layout(
    title=f"🪐 {selected_preset} 타원 궤도 시각화 (장반경: {a} AU, 이심률: {e})",
    xaxis_title="X 좌표 (AU)",
    yaxis_title="Y 좌표 (AU)",
    yaxis=dict(scaleanchor="x", scaleratio=1), # 1:1 비율 유지
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# 탐구 설명 박스
st.info("""
💡 **우주과학 탐구 포인트**
* **케플러 제1법칙 (타원 궤도의 법칙)**: 이심률($e$)이 0에 가까울수록 원에 가까워지며, 1에 가까워질수록 길쭉한 타원이 됩니다.
* **케플러 제2법칙 (면적 속도 일정의 법칙)**: 행성은 태양과 가까운 근일점에서 가장 빠르고, 원일점에서 가장 천천히 이동합니다.
* **케플러 제3법칙 (조화의 법칙)**: 공전 주기의 제곱($T^2$)은 궤도 장반경의 세제곱($a^3$)에 비례합니다.
""")
