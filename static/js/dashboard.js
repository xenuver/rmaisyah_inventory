// ── Dashboard Charts (Chart.js) ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

    Chart.defaults.font.family = "'Inter', sans-serif";

    // ── Stock Trend (Bar Chart - Side by Side) ────────────────────────
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
                        backgroundColor: '#10B981', // Emerald 500
                        borderRadius: 4,
                        barPercentage: 0.8,
                        categoryPercentage: 0.7,
                    },
                    {
                        label: 'Barang Keluar',
                        data: keluar,
                        backgroundColor: '#EF4444', // Red 500
                        borderRadius: 4,
                        barPercentage: 0.8,
                        categoryPercentage: 0.7,
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
                            padding: 15,
                            font: { size: 12, weight: '500' }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 10 } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0,0,0,0.04)' },
                        ticks: { font: { size: 10 } }
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
            '#6366F1', // Indigo
            '#3B82F6', // Blue
            '#10B981', // Emerald
            '#F59E0B', // Amber
            '#EC4899', // Pink
            '#8B5CF6', // Violet
            '#EF4444', // Red
            '#14B8A6', // Teal
            '#F97316', // Orange
            '#6B7280'  // Gray
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
                    hoverOffset: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 12,
                            font: { size: 11, weight: '500' }
                        }
                    }
                }
            }
        });
    }
});
