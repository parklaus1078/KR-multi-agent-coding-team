// Multi-Agent Coding Team - Dashboard JavaScript

const API_BASE = window.location.origin + '/api';

// State
let currentTab = 'pipelines';
let pipelines = [];
let refreshInterval = null;
let selectedProject = null;
let selectedTickets = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initPipelineForm();
    initAgentForms();
    initSkillButtons();
    initRefresh();
    loadProjects();
    loadPipelines();
    loadStats();
});

// Tab Navigation
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            switchTab(tab);
        });
    });
}

function switchTab(tab) {
    currentTab = tab;

    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tab}-tab`);
    });

    // Load data for tab
    if (tab === 'pipelines') {
        loadPipelines();
    } else if (tab === 'stats') {
        loadStats();
    }
}

// Pipeline Form
function initPipelineForm() {
    // Listen to project selection
    const projectSelect = document.getElementById('project-select');
    projectSelect.addEventListener('change', async (e) => {
        const projectName = e.target.value;
        if (projectName) {
            selectedProject = projectName;
            await loadTickets(projectName);
            document.getElementById('project-input').value = projectName;
            document.getElementById('tickets-section').style.display = 'block';
        } else {
            selectedProject = null;
            document.getElementById('tickets-section').style.display = 'none';
            document.getElementById('project-input').value = '';
        }
    });

    const runBtn = document.getElementById('run-pipeline-btn');
    runBtn.addEventListener('click', async () => {
        let ticket = document.getElementById('ticket-input').value.trim();
        const project = document.getElementById('project-input').value.trim();

        // If no manual ticket input, use selected tickets
        if (!ticket && selectedTickets.length > 0) {
            ticket = selectedTickets[0]; // Use first selected ticket
        }

        if (!ticket || !project) {
            showToast('Please enter both ticket and project', 'error');
            return;
        }

        await runPipeline(ticket, project);
    });
}

async function runPipeline(ticket, project) {
    try {
        showToast('Starting pipeline...', 'info');

        const response = await fetch(`${API_BASE}/pipeline/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket, project, resume: false })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(`Pipeline started: ${ticket}`, 'success');
            document.getElementById('ticket-input').value = '';
            document.getElementById('project-input').value = '';
            loadPipelines();
        } else {
            showToast(data.detail || 'Failed to start pipeline', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// Load Projects
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/projects/list`);
        const data = await response.json();
        renderProjectsDropdown(data.projects || []);
    } catch (error) {
        console.error('Failed to load projects:', error);
    }
}

// Render Projects Dropdown
function renderProjectsDropdown(projects) {
    const select = document.getElementById('project-select');
    select.innerHTML = '<option value="">Select Project...</option>';
    projects.forEach(project => {
        const option = document.createElement('option');
        option.value = project.name;
        option.textContent = `${project.name} (${project.type || 'unknown'})`;
        select.appendChild(option);
    });
}

// Load Tickets
async function loadTickets(projectName) {
    try {
        const response = await fetch(`${API_BASE}/projects/${projectName}/tickets`);
        const data = await response.json();
        renderTicketsList(data.tickets || []);
    } catch (error) {
        console.error('Failed to load tickets:', error);
        showToast('Failed to load tickets', 'error');
    }
}

// Render Tickets List
function renderTicketsList(tickets) {
    const container = document.getElementById('tickets-list');

    if (tickets.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--gray-600);">No tickets found</p>';
        return;
    }

    container.innerHTML = tickets.map(ticket => `
        <div class="ticket-item">
            <input type="checkbox" id="${ticket.ticket}" value="${ticket.ticket}" onchange="handleTicketSelection('${ticket.ticket}')">
            <label for="${ticket.ticket}">
                <strong>${ticket.ticket}</strong> - ${ticket.title || 'No title'}
            </label>
        </div>
    `).join('');
}

// Handle Ticket Selection
function handleTicketSelection(ticketId) {
    const checkbox = document.getElementById(ticketId);
    if (checkbox.checked) {
        if (!selectedTickets.includes(ticketId)) {
            selectedTickets.push(ticketId);
        }
        // Auto-fill ticket input with first selected ticket
        document.getElementById('ticket-input').value = ticketId;
    } else {
        selectedTickets = selectedTickets.filter(t => t !== ticketId);
        // Clear ticket input if no tickets selected
        if (selectedTickets.length === 0) {
            document.getElementById('ticket-input').value = '';
        } else {
            document.getElementById('ticket-input').value = selectedTickets[0];
        }
    }
}

// Load Pipelines
async function loadPipelines() {
    try {
        const response = await fetch(`${API_BASE}/pipeline/list`);
        const data = await response.json();

        pipelines = data.pipelines || [];
        renderPipelines();
    } catch (error) {
        console.error('Failed to load pipelines:', error);
    }
}

function renderPipelines() {
    const grid = document.getElementById('pipelines-grid');

    if (pipelines.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <p>No active pipelines</p>
                <p class="hint">Enter a ticket and project name to start</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = pipelines.map(pipeline => `
        <div class="pipeline-card" onclick="showPipelineDetails('${pipeline.ticket}')">
            <div class="pipeline-header">
                <span class="pipeline-ticket">${pipeline.ticket}</span>
                <span class="pipeline-status status-${pipeline.status}">
                    ${getStatusEmoji(pipeline.status)} ${pipeline.status.toUpperCase()}
                </span>
            </div>

            <div class="pipeline-info">
                <p><strong>Project:</strong> ${pipeline.project || 'N/A'}</p>
                <p><strong>Step:</strong> ${pipeline.current_step || 'N/A'}</p>
            </div>

            <div class="pipeline-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${pipeline.progress || 0}%"></div>
                </div>
                <p style="text-align: center; margin-top: 8px; font-size: 0.85rem; color: var(--gray-600);">
                    ${pipeline.progress || 0}%
                </p>
            </div>

            ${renderSteps(pipeline.steps)}
        </div>
    `).join('');
}

function renderSteps(steps) {
    if (!steps || steps.length === 0) return '';

    return `
        <div class="pipeline-steps">
            ${steps.map(step => `
                <div class="step step-${step.status}">
                    <span class="step-icon">${getStepIcon(step.status)}</span>
                    <span>${step.name}</span>
                    ${step.duration ? `<span style="margin-left: auto; font-size: 0.8rem;">${step.duration.toFixed(1)}s</span>` : ''}
                </div>
            `).join('')}
        </div>
    `;
}

function getStatusEmoji(status) {
    const emojis = {
        running: '🔵',
        success: '✅',
        failed: '❌',
        pending: '⏳',
        cancelled: '🚫'
    };
    return emojis[status] || '⚪';
}

function getStepIcon(status) {
    const icons = {
        running: '⏳',
        success: '✅',
        failed: '❌',
        pending: '⚪'
    };
    return icons[status] || '⚪';
}

// Pipeline Details Modal
async function showPipelineDetails(ticket) {
    try {
        const response = await fetch(`${API_BASE}/pipeline/status/${ticket}`);
        const pipeline = await response.json();

        const modal = document.getElementById('pipeline-modal');
        const modalBody = document.getElementById('modal-body');

        modalBody.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h3>Ticket: ${pipeline.ticket}</h3>
                <p><strong>Project:</strong> ${pipeline.project || 'N/A'}</p>
                <p><strong>Status:</strong> ${getStatusEmoji(pipeline.status)} ${pipeline.status.toUpperCase()}</p>
                <p><strong>Progress:</strong> ${pipeline.progress || 0}%</p>
                <p><strong>Started:</strong> ${pipeline.started_at || 'N/A'}</p>
                <p><strong>Completed:</strong> ${pipeline.completed_at || 'N/A'}</p>
            </div>

            <h4>Steps</h4>
            ${renderStepsDetail(pipeline.steps)}

            <div style="margin-top: 20px;">
                <button class="btn-secondary" onclick="viewLogs('${ticket}')">📋 View Logs</button>
                ${pipeline.status === 'running' ? `<button class="btn-primary" onclick="cancelPipeline('${ticket}')" style="background: var(--error); margin-left: 8px;">❌ Cancel</button>` : ''}
            </div>
        `;

        modal.style.display = 'block';
    } catch (error) {
        showToast('Failed to load pipeline details', 'error');
    }
}

function renderStepsDetail(steps) {
    if (!steps || steps.length === 0) return '<p>No steps</p>';

    return `
        <div style="margin-top: 16px;">
            ${steps.map(step => `
                <div style="padding: 12px; margin: 8px 0; background: var(--gray-50); border-radius: 8px; border-left: 4px solid ${getStepColor(step.status)};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><strong>${step.name}</strong></span>
                        <span>${getStepIcon(step.status)} ${step.status}</span>
                    </div>
                    ${step.duration ? `<p style="font-size: 0.85rem; color: var(--gray-600); margin-top: 4px;">Duration: ${step.duration.toFixed(1)}s</p>` : ''}
                    ${step.error ? `<p style="font-size: 0.85rem; color: var(--error); margin-top: 4px;">Error: ${step.error}</p>` : ''}
                </div>
            `).join('')}
        </div>
    `;
}

function getStepColor(status) {
    const colors = {
        running: 'var(--primary)',
        success: 'var(--success)',
        failed: 'var(--error)',
        pending: 'var(--gray-300)'
    };
    return colors[status] || 'var(--gray-300)';
}

async function viewLogs(ticket) {
    try {
        const response = await fetch(`${API_BASE}/pipeline/logs/${ticket}`);
        const data = await response.json();

        const logs = data.logs || 'No logs available';

        const modalBody = document.getElementById('modal-body');
        modalBody.innerHTML = `
            <h3>Logs: ${ticket}</h3>
            <pre style="background: var(--gray-900); color: #0f0; padding: 20px; border-radius: 8px; overflow-x: auto; max-height: 400px; font-size: 0.85rem;">${logs}</pre>
            <button class="btn-secondary" onclick="showPipelineDetails('${ticket}')" style="margin-top: 16px;">← Back</button>
        `;
    } catch (error) {
        showToast('Failed to load logs', 'error');
    }
}

async function cancelPipeline(ticket) {
    if (!confirm(`Cancel pipeline ${ticket}?`)) return;

    try {
        const response = await fetch(`${API_BASE}/pipeline/cancel/${ticket}`, {
            method: 'POST'
        });

        if (response.ok) {
            showToast('Pipeline cancelled', 'success');
            closeModal();
            loadPipelines();
        } else {
            showToast('Failed to cancel pipeline', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// Modal Close
document.querySelector('.close')?.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
    const modal = document.getElementById('pipeline-modal');
    if (e.target === modal) closeModal();
});

function closeModal() {
    document.getElementById('pipeline-modal').style.display = 'none';
}

// Agent Forms
function initAgentForms() {
    const runButtons = document.querySelectorAll('.btn-run');
    runButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const agent = btn.dataset.agent;
            const card = btn.closest('.agent-card');
            const ticket = card.querySelector('.agent-ticket').value.trim();
            const project = card.querySelector('.agent-project').value.trim();

            if (!ticket || !project) {
                showToast('Please enter both ticket and project', 'error');
                return;
            }

            await runAgent(agent, ticket, project);
        });
    });
}

async function runAgent(agent, ticket, project) {
    try {
        showToast(`Starting ${agent} agent...`, 'info');

        const response = await fetch(`${API_BASE}/agents/${agent}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket, project, auto_mode: true })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(`${agent} agent completed`, 'success');
        } else {
            showToast(data.detail || `${agent} agent failed`, 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// Skill Buttons
function initSkillButtons() {
    const skillButtons = document.querySelectorAll('.btn-skill');
    skillButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const skill = btn.dataset.skill;

            const ticket = prompt('Enter ticket (optional):');
            const project = prompt('Enter project:');

            if (!project) {
                showToast('Project is required', 'error');
                return;
            }

            await runSkill(skill, ticket, project);
        });
    });
}

async function runSkill(skill, ticket, project) {
    try {
        showToast(`Running ${skill} skill...`, 'info');

        const response = await fetch(`${API_BASE}/skills/${skill}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket, project, auto_fix: true })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(`${skill} skill completed`, 'success');
        } else {
            showToast(data.detail || `${skill} skill failed`, 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// Statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/pipeline/stats`);
        const stats = await response.json();

        document.getElementById('total-pipelines').textContent = stats.total || 0;
        document.getElementById('success-rate').textContent = `${stats.success_rate || 0}%`;
        document.getElementById('avg-duration').textContent = `${stats.avg_duration || 0}s`;
        document.getElementById('active-count').textContent = stats.active || 0;

        renderActivity(stats.recent || []);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function renderActivity(recent) {
    const chart = document.getElementById('activity-chart');

    if (recent.length === 0) {
        chart.innerHTML = `
            <div class="empty-state">
                <p>No activity data</p>
            </div>
        `;
        return;
    }

    chart.innerHTML = recent.map(item => `
        <div class="activity-item">
            <div>
                <strong>${item.ticket}</strong>
                <p style="font-size: 0.85rem; color: var(--gray-600); margin-top: 4px;">${item.project}</p>
            </div>
            <div style="text-align: right;">
                <span class="pipeline-status status-${item.status}">${getStatusEmoji(item.status)} ${item.status}</span>
                <p style="font-size: 0.85rem; color: var(--gray-600); margin-top: 4px;">${item.duration || 0}s</p>
            </div>
        </div>
    `).join('');
}

// Auto Refresh
function initRefresh() {
    const refreshBtn = document.getElementById('refresh-btn');
    refreshBtn.addEventListener('click', () => {
        if (currentTab === 'pipelines') {
            loadPipelines();
        } else if (currentTab === 'stats') {
            loadStats();
        }
        showToast('Refreshed', 'info');
    });

    // Auto-refresh every 5 seconds for pipelines
    refreshInterval = setInterval(() => {
        if (currentTab === 'pipelines') {
            loadPipelines();
        }
    }, 5000);
}

// Toast Notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Cleanup
window.addEventListener('beforeunload', () => {
    if (refreshInterval) clearInterval(refreshInterval);
});
