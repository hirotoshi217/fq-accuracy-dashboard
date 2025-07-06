function createChart(canvasId, label, labels, predData, actualData) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { label: '予想', data: predData, borderWidth: 2 },
        { label: '実績', data: actualData, borderWidth: 2 }
      ]
    },
    options: {
      scales: { y: { beginAtZero: false } }
    }
  });
}