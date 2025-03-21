import React, { useState } from "react";

const dataTypes = [
    { name: "Modis Land Cover Data", folder: "Modis_Land_Cover_Data" },
    { name: "Modis Gross Primary Production (GPP)", folder: "MODIS_Gross_Primary_Production_GPP" },
    { name: "Climate Precipitation Data", folder: "Climate_Precipitation_Data" },
    { name: "Gridded Population Density Data", folder: "Gridded_Population_Density_Data" }
];

const YearSlider = ({ onYearSelect, minYear = 2010, maxYear = 2023, selectedYear, onDataTypeSelect }) => {
    const [year, setYear] = useState(selectedYear || minYear);
    const [selectedDataType, setSelectedDataType] = useState(null);

    const handleSliderChange = (event) => {
        const newYear = event.target.value;
        setYear(newYear);
        onYearSelect(newYear);
    };

    const handleDataTypeSelect = (folder) => {
        setSelectedDataType(folder);
        onDataTypeSelect(folder);
    };

    return (
        <div style={{ 
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            height: "100%",
            overflow: "hidden",
            justifyContent: "space-between",
        }}>
            
            {/* Vertical Scrollable Buttons */}
            <div style={{
                display: "flex",
                flexDirection: "column",
                maxHeight: "100px",
                width: "100%"
            }}>
                {dataTypes.map((dataType, index) => (
                    <button
                        key={index}
                        onClick={() => handleDataTypeSelect(dataType.folder)}
                        style={{
                            padding: "4px",
                            marginBottom: "2px",
                            width: "100%",
                            backgroundColor: selectedDataType === dataType.folder ? "black" : "white",
                            color: selectedDataType === dataType.folder ? "white" : "black",
                            border: "2px solid black",
                            borderRadius: "5px",
                            cursor: "pointer",
                            transition: "0.3s",
                            fontSize: "8px",
                            marginBottom: "6px"
                        }}
                    >
                        {dataType.name}
                    </button>
                ))}
            </div>
            <div> 
            {/* Selected Year Display */}
            {/* <h4 style={{ color: "black", marginBottom: "3px", fontSize: "10px" }}>Selected Year: {year}</h4> */}

            {/* Year Slider */}
            {/* <input
                type="range"
                min={minYear}
                max={maxYear}
                step={1}
                value={year}
                onChange={handleSliderChange}
                style={{
                    width: "90%",
                    appearance: "none",
                    background: "black", // Slider track
                    height: "8px",
                    borderRadius: "5px",
                    outline: "none",
                    cursor: "pointer",
                    margin: "1px",
                }}
            /> */}
            </div>
            <style>
                {`
                input[type="range"]::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    appearance: none;
                    width: 15px;
                    height: 15px;
                    background: white; /* White slider dot */
                    border-radius: 50%;
                    cursor: pointer;
                    border: 2px solid black;
                }
                input[type="range"]::-moz-range-thumb {
                    width: 15px;
                    height: 15px;
                    background: white; /* White slider dot */
                    border-radius: 50%;
                    cursor: pointer;
                    border: 2px solid black;
                }
                `}
            </style>
        </div>
    );
};

export default YearSlider;
