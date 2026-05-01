// --- Budget Buddy | Modern Components ---

let myPieChart = null;

window.initChart = function() {
    const ctx = document.getElementById('budgetChart');
    if (!ctx) return;
    
    if (myPieChart) {
        myPieChart.destroy();
    }

    // Modern Dark Palette
    const colors = [
        '#3B82F6', // Stay (Blue)
        '#10B981', // Food (Emerald)
        '#F59E0B', // Travel (Amber)
        '#6366F1'  // Misc (Indigo)
    ];

    const data = {
        labels: ['Stay', 'Dining', 'Transport', 'Misc'],
        datasets: [{
            data: [
                parseInt(document.getElementById('sl-stay').value),
                parseInt(document.getElementById('sl-food').value),
                parseInt(document.getElementById('sl-travel').value),
                parseInt(document.getElementById('sl-misc').value)
            ],
            backgroundColor: colors,
            borderWidth: 2,
            borderColor: '#1E293B',
            hoverOffset: 15
        }]
    };

    myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94A3B8',
                        padding: 20,
                        usePointStyle: true,
                        font: { family: 'Inter', size: 11 }
                    }
                }
            }
        }
    });
};

window.updateChart = function() {
    if (!myPieChart) return;
    
    const stay = parseInt(document.getElementById('sl-stay').value);
    const food = parseInt(document.getElementById('sl-food').value);
    const travel = parseInt(document.getElementById('sl-travel').value);
    const misc = parseInt(document.getElementById('sl-misc').value);
    
    document.getElementById('val-stay').innerText = stay + '%';
    document.getElementById('val-food').innerText = food + '%';
    document.getElementById('val-travel').innerText = travel + '%';
    document.getElementById('val-misc').innerText = misc + '%';

    myPieChart.data.datasets[0].data = [stay, food, travel, misc];
    myPieChart.update();
};

window.saveBudgetPlan = function() {
    // Professional Toast would be better, but for now a simple console log and navigation
    console.log("Budget allocation updated.");
    navigate('home');
};
