function renderSchedule() {
    const list = document.getElementById('schedule-list');
    const agenda = window.BSidesData ? window.BSidesData.agenda : [];

    if (!list) return;

    if (!agenda || agenda.length === 0) {
        list.innerHTML = '<div class="text-center" style="color:#eb3812">Loading schedule...</div>';
        return;
    }

    list.innerHTML = ''; // Clear loading

    agenda.forEach(item => {
        const isBreak = item.isBreak;
        const cssClass = isBreak ? 'session-item break-item' : 'session-item';
        const timeRange = item.endTime ? `${item.startTime} - ${item.endTime}` : item.startTime;

        // Social Links Logic for Schedule
        let speakerSocial = '';
        if (item.speakerLinks) {
            speakerSocial = '<div class="speaker-social-small" style="display:inline-block; margin-left:10px;">';
            if (item.speakerLinks.linkedin) speakerSocial += `<a href="${item.speakerLinks.linkedin}" target="_blank" style="color:var(--color-primary); margin-right:5px;"><i class="fab fa-linkedin"></i></a>`;
            if (item.speakerLinks.twitter) speakerSocial += `<a href="${item.speakerLinks.twitter}" target="_blank" style="color:var(--color-primary); margin-right:5px;"><i class="fab fa-x-twitter"></i></a>`;
            if (item.speakerLinks.github) speakerSocial += `<a href="${item.speakerLinks.github}" target="_blank" style="color:var(--color-primary); margin-right:5px;"><i class="fab fa-github"></i></a>`;
            speakerSocial += '</div>';
        }

        const div = document.createElement('div');
        div.className = cssClass;
        div.innerHTML = `
            <div class="session-time">${timeRange}</div>
            <div class="session-details">
                <h3 class="session-title">${item.title}</h3>
                ${item.presenter ? `<div class="session-presenter"><i class="fas fa-user-secret"></i> ${item.presenter} ${speakerSocial}</div>` : ''}
            </div>
        `;

        if (!isBreak) {
            div.addEventListener('click', (e) => {
                // Prevent modal if clicking directly on a link
                if (e.target.closest('a')) return;
                openSessionModal(item);
            });
        }

        list.appendChild(div);
    });
}

// Expose to window
window.renderSchedule = renderSchedule;

// Auto-run if data is already present (e.g. from sync load)
document.addEventListener('DOMContentLoaded', () => {
    if (window.BSidesData && window.BSidesData.agenda) {
        renderSchedule();
    }
});