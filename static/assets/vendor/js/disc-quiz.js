// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('disc-assessment-form');
//     const nextQuestionBtn = document.getElementById('next-question-btn');
//     const doneButton = document.getElementById('done-button');
//     let timerDuration = 30; // 30 seconds for the timer
//     let timerElement = document.getElementById('timer');

//     // Enable button when a radio option is selected
//     document.querySelectorAll('input[type="radio"]').forEach(function (radio) {
//         radio.addEventListener('change', function () {
//             if (nextQuestionBtn) nextQuestionBtn.disabled = false;
//             if (doneButton) doneButton.disabled = false;
//         });
//     });

//     // Timer Logic
//     let timerInterval = setInterval(function () {
//         if (timerDuration > 0) {
//             timerDuration--;
//             // Display minutes and seconds
//             timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
//         } else {
//             clearInterval(timerInterval);
//             // Enable buttons when time runs out
//             if (nextQuestionBtn) nextQuestionBtn.disabled = false;
//             if (doneButton) doneButton.disabled = false;
//         }
//     }, 1000);

//     // Handle 'Next Question' button click to submit form manually
//     if (nextQuestionBtn) {
//         nextQuestionBtn.addEventListener('click', function () {
//             document.getElementById('question-time-input').value = 30 - timerDuration;
//             form.submit();
//         });
//     }

//     // Handle 'Done' button click to submit form manually
//     if (doneButton) {
//         doneButton.addEventListener('click', function () {
//             document.getElementById('question-time-input').value = 30 - timerDuration;
//             form.submit();
//         });
//     }
// });


// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('disc-assessment-form');
//     const nextQuestionBtn = document.getElementById('next-question-btn');
//     const doneButton = document.getElementById('done-button');
//     const loadingOverlay = document.getElementById('loading-overlay');
//     let timerDuration = 30; // 30 seconds for the timer
//     let timerElement = document.getElementById('timer');

//     // Enable button when a radio option is selected
//     document.querySelectorAll('input[type="radio"]').forEach(function (radio) {
//         radio.addEventListener('change', function () {
//             if (nextQuestionBtn) nextQuestionBtn.disabled = false;
//             if (doneButton) doneButton.disabled = false;
//         });
//     });

//     // Timer Logic
//     let timerInterval = setInterval(function () {
//         if (timerDuration > 0) {
//             timerDuration--;
//             // Display minutes and seconds
//             timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
//         } else {
//             clearInterval(timerInterval);
//             // Enable buttons when time runs out
//             if (nextQuestionBtn) nextQuestionBtn.disabled = false;
//             if (doneButton) doneButton.disabled = false;
//         }
//     }, 1000);

//     // Handle 'Next Question' button click to submit form manually
//     if (nextQuestionBtn) {
//         nextQuestionBtn.addEventListener('click', function () {
//             document.getElementById('question-time-input').value = 30 - timerDuration;
//             form.submit();
//         });
//     }

//     // Handle 'Done' button click to show the loading overlay and submit form
//     if (doneButton) {
//         doneButton.addEventListener('click', function (event) {
//             event.preventDefault(); // Prevent default button behavior

//             // Show loading overlay
//             loadingOverlay.style.display = 'flex';

//             // Set question time value and submit form
//             document.getElementById('question-time-input').value = 30 - timerDuration;
//             form.submit();
//         });
//     }
// });


// ----------------------------------------------------------------------------------------------

// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('disc-assessment-form');
//     const nextQuestionBtn = document.getElementById('next-question-btn');
//     const doneButton = document.getElementById('done-button');
//     let timerDuration = 30; // 30 seconds for the timer
//     let timerElement = document.getElementById('timer');
//     let timerInterval;

//     // Enable button when a radio option is selected
//     document.querySelectorAll('input[type="radio"]').forEach(function (radio) {
//         radio.addEventListener('change', function () {
//             if (nextQuestionBtn) nextQuestionBtn.disabled = false;
//             if (doneButton) doneButton.disabled = false;
//         });
//     });

//     // Timer Logic
//     function startTimer() {
//         let timeTaken = 0;
//         timerInterval = setInterval(function () {
//             if (timerDuration > 0) {
//                 timerDuration--;
//                 timeTaken++;
//                 // Display minutes and seconds
//                 timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
//             } else {
//                 clearInterval(timerInterval);
//                 autoSubmitFormAsNan(timeTaken);
//             }
//         }, 1000);
//     }

//     // Auto-submit form with "nan" if timer runs out
//     function autoSubmitFormAsNan(timeTaken) {
//         // Mark "nan" for no selection
//         const hiddenInput = document.createElement('input');
//         hiddenInput.type = 'hidden';
//         hiddenInput.name = 'selected_option';
//         hiddenInput.value = 'nan';
//         form.appendChild(hiddenInput);

//         // Set question time taken
//         document.getElementById('question-time-input').value = timeTaken;

//         // Submit form
//         form.submit();
//     }

//     // Handle 'Next Question' button click to submit form manually
//     if (nextQuestionBtn) {
//         nextQuestionBtn.addEventListener('click', function () {
//             document.getElementById('question-time-input').value = 30 - timerDuration;
//             form.submit();
//         });
//     }

//     // Handle 'Done' button click to submit form manually
//     if (doneButton) {
//         doneButton.addEventListener('click', function () {
//             document.getElementById('question-time-input').value = 30 - timerDuration;
//             form.submit();
//         });
//     }

//     // Start the timer
//     startTimer();
// });

// ----------------------------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('disc-assessment-form');
    const nextQuestionBtn = document.getElementById('next-question-btn');
    const doneButton = document.getElementById('done-button');
    let timerDuration = 30; // 30 seconds for the timer
    let timerElement = document.getElementById('timer');
    let timerInterval;

    // Disable buttons initially
    if (nextQuestionBtn) nextQuestionBtn.disabled = true;
    if (doneButton) doneButton.disabled = true;

    // Enable button when a radio option is selected
    document.querySelectorAll('input[type="radio"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            // Enable the appropriate button based on if it's the last question or not
            if (nextQuestionBtn) nextQuestionBtn.disabled = false;
            if (doneButton) doneButton.disabled = false;
        });
    });

    // Timer Logic
    function startTimer() {
        let timeTaken = 0;
        timerInterval = setInterval(function () {
            if (timerDuration > 0) {
                timerDuration--;
                timeTaken++;
                // Display minutes and seconds
                timerElement.innerHTML = `00:${timerDuration < 10 ? '0' : ''}${timerDuration}`;
            } else {
                clearInterval(timerInterval);
                autoSubmitFormAsNan(timeTaken);
            }
        }, 1000);
    }

    // Auto-submit form with "nan" if timer runs out
    function autoSubmitFormAsNan(timeTaken) {
        // Set "nan" for no selection
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'selected_option';
        hiddenInput.value = 'nan';
        form.appendChild(hiddenInput);

        // Set question time taken
        document.getElementById('question-time-input').value = timeTaken;

        // Submit form
        form.submit();
    }

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

    // Start the timer
    startTimer();
});
