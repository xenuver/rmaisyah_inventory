// ── Dashboard Charts (Chart.js) ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

    Chart.defaults.font.family = "'Inter', sans-serif";

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
            type: 'bar',
            data: {
                labels: formattedLabels,
                datasets: [
                    {
                        label: 'Barang Masuk',
                        data: masuk,
                        backgroundColor: '#059669',
                        borderRadius: 4,
                        borderWidth: 0,
                    },
                    {
                        label: 'Barang Keluar',
                        data: keluar,
                        backgroundColor: '#DC2626',
                        borderRadius: 4,
                        borderWidth: 0,
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
                            font: { size: 13 }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 11 } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0,0,0,0.05)' },
                        ticks: { font: { size: 11 } }
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
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 16,
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }
});
