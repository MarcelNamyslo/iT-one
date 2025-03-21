import React, { useEffect, useState, useRef } from "react";
import axios from "axios";

const YearScroller = ({ onYearSelect, selectedYear }) => {
    const [years, setYears] = useState([]);
    const scrollContainerRef = useRef(null);

    useEffect(() => {
        const API_URL = "http://127.0.0.1:8000/api/files/";

        axios.get(API_URL)
            .then(response => {
                const files = response.data.files;
                console.log("📂 Retrieved Files:", files);

                if (!files || files.length === 0) {
                    console.warn("⚠️ No files found from API!");
                    return;
                }

                const yearRegex = /(?:^|\/)(\d{4})(?:[^\d]|$)/g;
                const extractedYears = new Set();

                files.forEach(file => {
                    let match;
                    while ((match = yearRegex.exec(file)) !== null) {
                        extractedYears.add(match[1]);
                        console.log(`✅ Extracted Year: ${match[1]} from ${file}`);
                    }
                });

                const sortedYears = [...extractedYears].sort((a, b) => a - b);
                console.log("📅 Final Year List:", sortedYears);

                setYears(sortedYears);
            })
            .catch(error => {
                console.error("❌ Error fetching files:", error);
                console.error("❌ Check if Django server is running.");
            });
    }, []);

    const handleDragStart = (e, year) => {
        e.dataTransfer.setData("text/plain", year); // Store the year as drag data
    };

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            overflowX: "auto",
            padding: "2px 0",
            margin: "2px 0",
            whiteSpace: "nowrap",
            border: "2px solid grey",
            backgroundColor: "white"
        }}>
            {years.map((year) => (
                <button
                    key={year}
                    draggable
                    onDragStart={(e) => handleDragStart(e, year)} // Enable dragging
                    onClick={() => onYearSelect(year)}
                    style={{
                        margin: "4px",
                        padding: "6px 10px",
                        borderRadius: "5px",
                        border: `2px solid ${selectedYear === year ? "black" : "grey"}`,
                        backgroundColor: selectedYear === year ? "#ccc" : "white",
                        cursor: "pointer",
                        transition: "0.3s",
                        fontSize: "8px",
                    }}
                >
                    {year}
                </button>
            ))}
        </div>
    );
};

export default YearScroller;