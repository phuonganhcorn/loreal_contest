// CSRF Token setup for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Tab Switching Logic
function switchTab(tabName) {
    const tabs = ['routine', 'calendar', 'notifications'];
    tabs.forEach(tab => {
        const tabContent = document.getElementById(`${tab}-tab`);
        tabContent.classList.toggle('hidden', tab !== tabName);
    });
}

// Routine Generation Function
async function generateRoutine() {
    const skinType = document.getElementById('skin-type').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    
    const concerns = [];
    document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
        concerns.push(checkbox.value);
    });

    try {
        const response = await fetch('/generate-routine/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                skin_type: skinType,
                age: age,
                gender: gender,
                concerns: concerns
            })
        });

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        
        document.getElementById('routine-result').innerHTML = 
            `<div class="prose">${data.routine}</div>`;
    } catch (error) {
        console.error('Error generating routine:', error);
        document.getElementById('routine-result').innerHTML = 
            'Error generating routine. Please try again.';
    }
}

// Calendar Generation Functions
async function generateDailyRoutine(skinType, concerns, age, gender, dayOfWeek) {
    try {
        const response = await fetch('/generate-daily-routine/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                skin_type: skinType,
                concerns: concerns,
                age: age,
                gender: gender,
                day_of_week: dayOfWeek
            })
        });

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }

        return data.routine_html;
    } catch (error) {
        console.error('Error generating daily routine:', error);
        return getFallbackRoutine(skinType);
    }
}

function getFallbackRoutine(skinType) {
    const fallbackRoutines = {
        'Oily': [
            '1. Gentle Cleanser: Remove excess oil and impurities',
            '2. Salicylic Acid Toner: Control sebum and minimize pores',
            '3. Lightweight Moisturizer: Hydrate without clogging pores',
            '4. Sunscreen SPF 50+: Protect from UV rays'
        ],
        'Dry': [
            '1. Cream Cleanser: Gentle cleansing',
            '2. Hyaluronic Acid Serum: Deep hydration',
            '3. Rich Moisturizer: Lock in moisture',
            '4. Sunscreen SPF 30+: UV protection'
        ]
    };

    const routine = fallbackRoutines[skinType] || fallbackRoutines['Oily'];
    return `
        <h5 class="font-semibold mb-2 text-lg text-red-600">
            Fallback Routine
        </h5>
        <div class="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
            <ul class="list-disc list-inside text-sm">
                ${routine.map(step => `<li>${step}</li>`).join('')}
            </ul>
        </div>
    `;
}

async function generateCalendar() {
    const skinType = document.getElementById('skin-type').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    
    const concerns = [];
    document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
        concerns.push(checkbox.value);
    });

    const calendarResult = document.getElementById('calendar-result');
    calendarResult.innerHTML = '';

    const calendarGrid = document.createElement('div');
    calendarGrid.className = 'calendar-grid';

    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'modal-overlay';
    
    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    
    const modalClose = document.createElement('button');
    modalClose.className = 'modal-close';
    modalClose.innerHTML = '&times;';
    modalClose.addEventListener('click', () => {
        modalOverlay.classList.remove('show');
    });
    
    modalContent.appendChild(modalClose);

    const startDate = new Date();
    const routinePromises = [];

    for (let week = 0; week < 4; week++) {
        for (let day = 0; day < 7; day++) {
            const currentDate = new Date(startDate);
            currentDate.setDate(startDate.getDate() + (week * 7) + day);

            const dayCard = document.createElement('div');
            dayCard.className = 'calendar-day';
            
            const dateElement = document.createElement('div');
            dateElement.className = 'calendar-day-date';
            dateElement.textContent = currentDate.toLocaleDateString('en-US', {
                month: 'short', 
                day: 'numeric'
            });
            dayCard.appendChild(dateElement);

            const routinePromise = generateDailyRoutine(skinType, concerns, age, gender, day)
                .then(routineHtml => {
                    const routineElement = document.createElement('div');
                    routineElement.innerHTML = routineHtml;
                    routineElement.className = 'p-2 text-xs overflow-hidden';
                    dayCard.appendChild(routineElement);

                    dayCard.addEventListener('click', () => {
                        showRoutineModal(currentDate, routineHtml, modalOverlay, modalContent);
                    });
                });

            routinePromises.push(routinePromise);
            calendarGrid.appendChild(dayCard);
        }
    }

    await Promise.all(routinePromises);
    calendarResult.appendChild(calendarGrid);
    document.body.appendChild(modalOverlay);
}

function showRoutineModal(date, routineHtml, modalOverlay, modalContent) {
    modalContent.innerHTML = '';
    const modalClose = document.createElement('button');
    modalClose.className = 'modal-close';
    modalClose.innerHTML = '&times;';
    modalClose.addEventListener('click', () => {
        modalOverlay.classList.remove('show');
    });
    modalContent.appendChild(modalClose);
    
    const dateElement = document.createElement('h2');
    dateElement.className = 'text-2xl font-bold mb-4 text-center';
    dateElement.textContent = date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    modalContent.appendChild(dateElement);

    const routineElement = document.createElement('div');
    routineElement.innerHTML = routineHtml;
    routineElement.className = 'text-base';
    modalContent.appendChild(routineElement);

    modalOverlay.classList.add('show');
}

// Theme Toggle Functionality
function toggleTheme() {
    const html = document.documentElement;
    const themeIcon = document.querySelector('.theme-icon');

    html.classList.toggle('dark-mode');
    
    if (html.classList.contains('dark-mode')) {
        themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
}

// Check saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const html = document.documentElement;
    const themeIcon = document.querySelector('.theme-icon');

    if (savedTheme === 'dark') {
        html.classList.add('dark-mode');
        themeIcon.textContent = '☀️';
    }

    // Close modal when clicking outside
    document.addEventListener('click', (event) => {
        const modalOverlay = document.querySelector('.modal-overlay');
        if (modalOverlay && modalOverlay.classList.contains('show')) {
            if (event.target === modalOverlay) {
                modalOverlay.classList.remove('show');
            }
        }
    });
});

// Skin Analysis Functions
async function performSkinAnalysis() {
    const imageInput = document.getElementById('skin-analysis-upload');
    const analysisResult = document.getElementById('skin-analysis-result');
    
    // Check if an image is selected
    if (!imageInput.files || imageInput.files.length === 0) {
        analysisResult.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                Please select an image to analyze.
            </div>
        `;
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    // Show loading state
    analysisResult.innerHTML = `
        <div class="flex justify-center items-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
            <span class="ml-2">Analyzing your skin...</span>
        </div>
    `;

    try {
        // Send image to server for analysis
        const response = await fetch('/api/analyze-skin/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const data = await response.json();

        // Handle successful analysis
        if (data.success) {
            displaySkinAnalysisResults(data.analysis);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        // Handle errors
        analysisResult.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                ${error.message || 'An unexpected error occurred during skin analysis.'}
            </div>
        `;
        console.error('Skin Analysis Error:', error);
    }
}

function displaySkinAnalysisResults(analysis) {
    const analysisResult = document.getElementById('skin-analysis-result');
    
    // Create a detailed result display
    analysisResult.innerHTML = `
        <div class="bg-white shadow-lg rounded-lg p-6">
            <h3 class="text-2xl font-bold mb-4 text-purple-600">Skin Analysis Results</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <h4 class="font-semibold text-lg">Skin Type</h4>
                    <p class="text-gray-700">${analysis.skin_type || 'Not determined'}</p>
                </div>
                
                <div>
                    <h4 class="font-semibold text-lg">Confidence Score</h4>
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div class="bg-purple-600 h-2.5 rounded-full" 
                             style="width: ${(analysis.confidence_score || 0) * 100}%">
                        </div>
                    </div>
                    <p class="text-sm text-gray-600">
                        ${((analysis.confidence_score || 0) * 100).toFixed(2)}% Confidence
                    </p>
                </div>
            </div>

            <div class="mt-4">
                <h4 class="font-semibold text-lg mb-2">Detected Concerns</h4>
                <div class="flex flex-wrap gap-2">
                    ${(analysis.concerns || []).map(concern => `
                        <span class="bg-purple-100 text-purple-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded">
                            ${concern}
                        </span>
                    `).join('') || '<p class="text-gray-600">No specific concerns detected</p>'}
                </div>
            </div>

            <div class="mt-4">
                <h4 class="font-semibold text-lg mb-2">Recommendations</h4>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-gray-700">${analysis.recommendations || 'No specific recommendations'}</p>
                </div>
            </div>

            <div class="mt-6 text-center">
                <button onclick="saveAnalysisToProfile()" class="bg-purple-600 text-white px-6 py-2 rounded-full hover:bg-purple-700 transition">
                    Save Analysis to Profile
                </button>
            </div>
        </div>
    `;
}

async function saveAnalysisToProfile() {
    try {
        const response = await fetch('/api/save-skin-analysis/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        });

        const data = await response.json();

        if (data.success) {
            alert('Analysis saved to your profile successfully!');
        } else {
            throw new Error(data.error || 'Failed to save analysis');
        }
    } catch (error) {
        console.error('Save Analysis Error:', error);
        alert('Failed to save analysis. Please try again.');
    }
}

// Image preview functionality
function previewSkinAnalysisImage(event) {
    const imagePreview = document.getElementById('skin-analysis-preview');
    const file = event.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
        }
        reader.readAsDataURL(file);
    } else {
        imagePreview.src = '';
        imagePreview.classList.add('hidden');
    }
}