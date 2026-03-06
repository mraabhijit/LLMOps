// Auth State
let authToken = null;
const API_URL = "http://localhost:8000";

// DOM Elements
const authContainer = document.getElementById('authContainer');
const loggedOutState = document.getElementById('loggedOutState');
const loggedInState = document.getElementById('loggedInState');
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const logoutBtn = document.getElementById('logoutBtn');

const loginModal = document.getElementById('loginModal');
const modalTitle = document.getElementById('modalTitle');
const submitAuthBtn = document.getElementById('submitAuthBtn');
const closeLoginBtn = document.getElementById('closeLoginBtn');
const emailInput = document.getElementById('emailInput');
const passwordInput = document.getElementById('passwordInput');
const userEmailDisplay = document.getElementById('userEmail');

const searchBtn = document.getElementById('searchButton');
const ingredientInput = document.getElementById('ingredientInput');
const recipeContent = document.getElementById('recipeContent');
const micButton = document.getElementById('micButton');
const languageSelect = document.getElementById('languageSelect');

let isLoginMode = true;

// Functions to update UI based on state
function updateAuthUI() {
    if (authToken) {
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
    isLoginMode = true;
    modalTitle.textContent = "Login";
    submitAuthBtn.textContent = "Log In";
    loginModal.classList.remove('hidden');
});

registerBtn.addEventListener('click', () => {
    isLoginMode = false;
    modalTitle.textContent = "Register";
    submitAuthBtn.textContent = "Register";
    loginModal.classList.remove('hidden');
});

closeLoginBtn.addEventListener('click', () => {
    loginModal.classList.add('hidden');
});

submitAuthBtn.addEventListener('click', async () => {
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    const endpoint = isLoginMode ? "/login" : "/register";
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        
        if (!response.ok) {
            alert(data.detail || "Authentication error.");
            return;
        }

        if (isLoginMode) {
            authToken = data.access_token;
            updateAuthUI();
            loginModal.classList.add('hidden');
        } else {
            alert(data.message);
            // Switch to login mode
            isLoginMode = true;
            modalTitle.textContent = "Login";
            submitAuthBtn.textContent = "Log In";
        }
    } catch (err) {
        alert("Network error. Please try again later.");
        console.error(err);
    }
});

logoutBtn.addEventListener('click', () => {
    authToken = null;
    updateAuthUI();
    recipeContent.innerHTML = '<p class="placeholder-text">Recipe.</p>';
    recipeContent.classList.remove('recipe-text-loaded');
});

// Search Functionality (SSE Streaming)
searchBtn.addEventListener('click', async () => {
    const query = ingredientInput.value.trim();
    const language = languageSelect.value;
    
    if (!query) {
        alert("Please enter some ingredients first.");
        return;
    }

    if (!authToken) {
        alert("Please login first to view recipes.");
        loginBtn.click();
        return;
    }

    recipeContent.innerHTML = '<p class="placeholder-text">Searching...</p>';
    
    try {
        const response = await fetch(`${API_URL}/recipe/text`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`
            },
            body: JSON.stringify({
                ingredients: query,
                allergies: [],
                language: language
            })
        });

        if (!response.ok) {
            if(response.status === 401 || response.status === 403) {
                alert("Session expired or unauthorized. Please login again.");
                authToken = null;
                updateAuthUI();
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle SSE stream
        recipeContent.innerHTML = '';
        recipeContent.classList.add('recipe-text-loaded');
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        
        // Wrap output in a pre block to maintain line breaks
        const preElem = document.createElement('pre');
        preElem.style.whiteSpace = "pre-wrap";
        preElem.style.fontFamily = "inherit";
        recipeContent.appendChild(preElem);

        let done = false;
        while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            
            if (value) {
                const chunkStr = decoder.decode(value, { stream: true });
                const lines = chunkStr.split('\n');
                
                for (let line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.replace('data: ', '');
                        if(dataStr.trim() === '') continue;
                        
                        try {
                            const parsedData = JSON.parse(dataStr);
                            if (parsedData.type === 'metadata') {
                                if (parsedData.error) {
                                    preElem.innerHTML += `\n<span style="color: red;">ERROR: ${parsedData.error}</span>\n`;
                                }
                                if (parsedData.is_safe === false) {
                                    preElem.innerHTML += `\n<span style="color: red;">[BLOCKED] Unsafe Request</span>\n`;
                                }
                                if (parsedData.warnings && parsedData.warnings.length > 0) {
                                    preElem.innerHTML += `\n<strong style="color: orange;">WARNINGS:</strong>\n`;
                                    parsedData.warnings.forEach(w => {
                                        preElem.innerHTML += `<span style="color: orange;">- ${w}</span>\n`;
                                    });
                                    preElem.innerHTML += '\n';
                                }
                            } else if (parsedData.type === 'response') {
                                preElem.innerHTML += parsedData.text;
                            } else if (parsedData.type === 'chunk' && parsedData.text) {
                                preElem.innerHTML += parsedData.text;
                            }
                        } catch (e) {
                            console.error("Error parsing JSON chunk", e, dataStr);
                        }
                    }
                }
            }
        }
    } catch (err) {
        console.error("Error streaming recipe", err);
        recipeContent.innerHTML = '<p class="placeholder-text" style="color: red;">An error occurred while fetching the recipe.</p>';
    }
});

// Mic button simulation
micButton.addEventListener('click', () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert("Speech recognition isn't supported in your browser.");
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    // Set language from dropdown for speech recognition map
    const langMap = {
        "bengali": "bn-IN",
        "english": "en-IN",
        "gujarati": "gu-IN",
        "hindi": "hi-IN",
        "kannada": "kn-IN",
        "malayalam": "ml-IN",
        "marathi": "mr-IN",
        "odia": "od-IN",
        "punjabi": "pa-IN",
        "tamil": "ta-IN",
        "telugu": "te-IN",
    };
    recognition.lang = langMap[languageSelect.value] || 'en-IN';
    
    micButton.style.color = 'red'; 
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        ingredientInput.value = transcript;
        micButton.style.color = '';
    };
    
    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
        micButton.style.color = '';
    };
    
    recognition.onend = function() {
        micButton.style.color = '';
    };
    
    recognition.start();
});

// Initial Setup
updateAuthUI();
