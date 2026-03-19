// Updated loadActivities (fetches from DB)
async function loadActivities() {
    try {
        const response = await fetch('/api/activities');
        const activities = await response.json();
        const board = document.getElementById('activities-board');
        board.innerHTML = '';
        if (activities.length === 0) {
            board.innerHTML = '<p>No upcoming activities.</p>';
            return;
        }
        activities.forEach((activity, index) => {
            const card = document.createElement('div');
            card.className = 'activity-card';
            const daysRemaining = calculateDaysRemaining(activity.due_date);
            card.innerHTML = `
                <div class="activity-header" onclick="toggleDetails(${index})">
                    <strong>${activity.name}</strong>
                    <span>&darr;</span>
                </div>
                <div class="activity-info">
                    <p><strong>Class:</strong> ${activity.class}</p>
                    <p><strong>Date to deliver:</strong> ${activity.due_date}</p>
                </div>
                <div class="activity-details" id="activity-details-${index}">
                    <p><strong>What to do:</strong> ${activity.description}</p>
                    <p><strong>Days remaining:</strong> ${daysRemaining}</p>
                    <button class="btn btn-danger btn-sm" onclick="finishTask(${activity.id})">Finish Task</button>
                </div>
            `;
            board.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading activities:', error);
        document.getElementById('activities-board').innerHTML = '<p>Error loading activities.</p>';
    }
}

// New function to finish a task
async function finishTask(taskId) {
    try {
        const response = await fetch(`/api/finish-activity/${taskId}`, { method: 'PUT' });
        if (response.ok) {
            alert('Task finished!');
            loadActivities();  // Refresh the list
        } else {
            alert('Error finishing task.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error finishing task.');
    }
}

// Updated save handler (already calls loadActivities on success)
document.getElementById('save-task').addEventListener('click', async () => {
    // ... (your existing code)
    if (response.ok) {
        alert('Task added successfully!');
        document.getElementById('add-task-form').reset();
        bootstrap.Modal.getInstance(document.getElementById('addTaskModal')).hide();
        loadActivities();  // Refresh the list
    }
    // ...
});