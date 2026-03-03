import { useEffect, useState } from "react";

export default function PageLoader() {
    const [loaded, setLoaded] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setLoaded(true), 800);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className={`page-loader ${loaded ? "loaded" : ""}`} id="pageLoader">
            <div className="loader-content">
                <div className="loader-logo">
                    GEE<span className="accent">.</span>
                </div>
                <div className="loader-bar">
                    <div className="loader-bar-fill"></div>
                </div>
            </div>
        </div>
    );
}
