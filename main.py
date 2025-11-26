import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>EVOLVING LOGIC</title>

    <style>
        body { margin: 0; overflow: hidden; background-color: #0F172A; }
        canvas { display: block; }

        .overlay {
            position: absolute;
            top: 40px;
            left: 40px;
            text-align: left;
            pointer-events: none;
            color: white;
            font-family: 'Noto Sans KR', sans-serif;
            z-index: 10;
        }
        h1 {
            font-size: 3rem;
            font-weight: 900;
            margin: 0;
            letter-spacing: -1px;
            background: linear-gradient(to right, #38BDF8, #818CF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
        }
    </style>
</head>

<body>

<div class="overlay">
    <h1>EVOLVING LOGIC</h1>
</div>

<canvas id="mathCanvas"></canvas>

<script>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Mathematical Synthesis Visualization</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #0F172A; }
        canvas { display: block; }
        
        /* 레이아웃 변경: 타이틀을 좌측 상단으로 이동하여 중앙 확보 */
        .overlay {
            position: absolute;
            top: 40px;
            left: 40px;
            text-align: left;
            pointer-events: none;
            color: white;
            font-family: 'Noto Sans KR', sans-serif;
            z-index: 10;
        }
        h1 {
            font-size: 3rem;
            font-weight: 900;
            margin: 0;
            letter-spacing: -1px;
            background: linear-gradient(to right, #38BDF8, #818CF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
        }
        p.subtitle {
            font-size: 1rem;
            color: #94A3B8;
            margin-top: 0.5rem;
            max-width: 400px;
            line-height: 1.6;
        }

        /* 통계 박스 (우측 상단 고정) */
        .stat-box {
            position: absolute;
            top: 40px;
            right: 40px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 8px 16px;
            border-radius: 9999px;
            color: #64748B;
            font-family: monospace;
            font-size: 0.85rem;
            backdrop-filter: blur(4px);
            z-index: 10;
        }
        span.count { color: #38BDF8; font-weight: bold; }

        /* 하단 설명 패널: 화면을 가리지 않도록 하단 가장자리에 배치하고 투명도 높임 */
        .hud-panel {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 30px;
            width: 90%;
            justify-content: center; /* 중앙 정렬하되 양옆으로 퍼지게 */
            z-index: 10;
            pointer-events: none;
        }

        .hud-item {
            flex: 1;
            max-width: 300px; /* 너무 넓어지지 않게 제한 */
            background: rgba(15, 23, 42, 0.4); /* 투명도 높임 */
            border-left: 2px solid rgba(56, 189, 248, 0.5); /* 테두리 대신 왼쪽 라인만 강조 */
            padding: 15px 20px;
            color: #CBD5E1;
            font-family: 'Noto Sans KR', sans-serif;
            backdrop-filter: blur(2px);
            transition: all 0.3s ease;
            text-align: left;
        }
        
        .hud-title {
            color: #E0F2FE;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 6px;
        }
        
        .hud-desc {
            font-size: 0.8rem;
            color: #94A3B8;
            line-height: 1.4;
        }

        /* 모바일 대응 */
        @media (max-width: 768px) {
            .hud-panel {
                flex-direction: column;
                bottom: 10px;
                gap: 10px;
                align-items: center;
            }
            .hud-item { width: 90%; max-width: none; padding: 10px 15px; }
            h1 { font-size: 2rem; }
            .overlay { top: 20px; left: 20px; }
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
</head>
<body>

    <div class="overlay">
        <h1>EVOLVING LOGIC</h1>
        <p class="subtitle">반례는 시스템을 파괴하지 않습니다.<br>오히려 논리를 더 견고하게 만드는 양분이 됩니다.</p>
    </div>

    <div class="stat-box">
        LOGIC SYSTEM: <span class="count" id="blocked-count">0</span> DATA SYNTHESIZED
    </div>

    <!-- 하단 설명 패널 -->
    <div class="hud-panel">
        <div class="hud-item">
            <div class="hud-title">📐 구조적 방어 (Axioms)</div>
            <div class="hud-desc">
                견고한 기하학적 쉴드는 수학적 공리를 상징합니다. 외부의 공격에도 흔들리지 않는 기준점입니다.
            </div>
        </div>
        <div class="hud-item">
            <div class="hud-title">💠 흡수와 합성 (Synthesis)</div>
            <div class="hud-desc">
                붉은 반례(Error)가 닿으면 파괴되지 않고, <strong>푸른 에너지(Insight)</strong>로 변환되어 시스템 내부로 흡수됩니다.
            </div>
        </div>
        <div class="hud-item">
            <div class="hud-title">✨ 진화하는 논리 (Growth)</div>
            <div class="hud-desc">
                흡수된 에너지는 중심 핵으로 모여 시스템을 더 밝고 강하게 만듭니다. 반례가 많을수록 논리는 완벽해집니다.
            </div>
        </div>
    </div>

    <canvas id="mathCanvas"></canvas>

    <script>
        const canvas = document.getElementById('mathCanvas');
        const ctx = canvas.getContext('2d');
        const countEl = document.getElementById('blocked-count');

        let width, height;
        let particles = [];
        let absorbedParticles = []; // 흡수되어 중심으로 들어가는 입자들
        let blockedCount = 0;
        let tick = 0;
        let coreEnergy = 0; // 중심부 에너지 레벨 (반례 흡수 시 증가)

        // --- Configuration ---
        const SHIELD_RADIUS_BASE = 150; 
        const PARTICLE_SPEED = 3.5;
        const SPAWN_RATE = 0.25; 

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        // --- Classes ---

        class Particle { // The Attack (Counterexample)
            constructor() {
                const angle = Math.random() * Math.PI * 2;
                const dist = Math.max(width, height) / 1.3; 
                this.x = width/2 + Math.cos(angle) * dist;
                this.y = height/2 + Math.sin(angle) * dist;
                
                const angleToCenter = Math.atan2(height/2 - this.y, width/2 - this.x);
                this.vx = Math.cos(angleToCenter) * (PARTICLE_SPEED + Math.random());
                this.vy = Math.sin(angleToCenter) * (PARTICLE_SPEED + Math.random());
                
                this.size = Math.random() * 2 + 1.5;
                this.color = `rgba(239, 68, 68, ${Math.random()*0.5 + 0.5})`; // Initial Red
                this.trail = [];
                this.absorbed = false; // 흡수 상태 플래그
            }

            update() {
                if (this.absorbed) {
                    // 흡수 모드: 중심으로 회전하며 빨려들어감
                    const dx = width/2 - this.x;
                    const dy = height/2 - this.y;
                    this.x += dx * 0.08; // 중심으로 Lerp
                    this.y += dy * 0.08;
                    this.size *= 0.95; // 점점 작아짐
                    
                    if (this.size < 0.1) {
                        this.dead = true;
                        coreEnergy += 0.5; // 핵 에너지 증가
                        if(coreEnergy > 20) coreEnergy = 20; // Max cap
                    }
                    return;
                }

                // 일반 이동 모드
                this.x += this.vx;
                this.y += this.vy;
                
                this.trail.push({x: this.x, y: this.y});
                if(this.trail.length > 8) this.trail.shift();

                const dx = this.x - width/2;
                const dy = this.y - height/2;
                const dist = Math.sqrt(dx*dx + dy*dy);
                
                const currentShieldR = SHIELD_RADIUS_BASE + Math.sin(tick * 0.05) * 10;

                // 충돌 감지
                if (dist < currentShieldR) {
                    this.absorbed = true; // 죽지 않고 흡수됨
                    this.color = '#38BDF8'; // Blue/Cyan으로 변환
                    blockedCount++;
                    countEl.innerText = blockedCount;
                    
                    // 충돌 이펙트 (반례가 닿은 지점)
                    // createRipple(this.x, this.y, angleFromCenter(this.x, this.y)); 
                }
            }

            draw() {
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();

                if (!this.absorbed) {
                    ctx.beginPath();
                    ctx.strokeStyle = this.color;
                    ctx.lineWidth = 0.5;
                    for(let i=0; i<this.trail.length; i++){
                        ctx.lineTo(this.trail[i].x, this.trail[i].y);
                    }
                    ctx.stroke();
                }
            }
        }

        // --- Main Loop ---

        function drawShield() {
            const cx = width / 2;
            const cy = height / 2;
            const radius = SHIELD_RADIUS_BASE + Math.sin(tick * 0.05) * 10;
            
            // Core Glow (Reacts to absorbed energy)
            const coreGlow = 10 + coreEnergy * 2;
            ctx.shadowBlur = coreGlow;
            ctx.shadowColor = '#38BDF8';

            // 1. Core (Synthesis Reactor)
            ctx.beginPath();
            ctx.arc(cx, cy, radius * 0.2 + (coreEnergy), 0, Math.PI * 2); // 에너지가 찰수록 커짐
            ctx.fillStyle = `rgba(56, 189, 248, ${0.2 + coreEnergy * 0.02})`;
            ctx.fill();
            ctx.strokeStyle = '#38BDF8';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            ctx.shadowBlur = 0; // Reset shadow

            // 2. Logic Layers
            ctx.save();
            ctx.translate(cx, cy);
            
            // Hexagon
            ctx.rotate(tick * 0.003);
            ctx.beginPath();
            for (let i = 0; i < 6; i++) {
                const angle = (i * Math.PI * 2) / 6;
                ctx.lineTo(Math.cos(angle) * radius * 0.9, Math.sin(angle) * radius * 0.9);
            }
            ctx.closePath();
            ctx.strokeStyle = 'rgba(125, 211, 252, 0.3)';
            ctx.lineWidth = 1;
            ctx.stroke();

            // Triangle
            ctx.rotate(-tick * 0.01);
            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const angle = (i * Math.PI * 2) / 3;
                ctx.lineTo(Math.cos(angle) * radius * 0.6, Math.sin(angle) * radius * 0.6);
            }
            ctx.closePath();
            ctx.strokeStyle = 'rgba(167, 139, 250, 0.5)';
            ctx.lineWidth = 1;
            ctx.stroke();
            
            ctx.restore();

            // 3. Absorption Field (Boundary)
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(56, 189, 248, 0.6)`;
            ctx.lineWidth = 1;
            ctx.setLineDash([2, 10]); // 데이터 스트림 느낌
            ctx.lineDashOffset = -tick; // 흐르는 효과
            ctx.stroke();
            ctx.setLineDash([]);
        }

        function animate() {
            // Trail effect background
            ctx.fillStyle = 'rgba(15, 23, 42, 0.3)'; 
            ctx.fillRect(0, 0, width, height);

            tick++;
            
            // 에너지 자연 감소 (소비)
            if (coreEnergy > 0) coreEnergy -= 0.05;

            if (Math.random() < SPAWN_RATE) {
                particles.push(new Particle());
            }

            drawShield();

            particles.forEach((p, index) => {
                p.update();
                p.draw();
                if (p.dead) particles.splice(index, 1);
            });

            requestAnimationFrame(animate);
        }

        animate();

    </script>
</body>
</html></script>

</body>
</html>
"""

components.html(html_code, height=1400, scrolling=False)
