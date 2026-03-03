export default function Contact() {
    return (
        <section id="contact">
            <div className="container">
                <div className="section-label fade-up">
                    <span className="label-dot"></span> Let's Connect
                </div>
                <div className="contact-block fade-up">
                    <h2>Interested in working together?</h2>
                    <p>
                        I'm always open to discussing new ventures, collaborations, and opportunities. Feel free
                        to reach out.
                    </p>
                    <div className="contact-links">
                        <a href="mailto:geleulj@gmail.com" className="contact-card glass-card">
                            <span className="contact-icon">✉</span>
                            <span className="contact-type">Email</span>
                            <span className="contact-value">geleulj@gmail.com</span>
                            <span className="contact-arrow">→</span>
                        </a>
                        <a
                            href="https://linkedin.com/in/ghali"
                            target="_blank"
                            rel="noreferrer"
                            className="contact-card glass-card"
                        >
                            <span className="contact-icon">in</span>
                            <span className="contact-type">LinkedIn</span>
                            <span className="contact-value">linkedin.com/in/ghali</span>
                            <span className="contact-arrow">→</span>
                        </a>
                    </div>
                </div>
            </div>
        </section>
    );
}
