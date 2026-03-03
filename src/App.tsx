import { useEffect } from "react";
import { useScrollReveal } from "@/hooks/useScrollReveal";
import PageLoader from "@/components/PageLoader";
import GrainOverlay from "@/components/GrainOverlay";
import ScrollProgress from "@/components/ScrollProgress";
import CustomCursor from "@/components/CustomCursor";
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import TechMarquee from "@/components/TechMarquee";
import About from "@/components/About";
import Education from "@/components/Education";
import Ventures from "@/components/Ventures";
import Experience from "@/components/Experience";
import Projects from "@/components/Projects";
import Certifications from "@/components/Certifications";
import Achievements from "@/components/Achievements";
import Skills from "@/components/Skills";
import Contact from "@/components/Contact";
import Footer from "@/components/Footer";
import BackToTop from "@/components/BackToTop";

export default function App() {
    useScrollReveal();

    // Magnetic buttons
    useEffect(() => {
        const btns = document.querySelectorAll<HTMLElement>(".btn-primary, .btn-outline");
        const handlers = new Map<HTMLElement, { move: (e: MouseEvent) => void; leave: () => void }>();

        btns.forEach((btn) => {
            const move = (e: MouseEvent) => {
                const r = btn.getBoundingClientRect();
                const x = e.clientX - r.left - r.width / 2;
                const y = e.clientY - r.top - r.height / 2;
                btn.style.transform = `translate(${x * 0.25}px, ${y * 0.25}px)`;
            };
            const leave = () => {
                btn.style.transform = "";
            };
            btn.addEventListener("mousemove", move);
            btn.addEventListener("mouseleave", leave);
            handlers.set(btn, { move, leave });
        });

        return () => {
            handlers.forEach(({ move, leave }, btn) => {
                btn.removeEventListener("mousemove", move);
                btn.removeEventListener("mouseleave", leave);
            });
        };
    }, []);

    return (
        <>
            <PageLoader />
            <GrainOverlay />
            <ScrollProgress />
            <CustomCursor />
            <Navbar />
            <main>
                <Hero />
                <TechMarquee />
                <About />
                <Education />
                <Ventures />
                <Experience />
                <Projects />
                <Certifications />
                <Achievements />
                <Skills />
                <Contact />
            </main>
            <Footer />
            <BackToTop />
        </>
    );
}
