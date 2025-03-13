document.addEventListener("DOMContentLoaded", function () {
    // Uploading data with the chart.
    fetch("/crypto_graph.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("plotly-chart").innerHTML = data;
        });

    // Uploading the analysis text.
    fetch("/analysis.txt")
        .then(response => response.text())
        .then(data => {
            document.getElementById("analysis-text").textContent = data;
        });
});
