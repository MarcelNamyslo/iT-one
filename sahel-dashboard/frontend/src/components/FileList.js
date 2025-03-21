import React, { useEffect, useState } from "react"; 
import axios from "axios";

const FileList = ({ onFileSelect, isHidden, toggleList }) => {
    const [files, setFiles] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/files/")
            .then(response => setFiles(response.data.files))
            .catch(error => console.error("Error fetching files:", error));
    }, []);

    return (
        <div style={{ 
            display: "flex",
            alignItems: "center",
            position: "relative",
            height: "100%", // Ensure it takes full height
        }}>
            {/* Sidebar List */}
            <div style={{
                width: isHidden ? "0px" : "170px",
                height: "87vh", // Set height to ensure scrolling
                overflowY: "auto", // Enables vertical scrolling
                border: isHidden ? "none" : "2px solid grey",
                padding: isHidden ? "0px" : "10px",
                fontSize: "0.4em",
                transition: "width 0.3s ease-in-out",
                whiteSpace: "nowrap",
                position: "relative",
                backgroundColor: "white",
            }}>
                {!isHidden && (
                    <div>
                        <h3>Available Files</h3>
                        <ul style={{ listStyle: "none", padding: 0 }}>
                            {files.map((file, index) => (
                                <li key={index}
                                    onClick={() => onFileSelect(file)}
                                    style={{ cursor: "pointer", marginBottom: "5px" }}>
                                    {file}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Toggle Button (Properly aligned) */}
            <button
                onClick={toggleList}
                style={{
                    position: "absolute",
                    right: isHidden ? "-30px" : "-15px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    border: "1px solid grey",
                    borderRadius: "50%",
                    backgroundColor: "white",
                    cursor: "pointer",
                    width: "30px",
                    height: "30px",
                    fontSize: "16px",
                    fontWeight: "bold",
                    zIndex: 10,
                    transition: "right 0.3s ease-in-out"
                }}
            >
                 {isHidden ? "»" : "«"}
            </button>
        </div>
    );
};

export default FileList;
