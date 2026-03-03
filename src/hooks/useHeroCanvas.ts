import { useEffect, useRef, useCallback } from "react";

export function useHeroCanvas() {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    const initCanvas = useCallback(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        let w: number, h: number;
        let mouseX = 0, mouseY = 0;
        let animId: number;

        function resize() {
            const hero = canvas!.parentElement;
            if (!hero) return;
            w = canvas!.width = hero.offsetWidth;
            h = canvas!.height = hero.offsetHeight;
        }

        // --- STARS: Multiple layers for depth ---
        type Star = { x: number; y: number; r: number; twinkle: number; twinkleSpeed: number; baseAlpha: number };
        type Layer = { stars: Star[]; speed: number };
        const layers: Layer[] = [];

        function createStarLayers() {
            layers.length = 0;
            const configs = [
                { count: 300, maxR: 0.8, speed: 0.1, alpha: 0.3 },
                { count: 150, maxR: 1.2, speed: 0.3, alpha: 0.5 },
                { count: 60, maxR: 2.0, speed: 0.6, alpha: 0.8 },
            ];
            configs.forEach((cfg) => {
                const stars: Star[] = [];
                for (let i = 0; i < cfg.count; i++) {
                    stars.push({
                        x: Math.random() * w,
                        y: Math.random() * h,
                        r: Math.random() * cfg.maxR + 0.2,
                        twinkle: Math.random() * Math.PI * 2,
                        twinkleSpeed: 0.01 + Math.random() * 0.03,
                        baseAlpha: cfg.alpha * (0.4 + Math.random() * 0.6),
                    });
                }
                layers.push({ stars, speed: cfg.speed });
            });
        }

        // --- 3D WIREFRAME GLOBE ---
        const globe = {
            cx: 0, cy: 0, radius: 0,
            rotationY: 0,
            rotationX: 0.3,
        };

        function initGlobe() {
            globe.cx = w * 0.72;
            globe.cy = h * 0.45;
            globe.radius = Math.min(w, h) * 0.28;
        }

        function drawGlobe(t: number) {
            if (!ctx) return;
            globe.rotationY = t * 0.15;
            const R = globe.radius;

            // Atmosphere glow
            const grad = ctx.createRadialGradient(globe.cx, globe.cy, R * 0.2, globe.cx, globe.cy, R * 1.6);
            grad.addColorStop(0, "rgba(59, 130, 246, 0.06)");
            grad.addColorStop(0.3, "rgba(59, 130, 246, 0.04)");
            grad.addColorStop(0.6, "rgba(99, 102, 241, 0.02)");
            grad.addColorStop(1, "rgba(0, 0, 0, 0)");
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(globe.cx, globe.cy, R * 1.6, 0, Math.PI * 2);
            ctx.fill();

            // Inner glow
            const innerGrad = ctx.createRadialGradient(globe.cx, globe.cy, 0, globe.cx, globe.cy, R);
            innerGrad.addColorStop(0, "rgba(59, 130, 246, 0.08)");
            innerGrad.addColorStop(0.7, "rgba(59, 130, 246, 0.03)");
            innerGrad.addColorStop(1, "rgba(59, 130, 246, 0)");
            ctx.fillStyle = innerGrad;
            ctx.beginPath();
            ctx.arc(globe.cx, globe.cy, R, 0, Math.PI * 2);
            ctx.fill();

            // Clean outer circle
            ctx.beginPath();
            ctx.arc(globe.cx, globe.cy, R, 0, Math.PI * 2);
            ctx.strokeStyle = "rgba(59, 130, 246, 0.15)";
            ctx.lineWidth = 1;
            ctx.stroke();

            // Orbiting ring (tilted ellipse)
            ctx.save();
            ctx.translate(globe.cx, globe.cy);
            ctx.rotate(-0.2);
            ctx.beginPath();
            ctx.ellipse(0, 0, R * 1.35, R * 0.25, 0, 0, Math.PI * 2);
            ctx.strokeStyle = "rgba(59, 130, 246, 0.15)";
            ctx.lineWidth = 1;
            ctx.setLineDash([4, 8]);
            ctx.stroke();
            ctx.setLineDash([]);

            // Orbiting satellite dot
            const satAngle = t * 0.5;
            const satX = Math.cos(satAngle) * R * 1.35;
            const satY = Math.sin(satAngle) * R * 0.25;
            ctx.beginPath();
            ctx.arc(satX, satY, 3, 0, Math.PI * 2);
            ctx.fillStyle = "#60a5fa";
            ctx.fill();
            ctx.beginPath();
            ctx.arc(satX, satY, 8, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(96, 165, 250, 0.2)";
            ctx.fill();
            ctx.restore();

            // Second orbit ring
            ctx.save();
            ctx.translate(globe.cx, globe.cy);
            ctx.rotate(0.8);
            ctx.beginPath();
            ctx.ellipse(0, 0, R * 1.15, R * 0.3, 0, 0, Math.PI * 2);
            ctx.strokeStyle = "rgba(249, 115, 22, 0.1)";
            ctx.lineWidth = 0.8;
            ctx.setLineDash([3, 10]);
            ctx.stroke();
            ctx.setLineDash([]);

            const sat2Angle = -t * 0.35;
            const sat2X = Math.cos(sat2Angle) * R * 1.15;
            const sat2Y = Math.sin(sat2Angle) * R * 0.3;
            ctx.beginPath();
            ctx.arc(sat2X, sat2Y, 2.5, 0, Math.PI * 2);
            ctx.fillStyle = "#f97316";
            ctx.fill();
            ctx.beginPath();
            ctx.arc(sat2X, sat2Y, 6, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(249, 115, 22, 0.15)";
            ctx.fill();
            ctx.restore();
        }

        // --- SHOOTING STARS ---
        type ShootingStar = { x: number; y: number; vx: number; vy: number; life: number; decay: number; len: number };
        let shootingStars: ShootingStar[] = [];

        // --- ROCKETS ---
        type TrailPoint = { x: number; y: number; life: number };
        type Rocket = { x: number; y: number; vx: number; vy: number; life: number; size: number; trail: TrailPoint[] };
        let rockets: Rocket[] = [];

        function spawnRocket() {
            const side = Math.random() > 0.5;
            rockets.push({
                x: side ? -20 : w + 20,
                y: h * 0.2 + Math.random() * h * 0.5,
                vx: (side ? 1 : -1) * (2 + Math.random() * 2),
                vy: -0.5 - Math.random() * 1.5,
                life: 1,
                size: 1.5 + Math.random(),
                trail: [],
            });
        }

        // --- NEBULA CLOUDS ---
        function drawNebula() {
            if (!ctx) return;
            const nebulas = [
                { x: w * 0.15, y: h * 0.2, r: 250, color: "59, 130, 246" },
                { x: w * 0.82, y: h * 0.7, r: 200, color: "139, 92, 246" },
                { x: w * 0.5, y: h * 0.85, r: 300, color: "99, 102, 241" },
            ];
            nebulas.forEach((n) => {
                const grad = ctx!.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r);
                grad.addColorStop(0, `rgba(${n.color}, 0.03)`);
                grad.addColorStop(0.5, `rgba(${n.color}, 0.015)`);
                grad.addColorStop(1, "rgba(0,0,0,0)");
                ctx!.fillStyle = grad;
                ctx!.beginPath();
                ctx!.arc(n.x, n.y, n.r, 0, Math.PI * 2);
                ctx!.fill();
            });
        }

        // --- MAIN DRAW LOOP ---
        function draw() {
            if (!ctx) return;
            ctx.clearRect(0, 0, w, h);
            const t = performance.now() * 0.001;

            drawNebula();

            const parallaxX = (mouseX - w / 2) * 0.02;
            const parallaxY = (mouseY - h / 2) * 0.02;

            // Draw star layers with parallax
            layers.forEach((layer, li) => {
                const px = parallaxX * (li + 1) * 0.5;
                const py = parallaxY * (li + 1) * 0.5;

                layer.stars.forEach((s) => {
                    const twinkle = (Math.sin(t * s.twinkleSpeed * 60 + s.twinkle) + 1) * 0.5;
                    const alpha = s.baseAlpha * (0.3 + twinkle * 0.7);
                    const sx = ((s.x + px) % w + w) % w;
                    const sy = ((s.y + py) % h + h) % h;

                    ctx!.beginPath();
                    ctx!.arc(sx, sy, s.r, 0, Math.PI * 2);
                    ctx!.fillStyle = `rgba(200, 220, 255, ${alpha})`;
                    ctx!.fill();

                    if (s.r > 1.5 && twinkle > 0.7) {
                        const flareLen = s.r * 4 * twinkle;
                        ctx!.strokeStyle = `rgba(200, 220, 255, ${alpha * 0.3})`;
                        ctx!.lineWidth = 0.3;
                        ctx!.beginPath();
                        ctx!.moveTo(sx - flareLen, sy);
                        ctx!.lineTo(sx + flareLen, sy);
                        ctx!.moveTo(sx, sy - flareLen);
                        ctx!.lineTo(sx, sy + flareLen);
                        ctx!.stroke();
                    }
                });
            });

            drawGlobe(t);

            // Shooting stars
            if (Math.random() < 0.008) {
                shootingStars.push({
                    x: Math.random() * w * 0.6,
                    y: Math.random() * h * 0.3,
                    vx: 6 + Math.random() * 6,
                    vy: 2 + Math.random() * 3,
                    life: 1,
                    decay: 0.008 + Math.random() * 0.008,
                    len: 80 + Math.random() * 60,
                });
            }

            for (let i = shootingStars.length - 1; i >= 0; i--) {
                const ss = shootingStars[i]!;
                ss.x += ss.vx;
                ss.y += ss.vy;
                ss.life -= ss.decay;
                if (ss.life <= 0) { shootingStars.splice(i, 1); continue; }

                const tailX = ss.x - ss.vx * ss.len * 0.15;
                const tailY = ss.y - ss.vy * ss.len * 0.15;
                const g = ctx.createLinearGradient(ss.x, ss.y, tailX, tailY);
                g.addColorStop(0, `rgba(255, 255, 255, ${ss.life})`);
                g.addColorStop(0.3, `rgba(96, 165, 250, ${ss.life * 0.5})`);
                g.addColorStop(1, "rgba(96, 165, 250, 0)");
                ctx.beginPath();
                ctx.moveTo(ss.x, ss.y);
                ctx.lineTo(tailX, tailY);
                ctx.strokeStyle = g;
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.beginPath();
                ctx.arc(ss.x, ss.y, 2, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${ss.life})`;
                ctx.fill();
                ctx.beginPath();
                ctx.arc(ss.x, ss.y, 6, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(96, 165, 250, ${ss.life * 0.15})`;
                ctx.fill();
            }

            // Rockets
            if (Math.random() < 0.002) spawnRocket();

            for (let i = rockets.length - 1; i >= 0; i--) {
                const r = rockets[i]!;
                r.trail.push({ x: r.x, y: r.y, life: 1 });
                r.x += r.vx;
                r.y += r.vy;
                r.life -= 0.003;

                if (r.life <= 0 || r.x < -50 || r.x > w + 50 || r.y < -50) {
                    rockets.splice(i, 1);
                    continue;
                }

                for (let j = r.trail.length - 1; j >= 0; j--) {
                    const tp = r.trail[j]!;
                    tp.life -= 0.025;
                    if (tp.life <= 0) { r.trail.splice(j, 1); continue; }

                    ctx.beginPath();
                    ctx.arc(tp.x, tp.y, r.size * tp.life * 1.5, 0, Math.PI * 2);
                    ctx.fillStyle = `rgba(249, 115, 22, ${tp.life * 0.4})`;
                    ctx.fill();
                }

                ctx.beginPath();
                ctx.arc(r.x, r.y, r.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${r.life})`;
                ctx.fill();
                ctx.beginPath();
                ctx.arc(r.x - r.vx * 2, r.y - r.vy * 2, r.size * 3, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(249, 115, 22, ${r.life * 0.2})`;
                ctx.fill();
            }

            animId = requestAnimationFrame(draw);
        }

        const handleMouseMove = (e: MouseEvent) => {
            const rect = canvas!.getBoundingClientRect();
            mouseX = e.clientX - rect.left;
            mouseY = e.clientY - rect.top;
        };

        const handleResize = () => {
            resize();
            createStarLayers();
            initGlobe();
        };

        canvas.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("resize", handleResize);
        resize();
        createStarLayers();
        initGlobe();
        draw();

        return () => {
            cancelAnimationFrame(animId);
            canvas.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("resize", handleResize);
        };
    }, []);

    useEffect(() => {
        const cleanup = initCanvas();
        return cleanup;
    }, [initCanvas]);

    return canvasRef;
}
