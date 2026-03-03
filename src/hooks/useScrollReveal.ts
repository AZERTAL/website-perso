import { useEffect, useRef } from "react";

export function useScrollReveal() {
    const observerRef = useRef<IntersectionObserver | null>(null);

    useEffect(() => {
        observerRef.current = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        // Animate skill bars when parent becomes visible
                        entry.target.querySelectorAll<HTMLElement>(".sb-fill[data-width]").forEach((bar) => {
                            bar.style.width = bar.dataset.width + "%";
                        });
                    }
                });
            },
            { threshold: 0.08, rootMargin: "0px 0px -50px 0px" }
        );

        const els = document.querySelectorAll(".fade-up, .slide-in-left, .scale-in");
        els.forEach((el) => observerRef.current?.observe(el));

        return () => {
            observerRef.current?.disconnect();
        };
    }, []);
}
