/**
 *  Page auth register multi-steps
 */

'use strict';

// Select2 (jquery)
$(function() {
    var select2 = $('.select2');

    // select2
    if (select2.length) {
        select2.each(function() {
            var $this = $(this);
            $this.wrap('<div class="position-relative"></div>');
            $this.select2({
                placeholder: 'Select an country',
                dropdownParent: $this.parent()
            });
        });
    }
});

//* ------------------|| Multi Steps Validation ||--------------------------
document.addEventListener('DOMContentLoaded', function(e) {
    (function() {
        const stepsValidation = document.querySelector('#multiStepsValidation');
        if (typeof stepsValidation !== undefined && stepsValidation !== null) {
            // Multi Steps form
            const stepsValidationForm = stepsValidation.querySelector('#multiStepsForm');
            // Form steps
            const stepsValidationFormStep1 = stepsValidationForm.querySelector('#personalInfoValidation');
            const stepsValidationFormStep2 = stepsValidationForm.querySelector('#educationDetailValidation');
            const stepsValidationFormStep3 = stepsValidationForm.querySelector('#experienceDetailValidation');
            const stepsValidationFormStep4 = stepsValidationForm.querySelector('#candidateInfoValidation');
            // Multi steps next prev button
            const stepsValidationNext = [].slice.call(stepsValidationForm.querySelectorAll('.btn-next'));
            const stepsValidationPrev = [].slice.call(stepsValidationForm.querySelectorAll('.btn-prev'));

            let validationStepper = new Stepper(stepsValidation, {
                linear: true
            });

            // Personal Info
            const multiSteps1 = FormValidation.formValidation(stepsValidationFormStep1, {
                fields: {
                    multiStepsFirstName: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your first name'
                            }
                        }
                    },
                    multiStepsLastName: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your last name'
                            }
                        }
                    },
                    multiStepsEmail: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your email address'
                            },
                            emailAddress: {
                                message: 'Please enter a valid email address'
                            }
                        }
                    },
                    multiStepsPass: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter password'
                            }
                        }
                    },
                    multiStepsConfirmPass: {
                        validators: {
                            notEmpty: {
                                message: 'Confirm Password is required'
                            },
                            identical: {
                                compare: function() {
                                    return stepsValidationFormStep1.querySelector('[name="multiStepsPass"]').value;
                                },
                                message: 'The password and its confirm are not the same'
                            }
                        }
                    },
                    multiStepsCity: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your city'
                            }
                        }
                    },
                    multiStepsCountry: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your country'
                            }
                        }
                    },
                    multiStepsMobile: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter mobile number',
                                callback: function(value, validator, $field) {
                                    // Ensure that the value is selected and not empty
                                    return value !== '';
                                }
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap5: new FormValidation.plugins.Bootstrap5({
                        // Use this for enabling/changing valid/invalid class
                        // eleInvalidClass: '',
                        eleValidClass: '',
                        // rowSelector: '.col-sm-6'
                    }),
                    autoFocus: new FormValidation.plugins.AutoFocus(),
                    submitButton: new FormValidation.plugins.SubmitButton()
                },
                init: instance => {
                    instance.on('plugins.message.placed', function(e) {
                        if (e.element.parentElement.classList.contains('input-group')) {
                            e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
                        }
                    });
                }
            }).on('core.form.valid', function() {
                // Jump to the next step when all fields in the current step are valid
                validationStepper.next();
            });

            // Education Details
            const multiSteps2 = FormValidation.formValidation(stepsValidationFormStep2, {
                fields: {
                    multiStepsInstitute: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter the institute name'
                            }
                        }
                    },
                    multiStepsProgram: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter the program name'
                            }
                        }
                    },
                    multiStepsStartDate: {
                        validators: {
                            notEmpty: {
                                message: 'Please select a start date'
                            },
                            date: {
                                format: 'YYYY-MM-DD',
                                message: 'The start date is not valid'
                            }
                        }
                    },
                    multiStepsEndDate: {
                        validators: {
                            notEmpty: {
                                message: 'Please select an end date'
                            },
                            date: {
                                format: 'YYYY-MM-DD',
                                message: 'The end date is not valid'
                            },
                            callback: {
                                message: 'End date must be after the start date',
                                callback: function(input) {
                                    const startDate = stepsValidationFormStep2.querySelector('[name="multiStepsStartDate"]').value;
                                    const endDate = input.value;
                                    return startDate === '' || endDate === '' || new Date(endDate) > new Date(startDate);
                                }
                            }
                        }
                    },
                    multiStepsDegree: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter the degree'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap5: new FormValidation.plugins.Bootstrap5({
                        // Use this for enabling/changing valid/invalid class
                        // eleInvalidClass: '',
                        eleValidClass: '',
                        rowSelector: function(field, ele) {
                            // field is the field name
                            // ele is the field element
                            switch (field) {
                                case 'multiStepsInstitute':
                                case 'multiStepsProgram':
                                case 'multiStepsDegree':
                                    return '.col-md-12';
                                case 'multiStepsStartDate':
                                case 'multiStepsEndDate':
                                    return '.col-sm-6';
                                default:
                                    return '.row';
                            }
                        }
                    }),
                    autoFocus: new FormValidation.plugins.AutoFocus(),
                    submitButton: new FormValidation.plugins.SubmitButton()
                }
            }).on('core.form.valid', function() {
                // Jump to the next step when all fields in the current step are valid
                validationStepper.next();
            });

            // Experience Details
            const multiSteps3 = FormValidation.formValidation(stepsValidationFormStep3, {
                fields: {
                    multiStepsWorkplace: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter the workplace name'
                            }
                        }
                    },
                    multiStepsDesignation: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter the designation'
                            }
                        }
                    },
                    multiStepsStartDate: {
                        validators: {
                            notEmpty: {
                                message: 'Please select a start date'
                            },
                            date: {
                                format: 'YYYY-MM-DD',
                                message: 'The start date is not valid'
                            }
                        }
                    },
                    multiStepsEndDate: {
                        validators: {
                            notEmpty: {
                                message: 'Please select an end date'
                            },
                            date: {
                                format: 'YYYY-MM-DD',
                                message: 'The end date is not valid'
                            },
                            callback: {
                                message: 'End date must be after the start date',
                                callback: function(input) {
                                    const startDate = document.getElementById('multiStepsStartDate').value;
                                    const endDate = input.value;
                                    return startDate === '' || endDate === '' || new Date(endDate) > new Date(startDate);
                                }
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap5: new FormValidation.plugins.Bootstrap5({
                        // Use this for enabling/changing valid/invalid class
                        // eleInvalidClass: '',
                        eleValidClass: '',
                        rowSelector: function(field, ele) {
                            // field is the field name
                            // ele is the field element
                            switch (field) {
                                case 'multiStepsWorkplace':
                                case 'multiStepsDesignation':
                                    return '.col-md-12';
                                case 'multiStepsStartDate':
                                case 'multiStepsEndDate':
                                    return '.col-sm-6';
                                default:
                                    return '.row';
                            }
                        }
                    }),
                    autoFocus: new FormValidation.plugins.AutoFocus(),
                    submitButton: new FormValidation.plugins.SubmitButton()
                }
            }).on('core.form.valid', function() {
                // Jump to the next step when all fields in the current step are valid
                validationStepper.next();
            });

            // Candidate Info
            const multiSteps4 = FormValidation.formValidation(stepsValidationFormStep4, {
                fields: {
                    multiStepsLinkedin: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your LinkedIn profile URL'
                            },
                            uri: {
                                message: 'Please enter a valid URL for your LinkedIn profile'
                            }
                        }
                    },
                    multiStepsGithub: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your GitHub profile URL'
                            },
                            uri: {
                                message: 'Please enter a valid URL for your GitHub profile'
                            }
                        }
                    },
                    multiStepsUploadCV: {
                        validators: {
                            notEmpty: {
                                message: 'Please upload your CV'
                            },
                            file: {
                                extension: 'pdf',
                                type: 'application/pdf',
                                maxSize: 20 * 1024 * 1024, // 20 MB limit
                                message: 'Please upload a valid PDF file with a maximum size of 20 MB'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap5: new FormValidation.plugins.Bootstrap5({
                        // Use this for enabling/changing valid/invalid class
                        // eleInvalidClass: '',
                        eleValidClass: '',
                        rowSelector: function(field, ele) {
                            // field is the field name
                            // ele is the field element
                            switch (field) {
                                case 'multiStepsLinkedin':
                                case 'multiStepsGithub':
                                case 'multiStepsUploadCV':
                                    return '.col-md-12';
                                default:
                                    return '.col-dm-6';
                            }
                        }
                    }),
                    autoFocus: new FormValidation.plugins.AutoFocus(),
                    submitButton: new FormValidation.plugins.SubmitButton()
                },
                init: instance => {
                    instance.on('plugins.message.placed', function(e) {
                        if (e.element.parentElement.classList.contains('input-group')) {
                            e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
                        }
                    });
                }
            }).on('core.form.valid', function() {
                // You can submit the form
                // stepsValidationForm.submit()
                // or send the form data to server via an Ajax request
                // To make the demo simple, I just placed an alert
                alert('Submitted..!!');
            });

            stepsValidationNext.forEach(item => {
                item.addEventListener('click', event => {
                    // When click the Next button, we will validate the current step
                    switch (validationStepper._currentIndex) {
                        case 0:
                            multiSteps1.validate();
                            break;

                        case 1:
                            multiSteps2.validate();
                            break;

                        case 2:
                            multiSteps3.validate();
                            break;

                        case 3:
                            multiSteps4.validate();
                            break;

                        default:
                            break;
                    }
                });
            });

            stepsValidationPrev.forEach(item => {
                item.addEventListener('click', event => {
                    switch (validationStepper._currentIndex) {
                        case 3:
                            validationStepper.previous();
                            break;

                        case 2:
                            validationStepper.previous();
                            break;

                        case 1:
                            validationStepper.previous();
                            break;

                        case 0:

                        default:
                            break;
                    }
                });
            });
        }
    })();
});
//* -------------------------------------------------------------------------




//* ------------------- Screens Steps Count Logic.----------------------
document.getElementById("multiStepsForm").onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission

    // Send form data via AJAX
    var formData = new FormData(this);
    var currentStep = new URLSearchParams(window.location.search).get('step') || '1';

    fetch(`?step=${currentStep}`, {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Redirect to the next step based on response
            window.location.href = `?step=${data.next_step}`;
        } else {
            // Display form errors
            console.error('Form submission failed', data.errors);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// document.getElementById("multiStepsForm").onsubmit = function(event) {
//     event.preventDefault(); // Prevent the default form submission

//     var formData = new FormData(this);
    
//     fetch("{% url 'create_account_step' step=1 %}", {
//         method: "POST",
//         body: formData,
//         headers: {
//             'X-CSRFToken': '{{ csrf_token }}',
//         }
//     })
//     .then(response => {
//         if (response.ok) {
//             return response.json();
//         } else {
//             throw new Error('Something went wrong with the request.');
//         }
//     })
//     .then(data => {
//         if (data.status === 'error') {
//             // Display an alert or dialog if the email already exists
//             alert(data.message);  // Replace this with your preferred dialog library if needed
//         } else {
//             // Redirect to the next step if no error
//             window.location.href = "{% url 'create_account_step' step=2 %}";
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// };
//* -------------------------------------------------------------------


