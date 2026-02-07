console.log("JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    // Set initial streak bar width on page load
    const streakProgress = document.getElementById('streak-progress');

    if (streakProgress) {
        // Get streak number from HTML dataset
        const streakCount = parseInt(streakProgress.dataset.streak) || 0;

        // Convert streak into percent (7-day goal)
        const percent = Math.min((streakCount / 7) * 100, 100);

        // Apply width to the green bar
        streakProgress.style.width = percent + "%";

    }

    // Get all task checkboxes
    const checkboxes = document.querySelectorAll(".task-checkbox");

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const taskLogId = checkbox.dataset.taskLogId;

            fetch("/toggle-task/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ "task_log_id": taskLogId})
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error)
                    return;
                }
                
                console.log("Task updated:", data.completed);
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // "Done for the Day" button logic
    const doneDayBtn = document.getElementById("done-day-btn");
    const doneMessage = document.getElementById("done-message");

    if (doneDayBtn) {
        doneDayBtn.addEventListener("click", () => {
            fetch("/complete-day/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update streak number
                    document.getElementById("streak-count").textContent = data.streak;

                    // Update streak progress bar
                    const percent = Math.min((data.streak / 7) * 100, 100);
                    streakProgress.style.width = percent + "%";

                    // Show success message breifly
                    doneMessage.textContent = "🎉 Congratulations, you've completed your tasks!";
                    setTimeout(() => doneMessage.textContent = "", 2000);

                } else {
                    doneMessage.textContent = data.message;
                    setTimeout(() => doneMessage.textContent = "", 2000);
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    }
});

// Helper function to get CSRF token from cookies 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i=0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
            
}
