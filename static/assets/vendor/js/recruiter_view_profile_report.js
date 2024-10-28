document.addEventListener('DOMContentLoaded', function () {
    const viewReportButtons = document.querySelectorAll('button[data-assessment-id]');
    
    viewReportButtons.forEach(button => {
        button.addEventListener('click', function () {
            const assessmentId = this.getAttribute('data-assessment-id');
            console.log('Clicked button with assessment ID:', assessmentId); // Debug line

            if (assessmentId) {
                // Log the URL being fetched
                console.log('Fetching report data from:', `/get_report_data/?assessment_id=${assessmentId}`);
                
                fetch(`/get_report_data/?assessment_id=${assessmentId}`)
                    .then(response => {
                        // Log the status of the response
                        console.log('Response status:', response.status);
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Log the data received from the server
                        console.log('Fetched data:', data);

                        if (data.report_data) {
                            populateReportModal(data.report_data);
                            // Show the modal
                            const reportModal = new bootstrap.Modal(document.getElementById('view_report_modal'));
                            reportModal.show();

                            const modalElement = document.getElementById('view_report_modal');
                            modalElement.addEventListener('hidden.bs.modal', function () {
                                reportModal.dispose(); // Dispose the modal instance
                                const backdrop = document.querySelector('.modal-backdrop');
                                if (backdrop) {
                                    backdrop.remove();
                                }
                                document.body.classList.remove('modal-open');
                            });
                        } else {
                            console.error('No report data found:', data.error);
                        }
                    })
                    .catch(error => {
                        // Log any errors that occur during the fetch
                        console.error('Error fetching report data:', error);
                    });
            } else {
                console.error('No assessment ID found for the button clicked');
            }
        });
    });
});

function populateReportModal(data) {
    // Log data being used to populate the modal
    console.log('Populating modal with data:', data);

    // Populate the modal with the fetched data
    document.querySelector('#view_report_modal .modal-body').innerHTML = `
        <div class="row invoice-preview">
            <div class="col-xl-9 col-md-8 col-12 mb-md-0 mb-6">
                <div class="card invoice-preview-card p-sm-12 p-6">
                    <div class="card-body invoice-preview-header rounded">
                        <div class="d-flex justify-content-center">
                            <div class="mb-xl-0 mb-6 text-heading">
                                <div class="d-flex svg-illustration mb-6 gap-2 align-items-center">
                                    <div class="app-brand-logo demo">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 353.78 487.47">
                                            <g style="isolation: isolate;">
                                            <g id="Layer_2" data-name="Layer 2">
                                                <g id="OBJECTS">
                                                <g>
                                                    <g>
                                                    <path d="m353.78,131.18v178.34c-22.45-44.78-122.35-74.91-122.35-74.91v-117.55c0-70.95,101.99-83.97,118.85-15.05,2.29,9.35,3.5,19.12,3.5,29.17Z" style="fill: #7367f0;"/>
                                                    <path d="m0,366.49v-178.34c22.45,44.78,122.35,74.91,122.35,74.91v106.66c0,78.16-116.8,83.13-122.07,5.15-.19-2.77-.28-5.56-.28-8.38Z" style="fill: #7367f0;"/>
                                                    </g>
                                                    <path d="m353.77,247.77v47.58c-22.45-44.78-122.35-74.91-122.35-74.91v-52.94h.82c54.16,0,101.32,32.67,121.54,80.27Z" style="fill: #1f1e21; mix-blend-mode: overlay; opacity: .2;"/>
                                                    <path d="m0,239.69v-47.58c22.45,44.78,122.35,74.91,122.35,74.91v52.94h-.82c-54.16,0-101.32-32.67-121.54-80.27Z" style="fill: #1f1e21; mix-blend-mode: overlay; opacity: .2;"/>
                                                    <g>
                                                    <path d="m353.77,290.87v74.25c0,15.36-2.84,30.08-8.02,43.62-20.14-59.54-75.99-102.62-142.08-103.71-.85-.08-1.71-.12-2.58-.12h-78.89C56.73,304.91,3.28,253.5,0,188.85v-66.5c0-15.36,2.84-30.04,8-43.58,7.59,22.49,20.29,42.63,36.72,59.06,27.64,27.64,65.82,44.73,107.98,44.73h79.53c62.81,0,114.58,47.35,121.54,108.31Z" style="fill: #00b5e8;"/>
                                                    <path d="m353.77,290.87v74.25c0,15.36-2.84,30.08-8.02,43.62-20.14-59.54-75.99-102.62-142.08-103.71-.85-.08-1.71-.12-2.58-.12h-78.89C56.73,304.91,3.28,253.5,0,188.85v-66.5c0-15.36,2.84-30.04,8-43.58,7.59,22.49,20.29,42.63,36.72,59.06,27.64,27.64,65.82,44.73,107.98,44.73h79.53c62.81,0,114.58,47.35,121.54,108.31Z" style="fill: #7367f0;"/>
                                                    <path d="m353.77,290.87v14.16c-7.05-61.86-59.58-109.9-123.32-109.9h-80.69c-42.78,0-81.2-17.67-109.57-45.39C7.92,118.23,6.58,82.48,8,78.77c7.59,22.49,20.29,42.63,36.72,59.06,27.64,27.64,65.82,44.73,107.98,44.73h79.53c62.81,0,114.58,47.35,121.54,108.31Z" style="fill: #fff; mix-blend-mode: overlay; opacity: .5;"/>
                                                    <path d="m345.75,408.73c-7.26,19.07-19.17,35.85-34.34,48.96-21.44,18.55-49.41,29.77-79.99,29.77v-152.22c0-15.89-12.2-28.92-27.75-30.22,66.09,1.09,121.94,44.16,142.08,103.71Z" style="fill: #017dc0;"/>
                                                    </g>
                                                    <g>
                                                    <path d="m152.71,182.56c-42.16,0-80.34-17.09-107.98-44.73-16.43-16.43-29.13-36.57-36.72-59.06,7.24-19.03,19.11-35.79,34.24-48.9C63.7,11.26,91.71,0,122.35,0v152.22c0,16.76,13.59,30.34,30.36,30.34Z" style="fill: #7367f0;"/>
                                                    <path d="m152.71,182.56c-42.16,0-80.34-17.09-107.98-44.73-16.43-16.43-29.13-36.57-36.72-59.06,2.31-6.1,5.11-11.96,8.33-17.54,6.31,22.18,20.29,49.17,33.64,65.6,23.07,28.47,56.32,48.67,94.95,54.71h.02c2.47.66,5.09,1.01,7.77,1.01Z" style="fill: #7367f0; mix-blend-mode: overlay; opacity: .7;"/>
                                                    </g>
                                                    <g>
                                                    <path d="m201.06,304.91c42.16,0,80.34,17.09,107.98,44.73,16.43,16.43,29.13,36.57,36.72,59.06-7.24,19.03-19.11,35.79-34.24,48.9-21.46,18.61-49.47,29.87-80.11,29.87v-152.22c0-16.76-13.59-30.34-30.36-30.34Z" style="fill: #7367f0;"/>
                                                    <path d="m201.06,304.91c42.16,0,80.34,17.09,107.98,44.73,16.43,16.43,29.13,36.57,36.72,59.06-2.31,6.1-5.11,11.96-8.33,17.54-6.31-22.18-20.29-49.17-33.64-65.6-23.07-28.47-56.32-48.67-94.95-54.71h-.02c-2.47-.66-5.09-1.01-7.77-1.01Z" style="fill: #7367f0; mix-blend-mode: overlay; opacity: .7;"/>
                                                    <path d="m201.06,304.91c31.75-.59,63.56,9.39,89.32,27.96,25.8,18.45,45.67,45.27,55.29,75.53-2.75-7.41-5.88-14.69-9.7-21.6-26.45-49.51-78.84-81.12-134.91-81.9h0Z" style="fill: #f5f6f6;"/>
                                                    </g>
                                                    <path d="m152.71,182.56c-31.75.59-63.56-9.39-89.32-27.96-25.8-18.45-45.67-45.27-55.29-75.53,2.75,7.41,5.88,14.69,9.7,21.6,26.45,49.51,78.84,81.12,134.91,81.9h0Z" style="fill: #f5f6f6;"/>
                                                </g>
                                                </g>
                                            </g>
                                            </g>
                                        </svg>
                                    </div>
                                    <span class="app-brand-text fw-bold fs-4 ms-50"> Hirexcel </span>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-center">
                            <h3 class="fw-bold">Evaluation Summary Report</h3>
                        </div>
                    </div>
                    <div class="card-body px-0">
                        <h5 class="fw-bold mt-6">Candidate Information</h5>
                        <table class="table table-bordered">
                            <tbody>
                                <tr><td class="pe-4"><p class="fw-bold mb-0">First Name</p></td><td>${data.user_info?.first_name ?? 'N/A'}</td></tr>
                                <tr><td class="pe-4"><p class="fw-bold mb-0">Last Name</p></td><td>${data.user_info?.last_name ?? 'N/A'}</td></tr>
                                <tr><td class="pe-4"><p class="fw-bold mb-0">City</p></td><td>${data.user_info?.city ?? 'N/A'}</td></tr>
                                <tr><td class="pe-4"><p class="fw-bold mb-0">Country</p></td><td>${data.user_info?.country ?? 'N/A'}</td></tr>
                                <tr><td class="pe-4"><p class="fw-bold mb-0">Phone Number</p></td><td>${data.user_info?.phone_number ?? 'N/A'}</td></tr>
                            </tbody>
                        </table>
                        <h5 class="fw-bold mt-6">Job Information</h5>
                        <table class="table table-bordered">
                            <tbody>
                                <tr><td class="mx-auto"><p class="fw-bold mb-0">Job Title</p></td><td>${data.job_post?.title ?? 'N/A'}</td></tr>
                                <tr><td class="mx-auto"><p class="fw-bold mb-0">Job Type</p></td><td>${data.job_post?.job_type ?? 'N/A'}</td></tr>
                                <tr><td class="mx-auto"><p class="fw-bold mb-0">Job Position</p></td><td>${data.job_post?.job_position ?? 'N/A'}</td></tr>
                                <tr>
                                    <td class="mx-auto"><p class="fw-bold mb-0">Job Personality Traits</p></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto mb-0">
                                            ${(data.personality_traits_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr><td class="mx-auto"><p class="fw-bold mb-0">Cognitive Weightage</p></td><td>${data.job_post?.cognitive_weightage ?? 'N/A'}</td></tr>
                                <tr><td class="mx-auto"><p class="fw-bold mb-0">Technical Weightage</p></td><td>${data.job_post?.technical_weightage ?? 'N/A'}</td></tr>
                                <tr>
                                    <td class="mx-auto"><p class="fw-bold mb-0">Technical Assessment Level</p></td>
                                    <td>
                                        <div class="d-flex flex-row flex-nowrap overflow-auto mb-0">
                                            ${(data.technical_assessment_level_list ?? []).map(level => `<span class="badge bg-info-subtle text-info me-1">${level}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <h5 class="fw-bold mt-6">Assessment Insights</h5>
                        <table class="table table-bordered">
                            <tbody>
                                <tr>
                                    <td class=""><p class="fw-bold mb-0">Candidate Status</p></td>
                                    <td>
                                        ${data.evaluation_summary?.candidate_status === 'Not Recommended' ? 
                                            `<span class='badge bg-danger-subtle text-danger me-1 mt-2'>${data.evaluation_summary?.candidate_status}</span>` :
                                            `<span class='badge bg-success-subtle text-success me-1 mt-5'>${data.evaluation_summary?.candidate_status}</span>`
                                        }
                                    </td>
                                </tr>
                                <tr><td class=""><p class="fw-bold mb-0">Profile Synopsis</p></td><td>${data.evaluation_summary?.profile_synopsis ?? 'N/A'}</td></tr>
                                <tr>
                                    <td class=""><p class="fw-bold mb-0">Optimal Job Matches</p></td>
                                    <td>
                                        <ol class="mb-0">
                                            ${(data.optimal_job_matches_list ?? []).map(match => `<li>${match}</li>`).join('')}
                                        </ol>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <h5 class="fw-bold mt-6">Holistic Evaluation Summary</h5>
                        <table class="table table-bordered">
                            <tbody>
                                <tr>
                                    <td class="fw-bold">Cognitive Score Percentage</td>
                                    <td class="fw-medium">${data.cognitive_assessment?.cognitive_score_percentage ?? 'N/A'} &#37;</td>
                                    <td>
                                        ${data.cognitive_result === "Passed" ? 
                                            `<span class="badge bg-success-subtle text-success me-1">Passed</span>` : 
                                            `<span class="badge bg-danger-subtle text-danger me-1">Failed</span>`
                                        }
                                    </td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Technical Score Percentage</td>
                                    <td class="fw-medium">${data.technical_assessment?.tech_score_percentage ?? 'N/A'} &#37;</td>
                                    <td>
                                        ${data.technical_result === "Passed" ? 
                                            `<span class="badge bg-success-subtle text-success me-1">Passed</span>` : 
                                            `<span class="badge bg-danger-subtle text-danger me-1">Failed</span>`
                                        }
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <h5 class="fw-bold mt-6">Detailed Characteristics</h5>
                        <table  class="table table-bordered">
                            <tbody>
                                <tr>
                                    <td><strong>Category</strong></td>
                                    <td class="fw-bold display-6 ">${data.personality_report ?? 'N/A'}</td>
                                </tr>
                                <tr>
                                    <td><strong>Personality Traits</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_personality_trait_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                            ${(data.bigf_openness_personality_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                            ${(data.bigf_concientiousness_personality_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                            ${(data.bigf_extraversion_personality_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                            ${(data.bigf_agreeableness_personality_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                            ${(data.bigf_neuroticism_personality_list ?? []).map(trait => `<span class="badge bg-primary-subtle text-primary me-1 mb-1">${trait}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Cognitive Abilities</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_cognitive_abilities_list ?? []).map(ability => `<span class="badge bg-info-subtle text-info me-1 mb-1">${ability}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Tendencies</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_tendencies_list ?? []).map(tendency => `<span class="badge bg-info-subtle text-info me-1 mb-1">${tendency}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Weaknesses</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_weaknesses_list ?? []).map(weakness => `<span class="badge bg-danger-subtle text-danger me-1 mb-1">${weakness}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Behaviour</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_behaviour_list ?? []).map(behaviour => `<span class="badge bg-success-subtle text-success me-1 mb-1">${behaviour}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Motivated By</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_motivated_list ?? []).map(motivate => `<span class="badge bg-success-subtle text-success me-1 mb-1">${motivate}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Emotional Characteristics</strong></td>
                                    <td>
                                        <div class="d-flex flex-row flex-wrap overflow-auto py-1">
                                            ${(data.disc_emotional_list ?? []).map(emotion => `<span class="badge bg-success-subtle text-success me-1 mb-1">${emotion}</span>`).join('')}
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <hr class="mt-0 mb-6" />
                    <div class="card-body p-0">
                        <div class="row">
                            <div class="col-12">
                                <span class="fw-medium text-heading">Note:</span>
                                <span>This is a system-generated report. Thank You!</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}