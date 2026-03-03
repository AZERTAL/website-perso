export default function Education() {
    return (
        <section id="education">
            <div className="container">
                <div className="section-label fade-up">
                    <span className="label-dot"></span> Education
                </div>
                <div className="edu-timeline">
                    <div className="edu-item fade-up">
                        <div className="edu-year">2025–2029</div>
                        <div className="edu-card">
                            <h3>EADA Business School</h3>
                            <p>Double Degree in Global BBA and Bachelor in AI for Business</p>
                            <span className="edu-location">Barcelona, Spain</span>
                        </div>
                    </div>
                    <div className="edu-item fade-up d1">
                        <div className="edu-year">2025–2029</div>
                        <div className="edu-card">
                            <h3>SKEMA Business School</h3>
                            <p>Global BBA, Business Administration, Management and Operations</p>
                            <span className="edu-location">Barcelona, Spain</span>
                        </div>
                    </div>
                    <div className="edu-item fade-up d2">
                        <div className="edu-year">2024–2025</div>
                        <div className="edu-card">
                            <h3>Al Akhawayn University</h3>
                            <p>Bachelor of Business Administration — GPA 3.5/4.0</p>
                            <p className="edu-highlight">President of NextGen Business Club (Over 150 members)</p>
                            <span className="edu-location">Ifrane, Morocco</span>
                        </div>
                    </div>
                    <div className="edu-item fade-up d3">
                        <div className="edu-year">2024–2025</div>
                        <div className="edu-card">
                            <h3>Founder Institute</h3>
                            <p>Entrepreneur in Acceleration Program (STARTUP)</p>
                            <p style={{ marginTop: 12, fontSize: "0.85rem" }}>
                                Selected for the Founder Institute Pre-Acceleration Program, one of the world's most
                                prestigious startup incubators. Refining the MarketFlow business model—a B2B platform
                                revolutionizing the construction industry with AI-powered pricing, supplier trust
                                rankings, and smart negotiation tools. Engaging with top-tier mentors, investors, and
                                fellow entrepreneurs to accelerate growth and optimize the go-to-market strategy.
                                Structuring the roadmap for fundraising, product development, and international
                                expansion.
                            </p>
                            <span className="edu-location" style={{ display: "block", marginTop: 12 }}>
                                Global
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
