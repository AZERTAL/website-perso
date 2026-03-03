const TECH_ITEMS = [
    "Python", "React", "Next.js", "Node.js", "Supabase", "TypeScript",
    "TailwindCSS", "Bubble.io", "OpenAI API", "Figma", "Vercel", "Stripe",
    "Meta Ads", "Google Analytics",
];

export default function TechMarquee() {
    return (
        <section className="marquee-section">
            <div className="marquee-track">
                {[...TECH_ITEMS, ...TECH_ITEMS].map((item, i) => (
                    <span className="marquee-item" key={i}>
                        <span className="mi-dot"></span>
                        {item}
                    </span>
                ))}
            </div>
        </section>
    );
}
