let opportunitiesData = {};

async function loadData() {
    try {
        const response = await fetch('../data/processed/opportunities.json');
        opportunitiesData = await response.json();
        updateDashboard();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function updateDashboard() {
    document.getElementById('lastUpdate').textContent = new Date().toLocaleString();
    document.getElementById('oppCount').textContent = opportunitiesData.combined ? opportunitiesData.combined.length : 0;
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

window.addEventListener('load', loadData);
