'use strict';

// Select2 (jquery)
$(function () {
  var select2 = $('.select2');
  // For all Select2
  if (select2.length) {
    select2.each(function () {
      var $this = $(this);
      $this.wrap('<div class="position-relative"></div>');
      $this.select2({
        dropdownParent: $this.parent()
      });
    });
  }
});

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    // Profile form
    const personal_information_form = document.querySelector('#personal_information_form');
    const company_information_form = document.querySelector('#company_informaiton_form');

    // Initialize validation for both forms
    if (personal_information_form && company_information_form) {
      // Form validation for Personal Information Form
      const personalFormValidation = FormValidation.formValidation(personal_information_form, {
        fields: {
          multiStepsFirstName: {
            validators: {
              notEmpty: {
                message: 'First name is required'
              }
            }
          },
          multiStepsLastName: {
            validators: {
              notEmpty: {
                message: 'Last name is required'
              }
            }
          },
          multiStepsEmail: {
            validators: {
              notEmpty: {
                message: 'Email is required'
              },
              emailAddress: {
                message: 'Please enter a valid email address'
              }
            }
          },
          multiStepsMobile: {
            validators: {
              notEmpty: {
                message: 'Mobile number is required'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.col-sm-6'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        }
      });

      // Form validation for Company Information Form
      const companyFormValidation = FormValidation.formValidation(company_information_form, {
        fields: {
          multiStepsCompanyName: {
            validators: {
              notEmpty: {
                message: 'Company name is required'
              }
            }
          },
          multiStepsCompanyWebsite: {
            validators: {
              notEmpty: {
                message: 'Company website is required'
              },
              uri: {
                message: 'Please enter a valid URL'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.col-md-12'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        }
      });

      // Image upload and reset for Personal Information Form
      let accountUserImage = document.getElementById('uploadedAvatar');
      const fileInput = document.querySelector('.account-file-input'),
        resetFileInput = document.querySelector('.account-image-reset');

      if (accountUserImage) {
        const resetImage = accountUserImage.src;
        fileInput.onchange = () => {
          if (fileInput.files[0]) {
            accountUserImage.src = window.URL.createObjectURL(fileInput.files[0]);
          }
        };
        resetFileInput.onclick = () => {
          fileInput.value = '';
          accountUserImage.src = resetImage;
        };
      }

      // Submit Button Handling
      document.querySelector('#personal_information_form').onsubmit = function (e) {
        e.preventDefault();
        personalFormValidation.validate().then(function (status) {
          if (status === 'Valid') {
            // Handle valid form submission here
            alert('Personal Information Form is valid');
          }
        });
      };

      document.querySelector('#company_informaiton_form').onsubmit = function (e) {
        e.preventDefault();
        companyFormValidation.validate().then(function (status) {
          if (status === 'Valid') {
            // Handle valid form submission here
            alert('Company Information Form is valid');
          }
        });
      };
    }
  })();
});
