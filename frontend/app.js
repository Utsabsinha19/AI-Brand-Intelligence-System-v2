document.addEventListener('DOMContentLoaded', () => {
    // 1. Initial Page Load Animations (Anime.js)
    anime.timeline({ easing: 'easeOutExpo' })
        .add({
            targets: '.anim-header',
            translateY: [-20, 0],
            opacity: [0, 1],
            duration: 800
        })
        .add({
            targets: '.tech-badge',
            scale: [0.8, 1],
            opacity: [0, 1],
            delay: anime.stagger(100),
            duration: 600
        }, '-=600')
        .add({
            targets: '.anim-panel',
            translateY: [20, 0],
            opacity: [0, 1],
            duration: 800,
            delay: anime.stagger(200)
        }, '-=400');

    // 2. Real-Time Analytics State
    let stats = {
        count: 0,
        totalScore: 0,
        avgScore: 0.00
    };
    const categoryCounts = {};

    // 3. Chart.js Integration
    const ctx = document.getElementById('relevanceChart').getContext('2d');
    const relevanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Relevance Score',
                data: [],
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderWidth: 2,
                tension: 0.4, // Creates smooth, curved lines
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: 1.0, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                x: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } }
            },
            plugins: {
                legend: { labels: { color: '#f8fafc', font: { family: "'Segoe UI', sans-serif" } } }
            }
        }
    });

    // 4. WebSocket Integration
    const ws = new WebSocket('ws://localhost:8000/ws/analytics');
    const feed = document.getElementById('live-feed');
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        // -- Update Analytics State --
        stats.count += 1;
        stats.totalScore += data.relevance_score;
        stats.avgScore = stats.totalScore / stats.count;
        
        categoryCounts[data.matched_category] = (categoryCounts[data.matched_category] || 0) + 1;
        const topCat = Object.keys(categoryCounts).reduce((a, b) => categoryCounts[a] > categoryCounts[b] ? a : b);

        // -- Animate Number Counters (Anime.js) --
        anime({
            targets: document.getElementById('total-count'),
            innerHTML: [stats.count - 1, stats.count],
            round: 1,
            duration: 1000,
            easing: 'easeOutQuad'
        });

        anime({
            targets: document.getElementById('avg-relevance'),
            innerHTML: [stats.avgScore.toFixed(2)],
            round: 100, // round to 2 decimal places implicitly
            duration: 1000,
            easing: 'easeOutQuad'
        });

        document.getElementById('top-category').innerText = topCat;

        // -- Build & Animate New Stream Row --
        const row = document.createElement('div');
        row.className = 'mention-row';
        row.innerHTML = `
            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding-right: 15px;">${data.post.substring(0, 60)}...</span>
            <span style="color: #38bdf8">${data.matched_category}</span>
            <span>${data.relevance_score.toFixed(2)} (${data.confidence})</span>
            <span style="color: ${data.decision === 'Highly Relevant' ? '#4ade80' : '#f87171'}">${data.decision}</span>
        `;
        
        feed.prepend(row);
        
        anime({
            targets: row,
            translateX: [-50, 0],
            opacity: [0, 1],
            backgroundColor: ['#1e293b', '#131c2f'],
            duration: 800,
            easing: 'easeOutElastic(1, .8)'
        });

        // -- Update Chart.js Data --
        const timeNow = new Date().toLocaleTimeString();
        relevanceChart.data.labels.push(timeNow);
        relevanceChart.data.datasets[0].data.push(data.relevance_score);
        
        if (relevanceChart.data.labels.length > 20) {
            relevanceChart.data.labels.shift();
            relevanceChart.data.datasets[0].data.shift();
        }
        relevanceChart.update();
    };

    // 5. Input Submission to Trigger Analysis
    const analyzeBtn = document.getElementById('analyze-btn');
    const mentionInput = document.getElementById('mention-input');

    if (analyzeBtn && mentionInput) {
        analyzeBtn.addEventListener('click', async () => {
            const text = mentionInput.value.trim();
            if (!text) return;

            // Change button state
            analyzeBtn.innerText = 'Analyzing...';
            analyzeBtn.style.opacity = '0.7';

            try {
                const response = await fetch('http://localhost:8000/analyze/relevance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                if (response.ok) {
                    mentionInput.value = ''; // clear on success
                }
            } catch (err) {
                console.error('Fetch error:', err);
            } finally {
                analyzeBtn.innerText = 'Analyze Text';
                analyzeBtn.style.opacity = '1';
            }
        });
    }
});