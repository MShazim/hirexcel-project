
// Enable buttons when an option is selected
document.querySelectorAll('input[name="option"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
        if (nextQuestionBtn) nextQuestionBtn.disabled = false;
        if (doneButton) doneButton.disabled = false;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('technical-quiz-form');
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
        // let timeTaken = 0;
        timerInterval = setInterval(function () {
            if (timerDuration > 0) {
                timerDuration--;
                timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
            } else {
                clearInterval(timerInterval);
                submitFormWithDefaultAnswer();
            }
        }, 1000);
    }

    // Auto-submit form with "nan" if timer runs out
    function submitFormWithDefaultAnswer() {
        document.getElementById('question-time-input').value = 60;  // Default full time
        // Set default value for option to "nan"
        const hiddenNanInput = document.createElement('input');
        hiddenNanInput.setAttribute('type', 'hidden');
        hiddenNanInput.setAttribute('name', 'option');
        hiddenNanInput.setAttribute('value', 'nan');
        form.appendChild(hiddenNanInput);
        form.submit();
    }

    // Handle click events for Next and Done buttons
    if (nextQuestionBtn) {
        nextQuestionBtn.addEventListener('click', function () {
            handleSubmitForm();
        });
    }

    if (doneButton) {
        doneButton.addEventListener('click', function () {
            handleSubmitForm();
        });
    }

    // Function to handle form submission
    function handleSubmitForm() {
        clearInterval(timerInterval); // Stop the timer
        const timeTaken = 60 - timerDuration;
        document.getElementById('question-time-input').value = timeTaken; // Set the actual time taken
        form.submit(); // Manually submit the form
    }

    // Start the timer
    startTimer();
});
