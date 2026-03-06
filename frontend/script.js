// Simulated Auth State
let isLoggedIn = false;

// DOM Elements
const authContainer = document.getElementById('authContainer');
const loggedOutState = document.getElementById('loggedOutState');
const loggedInState = document.getElementById('loggedInState');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const loginModal = document.getElementById('loginModal');
const submitLoginBtn = document.getElementById('submitLoginBtn');
const closeLoginBtn = document.getElementById('closeLoginBtn');
const emailInput = document.getElementById('emailInput');
const userEmailDisplay = document.getElementById('userEmail');

const searchBtn = document.getElementById('searchButton');
const ingredientInput = document.getElementById('ingredientInput');
const recipeContent = document.getElementById('recipeContent');
const micButton = document.getElementById('micButton');

// Functions to update UI based on state
function updateAuthUI() {
    if (isLoggedIn) {
        loggedOutState.classList.add('hidden');
        loggedInState.classList.remove('hidden');
        userEmailDisplay.textContent = emailInput.value || 'user@example.com';
    } else {
        loggedOutState.classList.remove('hidden');
        loggedInState.classList.add('hidden');
    }
}

// Event Listeners for Auth
loginBtn.addEventListener('click', () => {
    loginModal.classList.remove('hidden');
});

closeLoginBtn.addEventListener('click', () => {
    loginModal.classList.add('hidden');
});

submitLoginBtn.addEventListener('click', () => {
    isLoggedIn = true;
    updateAuthUI();
    loginModal.classList.add('hidden');
    // If a search was pending, we could trigger it here
});

logoutBtn.addEventListener('click', () => {
    isLoggedIn = false;
    updateAuthUI();
    recipeContent.innerHTML = '<p class="placeholder-text">Recipe.</p>';
    recipeContent.classList.remove('recipe-text-loaded');
});

// Mock Search Functionality
searchBtn.addEventListener('click', () => {
    const query = ingredientInput.value.trim();
    
    if (!query) {
        alert("Please enter some ingredients first.");
        return;
    }

    if (!isLoggedIn) {
        alert("Please login first to view recipes.");
        loginModal.classList.remove('hidden');
        return;
    }

    // Simulate API Call / Formatting
    recipeContent.innerHTML = '<p class="placeholder-text">Loading...</p>';
    
    setTimeout(() => {
        recipeContent.classList.add('recipe-text-loaded');
        recipeContent.innerHTML = `
            <h3>Recipe for: ${query}</h3>
            <p><strong>Ingredients:</strong> ${query}</p>
            <p><strong>Instructions:</strong></p>
            <ol>
                <li>Preheat oven to 350°F (175°C).</li>
                <li>Mix the ${query} together in a large bowl.</li>
                <li>Bake for 30 minutes until golden brown.</li>
                <li>Serve hot and enjoy!</li>
            </ol>
            <p><em>Note: This is a placeholder recipe. The backend connection will provide real data.</em></p>
        `;
    }, 1000);
});

// Mic button simulation
micButton.addEventListener('click', () => {
    // Check for browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert("Speech recognition isn't supported in your browser.");
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    micButton.style.color = 'red'; // Visual feedback
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        ingredientInput.value = transcript;
        micButton.style.color = ''; // Reset color
    };
    
    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
        micButton.style.color = ''; // Reset color
    };
    
    recognition.onend = function() {
        micButton.style.color = ''; // Reset color
    };
    
    recognition.start();
});

// Initial Setup
updateAuthUI();
