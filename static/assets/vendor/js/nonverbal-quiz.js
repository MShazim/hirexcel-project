document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('non-verbal-quiz-form');
    const nextQuestionBtn = document.getElementById('next-question-btn');
    const doneButton = document.getElementById('done-button');
    const timerElement = document.getElementById('timer');
    let timerDuration = 60; // Timer set for 60 seconds
    let timerInterval;

    // Enable button when an option is selected
    document.querySelectorAll('input[name="option"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            if (nextQuestionBtn) nextQuestionBtn.disabled = false;
            if (doneButton) doneButton.disabled = false;
        });
    });

    // Timer Logic
    function startTimer() {
        timerInterval = setInterval(function () {
            if (timerDuration > 0) {
                timerDuration--;
                timerElement.textContent = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
            } else {
                clearInterval(timerInterval);
                submitFormWithDefaultAnswer();
            }
        }, 1000);
    }

    // Auto-submit form with "nan" if timer runs out
    function submitFormWithDefaultAnswer() {
        document.getElementById('time-taken-input').value = 60;  // Default full time
        form.submit();
    }

    // Handle form submission
    form.addEventListener('submit', function () {
        clearInterval(timerInterval); // Stop the timer
        const timeTaken = 60 - timerDuration;
        document.getElementById('time-taken-input').value = timeTaken; // Set the actual time taken
    });

    // Start the timer
    startTimer();
});
