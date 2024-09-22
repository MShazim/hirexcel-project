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

// Multi Steps Validation
// --------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function(e) {
    (function() {
        const stepsValidation = document.querySelector('#multiStepsValidation');
        if (typeof stepsValidation !== undefined && stepsValidation !== null) {
            // Multi Steps form
            const stepsValidationForm = stepsValidation.querySelector('#multiStepsForm');
            // Form steps
            const stepsValidationFormStep1 = stepsValidationForm.querySelector('#personalInfoValidation');
            const stepsValidationFormStep2 = stepsValidationForm.querySelector('#companyInfoValidation');
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

            // Candidate Info
            const multiSteps2 = FormValidation.formValidation(stepsValidationFormStep2, {
                fields: {
                    multiStepsCompanyName: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your company name'
                            }
                        }
                    },
                    multiStepsCompanyIndustry: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your industry'
                            }
                        }
                    },
                    multiStepsCompanySize: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your company size'
                            }
                        }
                    },
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
                                case 'multiStepsCompanyName':
                                case 'multiStepsCompanyIndustry':
                                case 'multiStepsCompanySize':
                                    return '.col-md-12';
                                default:
                                    return '.row';
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
                    console.log('Next button clicked. Current step:', validationStepper._currentIndex);
                    // When click the Next button, we will validate the current step
                    switch (validationStepper._currentIndex) {
                        case 0:
                            multiSteps1.validate();
                            break;

                        case 1:
                            multiSteps2.validate();
                            break;

                        default:
                            break;
                    }
                });
            });

            stepsValidationPrev.forEach(item => {
                item.addEventListener('click', event => {
                    switch (validationStepper._currentIndex) {
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