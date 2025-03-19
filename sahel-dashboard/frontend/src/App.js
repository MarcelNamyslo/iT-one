import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/data/")
            .then(response => setData(response.data))
            .catch(error => console.error("Fehler:", error));
    }, []);

    return (
        <div>
            <h1>Sahara-Ausbreitung Dashboard</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th>Datum</th>
                        <th>Region</th>
                        <th>Expansionsrate (km²/Jahr)</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((entry) => (
                        <tr key={entry.id}>
                            <td>{entry.date}</td>
                            <td>{entry.region}</td>
                            <td>{entry.expansion_rate}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;
