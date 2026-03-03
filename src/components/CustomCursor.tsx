import { useEffect, useRef } from "react";

export default function CustomCursor() {
    const dotRef = useRef<HTMLDivElement>(null);
    const ringRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const dot = dotRef.current;
        const ring = ringRef.current;
        if (!dot || !ring) return;

        let cx = -100,
            cy = -100,
            rx = -100,
            ry = -100;
        let animId: number;

        const handleMouseMove = (e: MouseEvent) => {
            cx = e.clientX;
            cy = e.clientY;
        };

        function updateCursor() {
            dot!.style.left = cx - 3 + "px";
            dot!.style.top = cy - 3 + "px";
            rx += (cx - rx) * 0.12;
            ry += (cy - ry) * 0.12;
            ring!.style.left = rx - 18 + "px";
            ring!.style.top = ry - 18 + "px";
            animId = requestAnimationFrame(updateCursor);
        }

        document.addEventListener("mousemove", handleMouseMove);
        updateCursor();

        // Hover effects on interactive elements
        const interactiveEls = document.querySelectorAll(
            "a, button, .btn-primary, .btn-outline, .venture-card, .contact-card, .stat, .ach-item, .detail-card, .edu-item, .exp-item, .skill-bar-item"
        );

        const addHover = () => ring.classList.add("hover");
        const removeHover = () => ring.classList.remove("hover");

        interactiveEls.forEach((el) => {
            el.addEventListener("mouseenter", addHover);
            el.addEventListener("mouseleave", removeHover);
        });

        return () => {
            cancelAnimationFrame(animId);
            document.removeEventListener("mousemove", handleMouseMove);
            interactiveEls.forEach((el) => {
                el.removeEventListener("mouseenter", addHover);
                el.removeEventListener("mouseleave", removeHover);
            });
        };
    }, []);

    return (
        <>
            <div className="cursor-dot" ref={dotRef}></div>
            <div className="cursor-ring" ref={ringRef}></div>
        </>
    );
}
