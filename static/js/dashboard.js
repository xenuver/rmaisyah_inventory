// ── Dashboard Charts (Chart.js) ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

    // ── Stock Trend (Line Chart) ─────────────────────────────────────
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        const labels = JSON.parse(trendCtx.dataset.labels || '[]');
        const masuk = JSON.parse(trendCtx.dataset.masuk || '[]');
        const keluar = JSON.parse(trendCtx.dataset.keluar || '[]');

        // Format date labels
        const formattedLabels = labels.map(d => {
            const date = new Date(d);
            return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' });
        });

        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: formattedLabels,
                datasets: [
                    {
                        label: 'Barang Masuk',
                        data: masuk,
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        borderWidth: 2.5,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 6,
                    },
                    {
                        label: 'Barang Keluar',
                        data: keluar,
                        borderColor: '#DC2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.1)',
                        borderWidth: 2.5,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 6,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { intersect: false, mode: 'index' },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: { family: 'Karla', size: 13 }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Karla', size: 11 } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0,0,0,0.05)' },
                        ticks: { font: { family: 'Karla', size: 11 } }
                    }
                }
            }
        });
    }

    // ── Category Breakdown (Doughnut Chart) ──────────────────────────
    const kategoriCtx = document.getElementById('kategoriChart');
    if (kategoriCtx) {
        const labels = JSON.parse(kategoriCtx.dataset.labels || '[]');
        const values = JSON.parse(kategoriCtx.dataset.values || '[]');

        const colors = [
            '#7C3AED', '#F97316', '#059669', '#2563EB',
            '#EC4899', '#14B8A6', '#8B5CF6', '#F59E0B',
            '#6366F1', '#EF4444'
        ];

        new Chart(kategoriCtx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#FFFFFF',
                    hoverOffset: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 16,
                            font: { family: 'Karla', size: 12 }
                        }
                    }
                }
            }
        });
    }
});
