document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('disc-assessment-form');
    const nextQuestionBtn = document.getElementById('next-question-btn');
    const doneButton = document.getElementById('done-button');
    let timerDuration = 30; // 30 seconds for the timer
    let timerElement = document.getElementById('timer');

    // Enable button when a radio option is selected
    document.querySelectorAll('input[type="radio"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            if (nextQuestionBtn) nextQuestionBtn.disabled = false;
            if (doneButton) doneButton.disabled = false;
        });
    });

    // Timer Logic
    let timerInterval = setInterval(function () {
        if (timerDuration > 0) {
            timerDuration--;
            // Display minutes and seconds
            timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
        } else {
            clearInterval(timerInterval);
            // Enable buttons when time runs out
            if (nextQuestionBtn) nextQuestionBtn.disabled = false;
            if (doneButton) doneButton.disabled = false;
        }
    }, 1000);

    // Handle 'Next Question' button click to submit form manually
    if (nextQuestionBtn) {
        nextQuestionBtn.addEventListener('click', function () {
            document.getElementById('question-time-input').value = 30 - timerDuration;
            form.submit();
        });
    }

    // Handle 'Done' button click to submit form manually
    if (doneButton) {
        doneButton.addEventListener('click', function () {
            document.getElementById('question-time-input').value = 30 - timerDuration;
            form.submit();
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const proceedBtn = document.getElementById('modal-proceed-btn');
    
    if (proceedBtn) {
        proceedBtn.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the button's default behavior (i.e., form submission or link navigation)

            // Make an AJAX POST request to populate the DISC_Assessment_Result table
            fetch('{% url "populate_disc_result" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',  // Use Django's CSRF token
                },
                body: JSON.stringify({
                    disc_assessment_id: '{{ request.session.DISC_ASSESSMENT_ID }}'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Redirect to the Big Five quiz start
                    window.location.href = "{% url 'big_five_quiz_start' %}";
                } else {
                    // Handle error case
                    console.error('Error populating DISC result:', data.message);
                    alert('An error occurred while processing the results. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An unexpected error occurred. Please try again.');
            });
        });
    }
});

