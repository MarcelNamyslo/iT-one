import React from "react";

const MainPage = ({ children }) => {
    return (
        <div style={{
            display: "flex",
            height: "95vh",
            padding: "10px",
            margin: "15px",
            boxSizing: "border-box",
            gap: "20px",
            border: "2px solid gray"
        }}>
            {children}
        </div>
    );
};

export default MainPage;
