
  document.addEventListener('DOMContentLoaded', function() {
    // Listen for click on any "Start Quiz" button
    document.querySelectorAll('.viewjob-list').forEach(button => {
      button.addEventListener('click', function() {
        // Retrieve data attributes from the clicked button
        const jobTitle = this.getAttribute('data-job-title');
        const companyName = this.getAttribute('data-company-name');
        const jobDescription = this.getAttribute('data-job-description');
        const jobPosition = this.getAttribute('data-job-position');

        // Set the modal content
        document.querySelector('#hirexcel_quizzes_modal .modal-title').textContent = jobTitle;
        document.querySelector('#hirexcel_quizzes_modal .job-title').textContent = jobTitle;
        document.querySelector('#hirexcel_quizzes_modal .company-name').textContent = companyName;
        document.querySelector('#hirexcel_quizzes_modal .job-description').textContent = jobDescription;
      });
    })
  });
