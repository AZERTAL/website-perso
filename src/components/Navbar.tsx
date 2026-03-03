import { useEffect, useRef, useState, useCallback } from "react";

const NAV_LINKS = [
    { href: "#about", label: "About" },
    { href: "#ventures", label: "Ventures" },
    { href: "#experience", label: "Experience" },
    { href: "#skills", label: "Skills" },
    { href: "#contact", label: "Contact" },
];

export default function Navbar() {
    const [hidden, setHidden] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);
    const [activeLink, setActiveLink] = useState("");
    const lastScrollRef = useRef(0);

    const handleSmoothScroll = useCallback((e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
        setMobileOpen(false);
        document.body.style.overflow = "";
    }, []);

    const toggleMobile = useCallback(() => {
        setMobileOpen((prev) => {
            document.body.style.overflow = !prev ? "hidden" : "";
            return !prev;
        });
    }, []);

    useEffect(() => {
        const handleScroll = () => {
            const cur = window.scrollY;
            if (cur > 200) {
                if (cur > lastScrollRef.current + 5) setHidden(true);
                else if (cur < lastScrollRef.current - 5) setHidden(false);
            } else {
                setHidden(false);
            }
            lastScrollRef.current = cur;
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    // Active nav tracking
    useEffect(() => {
        const sections = document.querySelectorAll("section[id]");
        const observers: IntersectionObserver[] = [];

        sections.forEach((sec) => {
            const obs = new IntersectionObserver(
                (entries) => {
                    if (entries[0]?.isIntersecting) {
                        setActiveLink(`#${sec.id}`);
                    }
                },
                { threshold: 0.25, rootMargin: "-80px 0px -50% 0px" }
            );
            obs.observe(sec);
            observers.push(obs);
        });

        return () => observers.forEach((obs) => obs.disconnect());
    }, []);

    return (
        <>
            <nav className={`nav ${hidden ? "hidden" : ""}`} id="navbar">
                <div className="nav-inner">
                    <div className="nav-logo">
                        GEE<span className="accent">.</span>
                    </div>
                    <div className="nav-links">
                        {NAV_LINKS.map((link) => (
                            <a
                                key={link.href}
                                href={link.href}
                                className={activeLink === link.href ? "active" : ""}
                                onClick={(e) => handleSmoothScroll(e, link.href)}
                            >
                                {link.label}
                            </a>
                        ))}
                    </div>
                    <div
                        className={`nav-hamburger ${mobileOpen ? "active" : ""}`}
                        id="hamburger"
                        onClick={toggleMobile}
                    >
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </nav>

            <div className={`mobile-nav ${mobileOpen ? "open" : ""}`} id="mobileNav">
                {NAV_LINKS.map((link) => (
                    <a key={link.href} href={link.href} onClick={(e) => handleSmoothScroll(e, link.href)}>
                        {link.label}
                    </a>
                ))}
            </div>
        </>
    );
}
