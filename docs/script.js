document.addEventListener("DOMContentLoaded", function () {
    // Загружаем график
    fetch("crypto_chart.html")
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка загрузки графика");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("plotly-chart").innerHTML = data;
        })
        .catch(error => {
            console.error(error);
            document.getElementById("plotly-chart").innerHTML = "<p>Ошибка загрузки графика</p>";
        });

    // Загружаем текст анализа
    fetch("analysis.txt")
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка загрузки анализа");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("analysis-text").textContent = data;
        })
        .catch(error => {
            console.error(error);
            document.getElementById("analysis-text").textContent = "Ошибка загрузки анализа";
        });
});
