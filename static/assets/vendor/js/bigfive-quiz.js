const circles = document.querySelectorAll('.circle-rating-item');

circles.forEach(circle => {

    circle.addEventListener('click', function () {
        const rating = this.getAttribute('data-rating');

        circles.forEach(c => c.querySelector('.circle').classList.remove('bg-primary'));

        circles.forEach(c => {
            if (c.getAttribute('data-rating') <= rating) {
                c.querySelector('.circle').classList.add('bg-primary');
            }
        });

        console.log(`You selected rating: ${rating}`);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('big-five-assessment-form');
    const nextQuestionBtn = document.getElementById('next-question-btn');
    const doneButton = document.getElementById('done-button');
    const timerElement = document.getElementById('timer');
    let timerDuration = 30; // Timer set for 30 seconds
    let timeTaken = 0; // Track time taken for the question
    let timerInterval;

    // Enable button when a rating is selected
    document.querySelectorAll('.circle-rating-item').forEach(function (circle) {
        circle.addEventListener('click', function () {
            const rating = this.getAttribute('data-rating');
            document.getElementById('selected_option').value = rating;

            // Update styles for selected option
            document.querySelectorAll('.circle').forEach(c => c.classList.remove('bg-primary'));
            this.querySelector('.circle').classList.add('bg-primary');

            // Enable buttons after selection
            if (nextQuestionBtn) nextQuestionBtn.disabled = false;
            if (doneButton) doneButton.disabled = false;
        });
    });

    // Timer Logic
    function startTimer() {
        timerInterval = setInterval(function () {
            if (timerDuration > 0) {
                timerDuration--;
                timeTaken++;
                timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
            } else {
                clearInterval(timerInterval);
                submitFormWithDefaultAnswer();
            }
        }, 1000);
    }

    // Auto-submit form with "0" if timer runs out
    function submitFormWithDefaultAnswer() {
        document.getElementById('selected_option').value = '0';  // Default answer
        document.getElementById('question-time').value = timeTaken; // Set time taken
        form.submit();
    }

    // Handle 'Next Question' button click
    if (nextQuestionBtn) {
        nextQuestionBtn.addEventListener('click', function () {
            document.getElementById('question-time').value = timeTaken; // Set time taken
            form.submit();
        });
    }

    // Handle 'Done' button click
    if (doneButton) {
        doneButton.addEventListener('click', function () {
            document.getElementById('question-time').value = timeTaken; // Set time taken
            form.submit();
        });
    }

    // Start the timer
    startTimer();
});