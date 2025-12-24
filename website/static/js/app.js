// Configuration
const API_CONFIG = {
    USER_SERVICE: 'http://localhost:8000',
    RIDE_SERVICE: 'http://localhost:8001',
    AI_SERVICE: 'http://localhost:8002'
};

// State Management
let currentUser = null;
let activeRides = [];
let availableRides = [];

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkServiceStatus();
    setInterval(checkServiceStatus, 30000); // Check every 30 seconds
});

function initializeApp() {
    // Check if user is logged in from localStorage
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateUIForLoggedInUser();
    }
}

function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Auth forms
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);

    // Ride forms
    document.getElementById('ai-ride-form').addEventListener('submit', handleAIRideRequest);
    document.getElementById('ride-request-form').addEventListener('submit', handleManualRideRequest);

    // Driver actions
    const refreshBtn = document.getElementById('refresh-rides-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadAvailableRides);
    }
}

// Tab Management
function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    const selectedBtn = document.querySelector(`[data-tab="${tabName}"]`);
    const selectedContent = document.getElementById(`${tabName}-tab`);

    if (selectedBtn) selectedBtn.classList.add('active');
    if (selectedContent) selectedContent.classList.add('active');
}

// Service Status Checking
async function checkServiceStatus() {
    const services = [
        { name: 'user-service', url: `${API_CONFIG.USER_SERVICE}/` },
        { name: 'ride-service', url: `${API_CONFIG.RIDE_SERVICE}/` },
        { name: 'ai-service', url: `${API_CONFIG.AI_SERVICE}/` }
    ];

    for (const service of services) {
        try {
            const response = await fetch(service.url);
            if (response.ok) {
                updateServiceStatus(service.name, 'online');
            } else {
                updateServiceStatus(service.name, 'offline');
            }
        } catch (error) {
            updateServiceStatus(service.name, 'offline');
        }
    }
}

function updateServiceStatus(serviceName, status) {
    const dot = document.getElementById(`${serviceName}-dot`);
    const text = document.getElementById(`${serviceName}-text`);
    
    if (dot) {
        dot.className = `status-dot ${status}`;
    }
    if (text) {
        text.textContent = status === 'online' ? 'Running' : 'Offline';
    }
}

// API Call Logging
function logAPICall(method, url, status, requestData = null, responseData = null) {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${status >= 200 && status < 300 ? 'success' : 'error'}`;
    
    logEntry.innerHTML = `
        <div>
            <span class="log-timestamp">[${timestamp}]</span>
            <span class="log-method">${method}</span>
            <span class="log-url">${url}</span>
            <span class="log-status ${status >= 200 && status < 300 ? 'success' : 'error'}">(${status})</span>
        </div>
        ${requestData ? `<div class="log-body">Request: ${JSON.stringify(requestData, null, 2)}</div>` : ''}
        ${responseData ? `<div class="log-body">Response: ${JSON.stringify(responseData, null, 2)}</div>` : ''}
    `;
    
    const logContainer = document.getElementById('response-log');
    logContainer.insertBefore(logEntry, logContainer.firstChild);
}

// Flow Visualization
function addFlowItem(serviceName, action, status, details) {
    const flowContainer = document.getElementById('flow-container');
    const flowInfo = flowContainer.querySelector('.flow-info');
    if (flowInfo) flowInfo.remove();

    const flowItem = document.createElement('div');
    flowItem.className = `flow-item ${status}`;
    
    const timestamp = new Date().toLocaleTimeString();
    flowItem.innerHTML = `
        <div class="flow-header">[${timestamp}] ${serviceName} → ${action}</div>
        <div class="flow-details">${details}</div>
    `;
    
    flowContainer.insertBefore(flowItem, flowContainer.firstChild);

    // Keep only last 10 items
    while (flowContainer.children.length > 10) {
        flowContainer.removeChild(flowContainer.lastChild);
    }
}

// Authentication Functions
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const url = `${API_CONFIG.USER_SERVICE}/users/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`;
        addFlowItem('User Service', 'Login', 'pending', `Attempting login for ${email}`);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        logAPICall('POST', url, response.status, { email }, data);

        if (data.error) {
            addFlowItem('User Service', 'Login', 'error', data.error);
            alert(data.error);
        } else if (data.user_details) {
            currentUser = data.user_details;
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            addFlowItem('User Service', 'Login', 'success', `Logged in as ${currentUser.username} (${currentUser.role})`);
            updateUIForLoggedInUser();
        }
    } catch (error) {
        addFlowItem('User Service', 'Login', 'error', error.message);
        alert('Login failed: ' + error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const dob = document.getElementById('register-dob').value;
    const role = document.getElementById('register-role').value;

    const userData = {
        username,
        email,
        password,
        dob: dob || null,
        role
    };

    try {
        const url = `${API_CONFIG.USER_SERVICE}/users/register`;
        addFlowItem('User Service', 'Register', 'pending', `Registering user ${username}`);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        logAPICall('POST', url, response.status, userData, data);

        if (data.error) {
            addFlowItem('User Service', 'Register', 'error', data.error);
            alert(data.error);
        } else if (data.user_details) {
            addFlowItem('User Service', 'Register', 'success', `User ${username} registered successfully`);
            alert('Registration successful! Please login.');
            switchTab('login');
            document.getElementById('register-form').reset();
        }
    } catch (error) {
        addFlowItem('User Service', 'Register', 'error', error.message);
        alert('Registration failed: ' + error.message);
    }
}

async function handleLogout() {
    if (!currentUser) return;

    try {
        const url = `${API_CONFIG.USER_SERVICE}/users/logout/${currentUser.id}`;
        addFlowItem('User Service', 'Logout', 'pending', `Logging out ${currentUser.username}`);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        logAPICall('POST', url, response.status, null, data);
        
        addFlowItem('User Service', 'Logout', 'success', 'Logged out successfully');
    } catch (error) {
        console.error('Logout error:', error);
    }

    currentUser = null;
    localStorage.removeItem('currentUser');
    updateUIForLoggedOutUser();
}

function updateUIForLoggedInUser() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'flex';
    document.getElementById('username-display').textContent = `${currentUser.username} (${currentUser.role})`;

    if (currentUser.role === 'rider') {
        document.getElementById('rider-section').style.display = 'block';
        document.getElementById('driver-section').style.display = 'none';
        loadRiderRides();
    } else if (currentUser.role === 'driver') {
        document.getElementById('driver-section').style.display = 'block';
        document.getElementById('rider-section').style.display = 'none';
        loadAvailableRides();
        loadDriverRides();
    }
}

function updateUIForLoggedOutUser() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('rider-section').style.display = 'none';
    document.getElementById('driver-section').style.display = 'none';
    
    // Clear forms
    document.getElementById('login-form').reset();
    document.getElementById('register-form').reset();
}

// AI Service Integration
async function handleAIRideRequest(e) {
    e.preventDefault();
    const requestText = document.getElementById('ai-request-text').value;

    if (!currentUser) {
        alert('Please login first');
        return;
    }

    try {
        // First call AI service to parse the request
        const aiUrl = `${API_CONFIG.AI_SERVICE}/ai/parse_ride_request?request_text=${encodeURIComponent(requestText)}`;
        addFlowItem('AI Service', 'Parse Request', 'pending', `Parsing: "${requestText}"`);
        
        const aiResponse = await fetch(aiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const aiData = await aiResponse.json();
        logAPICall('POST', aiUrl, aiResponse.status, { request_text: requestText }, aiData);

        if (aiData.error) {
            addFlowItem('AI Service', 'Parse Request', 'error', aiData.error);
            alert('AI parsing failed: ' + aiData.error);
            return;
        }

        const parsedDetails = aiData.parsed_details;
        addFlowItem('AI Service', 'Parse Request', 'success', `Parsed: ${parsedDetails.pickup_location} → ${parsedDetails.dropoff_location}`);

        // Pre-fill the manual form with parsed data
        document.getElementById('pickup-location').value = parsedDetails.pickup_location;
        document.getElementById('dropoff-location').value = parsedDetails.dropoff_location;
        
        // Auto-submit the ride request
        await createRideRequest(parsedDetails.pickup_location, parsedDetails.dropoff_location);
        
        document.getElementById('ai-request-text').value = '';
    } catch (error) {
        addFlowItem('AI Service', 'Parse Request', 'error', error.message);
        alert('AI request failed: ' + error.message);
    }
}

// Ride Request Functions
async function handleManualRideRequest(e) {
    e.preventDefault();
    const pickupLocation = document.getElementById('pickup-location').value;
    const dropoffLocation = document.getElementById('dropoff-location').value;

    await createRideRequest(pickupLocation, dropoffLocation);
}

async function createRideRequest(pickupLocation, dropoffLocation) {
    if (!currentUser) {
        alert('Please login first');
        return;
    }

    const rideData = {
        user_id: currentUser.id,
        pickup_location: pickupLocation,
        dropoff_location: dropoffLocation
    };

    try {
        const url = `${API_CONFIG.RIDE_SERVICE}/ride-requests/create`;
        addFlowItem('Ride Service', 'Create Request', 'pending', `${pickupLocation} → ${dropoffLocation}`);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(rideData)
        });
        
        const data = await response.json();
        logAPICall('POST', url, response.status, rideData, data);

        if (data.error) {
            addFlowItem('Ride Service', 'Create Request', 'error', data.error);
            alert('Ride request failed: ' + data.error);
        } else if (data.ride_request_details) {
            addFlowItem('Ride Service', 'Create Request', 'success', `Ride request created with ID: ${data.ride_request_details.id}`);
            alert('Ride request created successfully!');
            document.getElementById('ride-request-form').reset();
            loadRiderRides();
        }
    } catch (error) {
        addFlowItem('Ride Service', 'Create Request', 'error', error.message);
        alert('Ride request failed: ' + error.message);
    }
}

async function cancelRideRequest(rideRequestId) {
    if (!currentUser) return;

    try {
        const url = `${API_CONFIG.RIDE_SERVICE}/ride-requests/cancel_request/${rideRequestId}?user_id=${currentUser.id}`;
        addFlowItem('Ride Service', 'Cancel Request', 'pending', `Cancelling ride ${rideRequestId}`);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        logAPICall('POST', url, response.status, null, data);
        
        addFlowItem('Ride Service', 'Cancel Request', 'success', `Ride ${rideRequestId} cancelled`);
        alert('Ride request cancelled successfully!');
        loadRiderRides();
    } catch (error) {
        addFlowItem('Ride Service', 'Cancel Request', 'error', error.message);
        alert('Cancel failed: ' + error.message);
    }
}

// Driver Functions
async function loadAvailableRides() {
    // In a real application, this would fetch available rides from the backend
    // For now, we'll simulate with mock data stored in the service
    addFlowItem('Ride Service', 'Fetch Available Rides', 'success', 'Loading available ride requests');
    
    const listDiv = document.getElementById('available-rides-list');
    listDiv.innerHTML = '<div class="empty-state">Available rides would appear here. Create a ride request as a rider to see them.</div>';
}

async function acceptRideRequest(rideRequestId) {
    if (!currentUser) return;

    try {
        const url = `${API_CONFIG.RIDE_SERVICE}/ride-requests/accept_ride/${rideRequestId}?driver_id=${currentUser.id}`;
        addFlowItem('Ride Service', 'Accept Ride', 'pending', `Accepting ride ${rideRequestId}`);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        logAPICall('POST', url, response.status, null, data);
        
        addFlowItem('Ride Service', 'Accept Ride', 'success', `Ride ${rideRequestId} accepted`);
        alert('Ride accepted successfully!');
        loadAvailableRides();
        loadDriverRides();
    } catch (error) {
        addFlowItem('Ride Service', 'Accept Ride', 'error', error.message);
        alert('Accept failed: ' + error.message);
    }
}

async function loadDriverRides() {
    const listDiv = document.getElementById('driver-rides-list');
    listDiv.innerHTML = '<div class="empty-state">Your accepted rides will appear here</div>';
}

async function loadRiderRides() {
    const listDiv = document.getElementById('rider-rides-list');
    listDiv.innerHTML = '<div class="empty-state">Your ride requests will appear here after you create them</div>';
}

// Helper function to format dates
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}
