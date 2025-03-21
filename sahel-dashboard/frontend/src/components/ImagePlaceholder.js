import React, { useState } from "react";

const ImagePlaceholder = ({ selectedFile, onYearDrop }) => {
    const [isDragging, setIsDragging] = useState(false);

    // Drag events
    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        const droppedYear = e.dataTransfer.getData("text/plain");
        if (droppedYear) {
            onYearDrop(droppedYear);
        }
    };

    // Helper: check if file is an HTML file
    const isHtmlFile = selectedFile && selectedFile.endsWith(".html");
    const staticUrl = selectedFile.startsWith("raining_heatmaps/")
  ? `http://127.0.0.1:8000/static/${selectedFile}`
  : `http://127.0.0.1:8000/static/${selectedFile}`;


  console.log("staticUrl", staticUrl);
    return (
        <div 
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            style={{
                flex: 2,
                height: "95%",
                border: "2px solid gray",
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
            }}
        >
            {selectedFile ? (
                isHtmlFile ? (
                    <iframe
                     src={staticUrl}
                        title="HTML Preview"
                        style={{
                            width: "100%",
                            height: "100%",
                            border: "none",
                            borderRadius: "5px",
                        }}
                    />
                ) : (
                    <img 
                        src={`http://127.0.0.1:8000/api/process-tiff/${selectedFile}`} 
                        alt="Selected Raster Data" 
                        onError={(e) => e.target.style.display = "none"} 
                        style={{
                            maxWidth: "100%",
                            maxHeight: "100%",
                            objectFit: "contain",
                            borderRadius: "5px",
                        }}
                    />
                )
            ) : (
                <p style={{ fontSize: "16px", color: "#555" }}>
                    Drag a year here to update the image
                </p>
            )}
        </div>
    );
};

export default ImagePlaceholder;
