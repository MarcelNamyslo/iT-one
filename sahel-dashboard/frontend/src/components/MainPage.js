import React from "react";

const MainPage = ({ children }) => {
    return (
        <div style={{ display: "flex", flexDirection: "column", height: "95vh" }}>
            {/* Title Section */}
            <div style={{
                textAlign: "center",
                fontSize: "17px",
                fontWeight: "bold",
                padding: "5px",
                borderBottom: "2px solid gray",
                
            }}>
                Climate & GIS Data Dashboard
            </div>

            {/* Main Content Section */}
            <div style={{
                height: "98%",
                display: "flex",
                flex: 1,
                padding: "10px",
                margin: "5px",
                boxSizing: "border-box",
                gap: "20px",
                border: "2px solid gray"
            }}>
                {children}
            </div>
        </div>
    );
};

export default MainPage;
