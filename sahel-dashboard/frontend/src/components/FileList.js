import React, { useEffect, useState } from "react";
import axios from "axios";

const FileList = ({ onFileSelect, isHidden, toggleList }) => {
    const [files, setFiles] = useState([]);
    const [files1, setFiles1] = useState([]);
    const [showFiles1, setShowFiles1] = useState(false);  // 🔄 Toggle between lists

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/files/")
            .then(response => {
                setFiles(response.data.files || []);
                setFiles1(response.data.files1 || []);
            })
            .catch(error => console.error("Error fetching files:", error));
    }, []);

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            position: "relative",
            height: "100%",
        }}>
            <div style={{
                width: isHidden ? "0px" : "170px",
                height: "86.5vh",
                overflowY: "auto",
                border: isHidden ? "none" : "2px solid grey",
                padding: isHidden ? "0px" : "10px",
                fontSize: "0.4em",
                transition: "width 0.3s ease-in-out",
                whiteSpace: "nowrap",
                position: "relative",
                backgroundColor: "white",
                scrollbarWidth: "none",
                msOverflowStyle: "none"
            }}>
                {!isHidden && (
                    <div>
                        <h3>{showFiles1 ? "HTML Maps" : "Available Tifs"}</h3>

                        {/* 🔘 Toggle Button */}
                        <button
                            onClick={() => setShowFiles1(!showFiles1)}
                            style={{
                                marginBottom: "8px",
                                fontSize: "0.5em",
                                padding: "5px 10px",
                                backgroundColor: showFiles1 ? "black" : "white",
                                color: showFiles1 ? "white" : "black",
                                border: "1px solid black",
                                borderRadius: "5px",
                                cursor: "pointer",
                                transition: "0.2s"
                            }}
                        >
                            {showFiles1 ? "Show Files" : "Show HTML"}
                        </button>

                        <ul style={{ listStyle: "none", padding: 0 }}>
                            {(showFiles1 ? files1 : files).map((file, index) => (
                                <li key={index}
                                    onClick={() => onFileSelect(file)}
                                    style={{
                                        cursor: "pointer",
                                        marginBottom: "5px",
                                        overflowWrap: "break-word"
                                    }}
                                >
                                    {file}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Sidebar Collapse Button */}
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
