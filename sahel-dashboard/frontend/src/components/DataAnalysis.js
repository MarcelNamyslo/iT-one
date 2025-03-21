import React, { useEffect, useState } from "react";
import BarChart from "./BarChart"; // Import the BarChart component

const DataAnalysis = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const handleMessage = (event) => {
            // Check for our message type
            if (event.data?.type === "mapDataClicked") {
                console.log("🟢 Map Click Detected in React:", event.data.payload);
                setData(event.data.payload);
            }
        };

        window.addEventListener("message", handleMessage);
        return () => {
            window.removeEventListener("message", handleMessage);
        };
    }, []);

    return (
        <div style={{
            flex: 1,
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)", // 3 equal columns
            gridTemplateRows: "1fr", // 1 row
            gap: "10px",
            paddingTop: "10px",
            height: "250px", // Adjust as needed
        }}>
            {/* First Box: Bar Chart using stats from backend */}
            <div style={{
                border: "2px solid gray",
                height: "100%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
            }}>
                <BarChart stats={data ? data.stats : {}} city={data ? data.city : ""} />
            </div>

            {/* Second Box: List of the raw statistics
            <div style={{
                border: "2px solid gray",
                height: "100%",
                overflowY: "auto",
                padding: "10px"
            }}>
                {data && data.stats ? (
                    <ul>
                        {Object.entries(data.stats).map(([year, value]) => (
                            <li key={year}><strong>{year}:</strong> {value.toFixed(2)} mm</li>
                        ))}
                    </ul>
                ) : (
                    <p>No stats available.</p>
                )}
            </div> */}

            {/* Third Box: You can place any other analysis or leave empty */}
            <div style={{ border: "2px solid gray", height: "100%" }}>
                {/* Additional content */}
            </div>
        </div>
    );
};

export default DataAnalysis;
