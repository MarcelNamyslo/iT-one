import React from "react"; 
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend,
    Title
} from "chart.js";

// Register necessary Chart.js components
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend, Title)

const BarChart = ({ stats, city, placeholder }) => {
    const allYears = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];
    
    const years = allYears;
    const values = years.map(year => (stats && stats[year] != null ? stats[year] : 0));

    const chartData = {
        labels: years,
        datasets: [
            {
                label: `Mean ${placeholder}$ (mm)`,
                data: values,
                backgroundColor: "rgba(54, 162, 235, 0.6)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            title: city ? {  // Display title only if city is known
                display: true,
                text: `Annual Mean ${placeholder}  in ${city}`,
                font: { size: 9 },
            } : { display: false },  // Hide title if city is unknown
            legend: { display: false },
            tooltip: { enabled: true },
        },
        scales: {
            x: {
                title: { display: true, text: "Year", font: { size: 10 } },
                grid: { display: false },
                ticks: { font: { size: 10 } },
            },
            y: {
                grid: { color: "rgba(200, 200, 200, 0.3)" },
                ticks: { beginAtZero: true, font: { size: 10 } },
            },
        },
    };

    return <Bar data={chartData} options={options}  />;
};

export default BarChart;
