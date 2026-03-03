import { useEffect, useRef } from "react";
import { useHeroCanvas } from "@/hooks/useHeroCanvas";

export default function Hero() {
    const canvasRef = useHeroCanvas();
    const nameRef = useRef<HTMLHeadingElement>(null);
    const glowRef = useRef<HTMLDivElement>(null);

    // Letter-by-letter reveal
    useEffect(() => {
        const el = nameRef.current;
        if (!el) return;
        const text = el.textContent || "";
        el.textContent = "";
        el.style.opacity = "1";
        text.split("").forEach((char, i) => {
            const span = document.createElement("span");
            span.className = "char";
            span.textContent = char === " " ? "\u00A0" : char;
            span.style.animationDelay = `${i * 0.04 + 0.3}s`;
            el.appendChild(span);
        });
    }, []);

    // Counter animation
    useEffect(() => {
        const counters = document.querySelectorAll<HTMLElement>("[data-count]");
        const observers: IntersectionObserver[] = [];

        counters.forEach((el) => {
            const cObs = new IntersectionObserver(
                (entries) => {
                    if (entries[0]?.isIntersecting) {
                        const target = parseInt(el.dataset.count || "0");
                        const start = Date.now();
                        (function animate() {
                            const p = Math.min((Date.now() - start) / 1800, 1);
                            const eased = 1 - Math.pow(1 - p, 4);
                            el.textContent = Math.round(target * eased) + (target > 10 ? "+" : "");
                            if (p < 1) requestAnimationFrame(animate);
                        })();
                        cObs.unobserve(el);
                    }
                },
                { threshold: 0.5 }
            );
            cObs.observe(el);
            observers.push(cObs);
        });

        return () => observers.forEach((obs) => obs.disconnect());
    }, []);

    // Parallax glow
    useEffect(() => {
        const handleScroll = () => {
            const s = window.scrollY;
            if (glowRef.current && s < window.innerHeight) {
                glowRef.current.style.transform = `translateY(${s * 0.3}px) scale(${1 + s * 0.0003})`;
            }
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <section className="hero" id="hero">
            <canvas className="hero-canvas" id="heroCanvas" ref={canvasRef}></canvas>
            <div className="hero-glow" ref={glowRef}></div>

            <div className="container hero-split">
                <div className="hero-left">
                    <div className="hero-welcome fade-up">
                        <span className="tag-pill">📍 Based in Barcelona, Spain</span>
                    </div>
                    <h1 className="hero-name" ref={nameRef}>
                        Ghali El Eulj
                    </h1>
                    <p className="hero-tagline fade-up d2">
                        Student & Tech Entrepreneur<span className="typing-cursor"></span>
                    </p>
                    <p className="hero-desc fade-up d3">
                        AI & Business double-degree student building scalable ventures at the intersection of
                        artificial intelligence, education, and market systems. Founder of two active startups
                        before 20.
                    </p>

                    <div className="hero-ctas fade-up d4">
                        <a href="#ventures" className="btn-primary">
                            View Ventures
                        </a>
                        <a href="mailto:geleulj@gmail.com" className="btn-outline">
                            Get in Touch →
                        </a>
                    </div>
                </div>

                <div className="hero-right fade-up d3">
                    <div className="orbit-system">
                        <div className="orbit-ring orbit-ring-1">
                            <div className="orbit-dot"></div>
                        </div>
                        <div className="orbit-ring orbit-ring-2">
                            <div className="orbit-dot orbit-dot-2"></div>
                        </div>
                        <div className="orbit-ring orbit-ring-3">
                            <div className="orbit-dot orbit-dot-3"></div>
                        </div>
                        <div className="orbit-core">
                            <span className="orbit-label">GEE</span>
                        </div>
                        <div className="orbit-tag ot-1">AI/ML</div>
                        <div className="orbit-tag ot-2">EdTech</div>
                        <div className="orbit-tag ot-3">B2B</div>
                        <div className="orbit-tag ot-4">SaaS</div>
                    </div>
                </div>
            </div>

            <div className="container">
                <div className="hero-stats fade-up d5">
                    <div className="stat">
                        <span className="stat-num" data-count="2">0</span>
                        <span className="stat-label">Active Startups</span>
                    </div>
                    <div className="stat">
                        <span className="stat-num">6-fig</span>
                        <span className="stat-label">Revenue Scaled</span>
                    </div>
                    <div className="stat">
                        <span className="stat-num" data-count="100">0</span>
                        <span className="stat-label">Club Members Built</span>
                    </div>
                    <div className="stat">
                        <span className="stat-num" data-count="4">0</span>
                        <span className="stat-label">Languages Spoken</span>
                    </div>
                </div>
            </div>
        </section>
    );
}
