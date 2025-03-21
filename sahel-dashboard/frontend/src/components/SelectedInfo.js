import React, { useEffect, useState } from "react";

const SelectedInfo = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const handleMessage = (event) => {
            console.log("📡 Received event:", event.data);

            if (event.data?.type === "mapDataClicked") {
                console.log("🟢 Updating state with backend response:", event.data.payload);
                setData(event.data.payload);
            }
        };

        window.addEventListener("message", handleMessage);

        return () => {
            window.removeEventListener("message", handleMessage);
        };
    }, []);

    return (
        <div style={{ border: "2px solid gray", padding: "10px", width: "250px" }}>
            <h3 style={{ fontSize: "12px" }}>Selected Region Info</h3>
            {data ? (
                <>
                    <p style={{ fontSize: "10px" }}><strong>Message:</strong> {data.message}</p>

                    {/* 🔥 Fix: Properly iterate over `stats` and display the data */}
                    <h4 style={{ fontSize: "10px" }}>Precipitation Stats:</h4>
                    <ul style={{ fontSize: "10px", paddingLeft: "15px" }}>
                        {Object.entries(data.stats).map(([year, value]) => (
                            <li key={year}><strong>{year}:</strong> {value.toFixed(2)} mm</li>
                        ))}
                    </ul>
                </>
            ) : (
                <p style={{ fontSize: "10px" }}>No data selected.</p>
            )}
        </div>
    );
};

export default SelectedInfo;
