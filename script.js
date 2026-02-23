let chart;
let soilData = [];
let labels = [];

function fetchData() {
    fetch("/get_data")
    .then(response => response.json())
    .then(data => {

        document.getElementById("soilValue").innerText = data.soil + "%";
        document.getElementById("tempValue").innerText = data.temp + "°C";
        document.getElementById("statusValue").innerText = data.status;

        soilData.push(data.soil);
        labels.push(labels.length + 1);

        updateChart();
    });
}

function updateChart(){
    const ctx = document.getElementById("chart");

    if(chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Soil Moisture %",
                data: soilData,
                borderColor: "green"
            }]
        }
    });
}

fetchData();
setInterval(fetchData, 3000);