import React, { useEffect, useState } from "react";
import axios from "axios";

const HtmlMapViewer = ({ selectedYear }) => {
    const [htmlFiles, setHtmlFiles] = useState([]);
    const [selectedHtml, setSelectedHtml] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/html-maps/")
            .then(response => {
                setHtmlFiles(response.data.html_maps);
            })
            .catch(error => console.error("❌ Error fetching HTML maps:", error));
    }, []);

    // Extract year from filename
    const extractYearFromFilename = (filename) => {
        const match = filename.match(/(\d{4})/);
        return match ? match[1] : null;
    };

    useEffect(() => {
        if (selectedYear && htmlFiles.length > 0) {
            // Find the first file that contains the selected year
            const matchedHtml = htmlFiles.find(file => extractYearFromFilename(file) === selectedYear);

            if (matchedHtml) {
                setSelectedHtml(matchedHtml);
            } else {
                setSelectedHtml(null); // Clear if no match
            }
        }
    }, [selectedYear, htmlFiles]);

    return (
        <div style={{ width: "98%", height: "98%", alignItems: "center", justifyContent: "center" }}>
            <select
                onChange={(e) => setSelectedHtml(e.target.value)}
                value={selectedHtml || ""}
                style={{ margin: "10px", width: "90%", padding: "5px" }}
            >
                {htmlFiles.length === 0 ? (
                    <option>No maps available</option>
                ) : (
                    htmlFiles.map((file, index) => (
                        <option key={index} value={file}>{file}</option>
                    ))
                )}
            </select>

            {selectedHtml && (
                <iframe
                    title="HTML Map"
                    src={`http://127.0.0.1:8000/static/${selectedHtml}`}
                    style={{ width: "95%", height: "92%", border: "none" }}
                />
            )}
        </div>
    );
};

export default HtmlMapViewer;
