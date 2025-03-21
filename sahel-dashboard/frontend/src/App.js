import React, { useState, useEffect } from "react";
import axios from "axios";
import MainPage from "./components/MainPage";
import FileList from "./components/FileList";
import ImagePlaceholder from "./components/ImagePlaceholder";
import DataAnalysis from "./components/DataAnalysis";
import YearScroller from "./components/YearScroller";
import YearSlider from "./components/YearSlider";
import HtmlMapViewer from "./components/HtmlMapViewer";
import SelectedInfo from "./components/SelectedInfo"
//import colors from "../theme/colors";
function App() {
    const [availableFiles, setAvailableFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState("Climate_Precipitation_Data/2010R.tif");
    const [selectedYear, setSelectedYear] = useState(null);
    const [selectedDataType, setSelectedDataType] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [isFileListHidden, setIsFileListHidden] = useState(false);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/files/")
            .then(response => setAvailableFiles(response.data.files))
            .catch(error => console.error("Error fetching files:", error));
    }, []);

    const extractYearFromFilename = (filename) => {
        const match = filename.match(/(\d{4})/);
        return match ? match[1] : null;
    };

    const extractBaseFilename = (filename) => {
        return filename.replace(/\d{4}/, "{YEAR}"); // Replace year with placeholder
    };

    const handleFileSelect = (filename) => {
        setSelectedFile(filename);
        const extractedYear = extractYearFromFilename(filename);
        setSelectedYear(extractedYear || null);
        setErrorMessage("");
    };

    const handleYearSelect = (year) => {
        setSelectedYear(year);
        if (selectedDataType) {
            updateSelectedFile(selectedDataType, year);
        } else if (selectedFile) {
            // Try updating based on the currently selected file if no dataset is chosen yet
            const baseFilename = extractBaseFilename(selectedFile);
            const newFilename = baseFilename.replace("{YEAR}", year);
            if (availableFiles.includes(newFilename)) {
                setSelectedFile(newFilename);
                setErrorMessage("");
            } else {
                setErrorMessage(`No data for the year ${year} available`);
            }
        }
    };

    const handleYearDrop = (droppedYear) => {
        setSelectedYear(droppedYear);
        if (selectedDataType) {
            updateSelectedFile(selectedDataType, droppedYear);
        }
    };

    const handleDataTypeSelect = (folder) => {
        setSelectedDataType(folder);
        if (selectedYear) {
            updateSelectedFile(folder, selectedYear);
        }
    };

    const updateSelectedFile = (folder, year) => {
        // Find a file that belongs to the selected folder and contains the year
        const matchedFile = availableFiles.find(file =>
            file.startsWith(folder) && file.includes(year)
        );
    
        if (matchedFile) {
            setSelectedFile(matchedFile);
            setErrorMessage("");  // Remove error from frontend
        } else {
            // Show system alert without modifying frontend state
            window.alert(`No data available for ${folder} in ${year}`);
        }
    };

    const toggleFileList = () => {
        setIsFileListHidden(!isFileListHidden);
    };

    return (
        
        <MainPage>
             
            <FileList 
                onFileSelect={handleFileSelect}
                isHidden={isFileListHidden}
                toggleList={toggleFileList}
            />

<div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
                <YearScroller onYearSelect={handleYearSelect} selectedYear={selectedYear} />
                <div style={{ flex: 1, display: "flex", flexDirection: "row", gap: "3px" }}>
                <div style={{ border: "2px solid gray", width: "50%", alignItems: "center",
            justifyContent: "center",}}> 
                
                <HtmlMapViewer  onYearSelect={handleYearSelect} selectedYear={selectedYear} onDataTypeSelect={handleDataTypeSelect} />

                    
                </div>
                <div style={{ flex: 1, display: "flex", flexDirection: "column" }}> 
                {(
                    <div style={{ display: "flex", flexDirection: "row", width: "100%", height: "40vh", gap: "10px" }}>
                        {/* Image Placeholder (80%) */}
                        <div style={{ flex: 8, border: "2px solid gray", padding: "10px" }}>
                            <ImagePlaceholder selectedFile={selectedFile} onYearDrop={handleYearDrop} />
                        </div>

                        {/* Additional Content Box (20%) */}
                        <div style={{ flex: 2, border: "2px solid gray", padding: "10px" }}>
                            <YearSlider onYearSelect={handleYearSelect} selectedYear={selectedYear} onDataTypeSelect={handleDataTypeSelect} />
                        </div>
                    </div>
                )}

<DataAnalysis />
{/* <div>
            <p>Map Data Dashboard</p>
            <SelectedInfo />
        </div> */}
                </div>
                </div>
            </div>
        </MainPage>
    );
}

export default App;

