// Mood to Recommendations mapping 
const moodRecommendations = {
    stressed: {
        playlist: ["lofi-focus", "ambient-chill"],
        bg: "stressed-bg",
        timer: "10/2 micro"
    },

    sleepy: {
        playlist: ["ambient-chill", "classical-deep"],
        bg: "sleepy-bg",
        timer: "25/5 pomodoro" 
    },

    motivated: {
        playlist: ["power-up", "lofi-focus"],
        bg: "motivated-bg",
        timer: "50/10 deep work"
    },

    overwhelmed: {
        playlist: ["ambient-chill", "classical-deep"],
        bg: "overwhelmed-bg",
        timer: "10/2 micro"
    },

    calm: {
        playlist: ["nature-sounds", "classical-deep"],
        bg: "calm-bg",
        timer: "25/5 pomodoro"
    }
};

// Timer variables 
let timerDuration = 0;           // seconds left on timer  
let timerInterval = null;        // will store setInterval reference
let isRunning = false;           // track if timer is active
let currentFormat = "pomodoro"; // default timer 
let isWorkPhase = true;


// Playlist categories 
const playlistCategories = {
    "lofi-focus": {
        title: "Lofi Focus",
        description: "Soft beats for calm, sustained concentrations.",
        bpm: "60-90 BPM",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX8Uebhn9wzrS?utm_source=generator"
    },
    "classical-deep": {
        title: "Classical Deep",
        description: "Instrumental classical music for deep thinking.",
        bpm: "50-70 BPM",
        embed: "https://open.spotify.com/embed/playlist/0QknRAZUpwPtM2dQIzAnAa?utm_source=generator"
    },
    "ambient-chill": {
        title: "Ambient Chill",
        description: "Atmospheric sounds to reduce stress.",
        bpm: "No fixed BPM (ambient)",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DWWb1L5n1gkOJ?utm_source=generator"
    },

    "power-up": {
        title: "Power up",
        description: "Upbeat music to increase motivation to study",
        bpm: "100-130 BPM",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1EId6O1Ld1B4MG?utm_source=generator"
    },

    "nature-sounds": {
        title: "Nature Sounds",
        description: "Nature sounds to reduce stress.",
        bpm: "No fixed BPM (ambient)",
        embed: "https://open.spotify.com/embed/playlist/2e3rjSsz1U1tF8rFnoh9lm?utm_source=generator"
    }
};


document.addEventListener("DOMContentLoaded", () => {

    // -----Mood Environment Logic-----
    const globalBtn = document.getElementById("mood-env-btn");
    const moodEnvContainer = document.getElementById("mood-env-container");

    // -----Daily Report Page-----
    const reportBtn = document.getElementById("daily-report-btn");
    const returnBtn = document.getElementById("return-dashboard-btn");
    const mainContent = document.getElementById("main-dashboard-content");

    if (reportBtn) {
        reportBtn.addEventListener("click", () => {
            // Hide dashboard
            mainContent.style.display = "none";

            // Navigate to daily_report page
            window.location.href = "/daily-report/";
        })
    }

    // Return Back to Dashboard
    if (returnBtn){
        returnBtn.addEventListener("click", () => {
            // Navigate back to your main dashboard page
            window.location.href = "/dashboard/";
        });
    }


    // Daily report progress bar
    const fill = document.getElementById("progress-fill");
    
    if (fill){
        const percentage = Number(fill.dataset.percentage || 0);

        let width = 0;

        const interval = setInterval(() => {
            if (width >= percentage) {
                clearInterval(interval);
            } else {
                width++;
                fill.style.width = width + "%";
            }
        }, 10); // Speed of animation
    }

    // Hide mood environment container initially
    document.getElementById("mood-env-container").style.display = "none";


    if (globalBtn && moodEnvContainer) {
        globalBtn.addEventListener("click", () => {
            console.log("Mood button clicked!");

            document.getElementById("main-dashboard-content").style.display = "none";
            
            // Hide Focus button itself
            document.getElementById("mood-env-form").style.display = "none";

            // Show mood environment container 
            moodEnvContainer.style.display = "block";

            // Display Mood Selection Screen 
            moodEnvContainer.innerHTML = `
                <div id="welcome-screen" class="welcome-screen">
                    <h1>Welcome to your Mood-Based Environment</h1>
                    <p>Select your current mood:</p>
                    
                 
                    <div class="mood-bubbles">
                            <div class="bubble" data-mood="stressed">😖 Stressed</div>
                            <div class="bubble" data-mood="sleepy">😴 Sleepy</div>
                            <div class="bubble" data-mood="motivated">💪 Motivated</div>
                            <div class="bubble" data-mood="overwhelmed">😵 Overwhelmed</div>
                            <div class="bubble" data-mood="calm">😌 Calm</div>
                    </div>

                    <button id="back-to-dashboard">Back to Dashboard</button>
                </div>
            `;

            // Attach Bubble click listeners
            const bubbles = moodEnvContainer.querySelectorAll(".bubble");
            bubbles.forEach(bubble => {
                bubble.addEventListener("click", () => {
                    const mood = bubble.dataset.mood;
                    console.log("Bubble clicked:", mood);
                    applyMood(mood);
                });
            });

            // Attach dashboard back button listener 
            const backBtn = document.getElementById("back-to-dashboard");

            backBtn.addEventListener("click", () => {

                // Hide mood screen
                moodEnvContainer.style.display = "none";

                // Show dashboard content again
                document.getElementById("main-dashboard-content").style.display = "block";

                // Show Focus button again
                document.getElementById("mood-env-form").style.display = "block";
            })

        });
    }
});

function applyMood(mood) {
    const container = document.getElementById("mood-env-container");
    const rec = moodRecommendations[mood];
    const timerSound = document.getElementById("timer-sound");

    const timerFormats = {
        pomodoro: { work: 25*60, break: 5*60 },
        micro: { work: 10*60, break: 2*60},
        deep: { work: 50*60, break: 10*60}
    };

    // Hide dashboard only
    document.getElementById("main-dashboard-content").style.display = "none";
    document.getElementById("mood-env-form").style.display = "none";

    // Show container
    container.style.display = "block";

    // Reset previous class
    container.className = ""; // reset
    container.classList.add(`mood-${mood}`, "animated-bg");
    
    // Add environment content 
    container.innerHTML = `
        <div id="environment-content" class="environment-content">
            <h1>${mood.charAt(0).toUpperCase() + mood.slice(1)} Mode</h1>

            <div id="timer-container">
                <h3>Timer</h3>
                <div id="timer-display">00:00</div>               
                <div id="timer-controls">
                    <button id="start-btn">Start</button>
                    <button id="pause-btn">Pause</button>
                    <button id="reset-btn">Reset</button>
                </div>
            </div>

            <h3>Recommended Playlists</h3>
            <div id="playlist-cards"></div>

            <button id="back-btn">Back to Mood Selection</button>
        </div>
    `;

    const playlistCardsContainer = document.getElementById("playlist-cards");

    // Clear any previous cards
    playlistCardsContainer.innerHTML = "";

    // Get playlist keys for this mood
    const moodPlaylist = rec.playlist;

    moodPlaylist.forEach(playlistKey => {
        const category = playlistCategories[playlistKey];

        const card = document.createElement("div");
        card.classList.add("playlist-card");

        // Embed playlists
        card.innerHTML = `
            <h4>${category.title}</h4>
            <p>${category.description}</p>
            <span>${category.bpm}</span>
            <iframe src="${category.embed}" width="100%" height="80" frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>              
        `;
        
        playlistCardsContainer.appendChild(card);
    });

    // Floating circles container
    const bubblesContainer = document.createElement("div");
    bubblesContainer.id = "floating-circles";
    container.appendChild(bubblesContainer);

    // Create 10 floating circles
    for (let i = 0; i < 10; i++) {
        const circle = document.createElement("div");
        circle.classList.add("floating-circle");

        // Randomize size
        const size = Math.random() * 40 + 20; // 20px to 60px
        circle.style.width = `${size}px`;
        circle.style.height = `${size}px`;

        // Randomize animation duration
        const duration = Math.random() * 5 + 3;
        circle.style.animationDuration = `${duration}s`;

        // Randomize initial position
        circle.style.left = `${Math.random() * 100}%`;
        circle.style.top = `${Math.random() * 100}%`;

        bubblesContainer.appendChild(circle);
        }

    // ----Timer Logic-----
    // Set preset timer based on mood
    currentFormat = rec.timer.includes("micro") ? "micro" :
                    rec.timer.includes("deep") ? "deep" : "pomodoro";
    
    // Set timer duration to the work phase of this format
    timerDuration = timerFormats[currentFormat].work;

    // Reset timer state 
    isRunning = false;
    isWorkPhase = true;

    // Initialize timer variables
    const timerDisplay = document.getElementById("timer-display"); 
    const startBtn = document.getElementById("start-btn");
    const pauseBtn = document.getElementById("pause-btn");
    const resetBtn = document.getElementById("reset-btn");

    // Show initial timer
    timerDisplay.textContent = formatTime(timerDuration);

    // Start button
    startBtn.addEventListener("click", () => {
        // Decrease the timer if there are still seconds left
        if (!isRunning) {
            isRunning = true;
            timerInterval = setInterval(() => {
                if (timerDuration > 0){
                    timerDuration--;
                    timerDisplay.textContent = formatTime(timerDuration);

                } else {
                    clearInterval(timerInterval);
                    isRunning = false;

                    // Alert user that time ended
                    timerSound.play(); 
                    alert("Time is up!");

                    // Switch phase
                    isWorkPhase = !isWorkPhase;
                    timerDuration = isWorkPhase  ? timerFormats[currentFormat].work
                                                : timerFormats[currentFormat].break;
                    
                    timerDisplay.textContent = formatTime(timerDuration);

                }
            }, 1000);
        }
    });

    // Pause button
    pauseBtn.addEventListener("click", () => {
        if(isRunning) {
            clearInterval(timerInterval);
            isRunning = false;
        }
    });

    // Reset button
    resetBtn.addEventListener("click", () => {
        clearInterval(timerInterval);
        isRunning = false;
        isWorkPhase = true;
        timerDuration = timerFormats[currentFormat].work;
        timerDisplay.textContent = formatTime(timerDuration);
    });


    // Add a back button listerner
   document.getElementById("back-btn").addEventListener("click", () => {

    container.className = "";

    // Rebuild mood selection screen 
    container.innerHTML = `
        <div id="welcome-screen" class="welcome-screen">
            <h1>Welcome to your Mood-Based Environment</h1>
            <p>Select your current mood:</p>
                                     
            <div class="mood-bubbles">
                <div class="bubble" data-mood="stressed">😖 Stressed</div>
                <div class="bubble" data-mood="sleepy">😴 Sleepy</div>
                <div class="bubble" data-mood="motivated">💪 Motivated</div>
                <div class="bubble" data-mood="overwhelmed">😵 Overwhelmed</div>
                <div class="bubble" data-mood="calm">😌 Calm</div>
            </div>

            <button id="back-to-dashboard">Back to Dashboard</button>
        </div>
    `;

    // Reattach bubble listeners
    const bubbles = container.querySelectorAll(".bubble");
    bubbles.forEach(bubble => {
        bubble.addEventListener("click", () => {
            const mood = bubble.dataset.mood;
            applyMood(mood);
        });
    });

    // Reattach dashboard back button
    document.getElementById("back-to-dashboard").addEventListener("click", () => {
        container.style.display = "none";
        document.getElementById("main-dashboard-content").style.display = "block";
        document.getElementById("mood-env-form").style.display = "block";
    })
    
    });


}

// Function to format seconds into MM:SS
function formatTime(seconds) {
    const m = Math.floor(seconds / 60).toString().padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
}
