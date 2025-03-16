document.addEventListener("DOMContentLoaded", function () {
    // Loading the chart
    fetch("crypto_chart.html")
        .then(response => {
            if (!response.ok) {
                throw new Error("Chart loading error");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("plotly-chart").innerHTML = data;
        })
        .catch(error => {
            console.error(error);
            document.getElementById("plotly-chart").innerHTML = "<p>Chart loading error</p>";
        });

    // Loading the analysis text
    fetch("analysis.txt")
        .then(response => {
            if (!response.ok) {
                throw new Error("Analysis loading error");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("analysis-text").textContent = data;
        })
        .catch(error => {
            console.error(error);
            document.getElementById("analysis-text").textContent = "Analysis loading error";
        });
});
