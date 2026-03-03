export default function Skills() {
    return (
        <section id="skills">
            <div className="container">
                <div className="section-label fade-up">
                    <span className="label-dot"></span> Skills & Competencies
                </div>
                <div className="skills-layout">
                    <div className="skills-group fade-up">
                        <h3>Strategy & Business</h3>
                        <div className="skill-bars">
                            <SkillBar label="Entrepreneurship & Strategy" pct={95} />
                            <SkillBar label="Growth Marketing" pct={90} />
                            <SkillBar label="Market Expansion" pct={85} />
                            <SkillBar label="Negotiation" pct={85} />
                        </div>
                    </div>
                    <div className="skills-group fade-up d1">
                        <h3>Technology & Product</h3>
                        <div className="skill-bars">
                            <SkillBar label="AI Product Development" pct={90} />
                            <SkillBar label="Performance Advertising" pct={88} />
                            <SkillBar label="Data-Driven Decision Making" pct={85} />
                            <SkillBar label="Process Optimization" pct={80} />
                        </div>
                    </div>
                    <div className="skills-group fade-up d2">
                        <h3>Languages</h3>
                        <div className="skill-bars">
                            <SkillBar label="French" pct={100} level="Native" />
                            <SkillBar label="Arabic" pct={100} level="Native" />
                            <SkillBar label="English" pct={92} level="C2" />
                            <SkillBar label="Spanish" pct={30} level="A2" />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

function SkillBar({ label, pct, level }: { label: string; pct: number; level?: string }) {
    return (
        <div className="skill-bar-item">
            <div className="sb-top">
                <span>{label}</span>
                <span>{level || `${pct}%`}</span>
            </div>
            <div className="sb-track">
                <div className="sb-fill" data-width={pct}></div>
            </div>
        </div>
    );
}
