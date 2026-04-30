// src/JS/modules/notifications.js
/**
 * Notification Management Module
 * n8n Integration for notification workflows
 */

function switchTab(tabName) {
    // Hide all tabs
    document.getElementById('alertsTab').style.display = 'none';
    document.getElementById('settingsTab').style.display = 'none';
    document.getElementById('integrationsTab').style.display = 'none';

    // Show selected tab
    document.getElementById(tabName + 'Tab').style.display = 'block';

    // Update active button
    document.querySelectorAll('[onclick*="switchTab"]').forEach(btn => {
        btn.classList.remove('border-teal-400', 'text-teal-400');
        btn.classList.add('text-slate-400');
    });

    event.target.classList.add('border-teal-400', 'text-teal-400');
    event.target.classList.remove('text-slate-400');
}

function toggleNotification(element) {
    element.classList.toggle('active');
}

async function saveSettings() {
    try {
        const settings = {
            email_enabled: document.querySelectorAll('.toggle-switch.active')[0] !== undefined,
            push_enabled: document.querySelectorAll('.toggle-switch.active')[1] !== undefined,
            frequency: document.querySelector('input[name="frequency"]:checked').value
        };

        const response = await fetch('/notifications/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });

        const data = await response.json();
        if (data.status === 'success') {
            alert('Settings saved successfully!');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        alert('Error saving settings');
    }
}

async function createJobAlert(keywords, location, frequency = 'instant') {
    try {
        const response = await fetch('/notifications/job-alert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                keywords: keywords,
                location: location,
                frequency: frequency
            })
        });

        const data = await response.json();
        if (data.status === 'success') {
            alert('Job alert created successfully!');
        }
    } catch (error) {
        console.error('Error creating job alert:', error);
        alert('Error creating job alert');
    }
}

// Initialize notifications module when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Any initialization code can go here
    console.log('Notifications module loaded');
});