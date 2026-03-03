import { useEffect } from "react";

export default function Ventures() {
    // Tilt effect on venture cards
    useEffect(() => {
        const cards = document.querySelectorAll<HTMLElement>("[data-tilt]");
        const handlers = new Map<HTMLElement, { move: (e: MouseEvent) => void; leave: () => void }>();

        cards.forEach((card) => {
            const move = (e: MouseEvent) => {
                const r = card.getBoundingClientRect();
                const rx = ((e.clientY - r.top - r.height / 2) / r.height) * -6;
                const ry = ((e.clientX - r.left - r.width / 2) / r.width) * 6;
                card.style.transform = `perspective(800px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-8px)`;
            };
            const leave = () => {
                card.style.transform = "";
            };
            card.addEventListener("mousemove", move);
            card.addEventListener("mouseleave", leave);
            handlers.set(card, { move, leave });
        });

        return () => {
            handlers.forEach(({ move, leave }, card) => {
                card.removeEventListener("mousemove", move);
                card.removeEventListener("mouseleave", leave);
            });
        };
    }, []);

    return (
        <section id="ventures">
            <div className="container">
                <div className="section-label fade-up">
                    <span className="label-dot"></span> Ventures
                </div>
                <div className="ventures-grid">
                    <div className="venture-card glass-card fade-up" data-tilt>
                        <span className="intra-data">DAT.01 / APX</span>
                        <div className="vc-header">
                            <span className="vc-badge live">Live</span>
                            <span className="vc-date">Jan 2026 – Present</span>
                        </div>
                        <h3>Apex Scholar</h3>
                        <span className="vc-role">Founder & CTO</span>
                        <p>
                            Apex Scholar is an AI-driven study co-pilot that helps ambitious students structure,
                            memorize, and master course material significantly faster. The platform combines
                            intelligent flashcards, adaptive quizzes, an AI tutor, and learning analytics to
                            optimize retention and track progress over time. It is built for elite and exam-focused
                            learners, providing a centralized workspace to organize content, automate revision, and
                            turn complex material into actionable study plans.
                        </p>
                        <div className="vc-tags">
                            <span>AI/ML</span>
                            <span>EdTech</span>
                            <span>SaaS</span>
                            <span>Product</span>
                        </div>
                        <a href="https://studentify.org" target="_blank" rel="noreferrer" className="vc-link">
                            Visit Website →
                        </a>
                    </div>

                    <div className="venture-card glass-card fade-up d1" data-tilt>
                        <span className="intra-data">DAT.02 / MKF</span>
                        <div className="vc-header">
                            <span className="vc-badge live">Live</span>
                            <span className="vc-date">Oct 2024 – Present</span>
                        </div>
                        <h3>MarketFlow</h3>
                        <span className="vc-role">Founder & CEO</span>
                        <p>
                            Transforming global B2B commerce, MarketFlow connects businesses with trusted suppliers
                            worldwide. Our platform ensures transparent pricing, AI-driven market insights, and a
                            performance-based ranking system for secure and efficient transactions. MarketFlow
                            simplifies procurement, empowering businesses of all sizes to thrive.
                        </p>
                        <div className="vc-tags">
                            <span>AI/ML</span>
                            <span>B2B</span>
                            <span>Supply Chain</span>
                            <span>Platform</span>
                        </div>
                        <a
                            href="https://marketflow-world.com"
                            target="_blank"
                            rel="noreferrer"
                            className="vc-link"
                        >
                            Visit Website →
                        </a>
                    </div>
                </div>
            </div>
        </section>
    );
}
