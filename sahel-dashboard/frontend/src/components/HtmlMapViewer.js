import React, { useEffect, useState } from "react";
import axios from "axios";

const HtmlMapViewer = ({ onYearSelect, minYear = 2010, maxYear = 2024, selectedYear, onDataTypeSelect }) => {
    const [htmlFiles, setHtmlFiles] = useState([]);
    const [selectedHtml, setSelectedHtml] = useState("districts_heatmap_2010.html");

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/html-maps/")
            .then(response => setHtmlFiles(response.data.html_maps))
            .catch(error => console.error("❌ Error fetching HTML maps:", error));
    }, []);

    const extractYearFromFilename = (filename) => {
        const match = filename.match(/(\d{4})/);
        return match ? match[1] : null;
    };

    useEffect(() => {
        if (selectedYear && htmlFiles.length > 0) {
            const matchedHtml = htmlFiles.find(file => extractYearFromFilename(file) === selectedYear);
            setSelectedHtml(matchedHtml || null);
        }
    }, [selectedYear, htmlFiles]);

    const handleSliderChange = (e) => {
        const newYear = e.target.value;
        onYearSelect(newYear);
    };

    return (
        <div style={{margin: "15px", width: "100%", height: "93%", alignItems: "center", justifyContent: "center" }}>
            {selectedHtml && (
                <iframe
                    title="HTML Map"
                    src={`http://127.0.0.1:8000/static/${selectedHtml}`}
                    style={{ width: "95%", height: "92%", border: "none" }}
                />
            )}

            <div style={{ justifyContent: "center" }}>
                <h4 style={{ color: "black", marginBottom: "3px", fontSize: "10px",  textAlign: "center" }}>
                    Selected Year: {selectedYear}
                </h4>

                <input
                    type="range"
                    min={minYear}
                    max={maxYear}
                    step={1}
                    value={selectedYear}
                    onChange={handleSliderChange}
                    style={{
                        width: "90%",
                        appearance: "none",
                        background: "black",
                        height: "8px",
                        borderRadius: "5px",
                        outline: "none",
                        cursor: "pointer",
                        margin: "1px",
                    }}
                />
            </div>
        </div>
    );
};


export default HtmlMapViewer;
