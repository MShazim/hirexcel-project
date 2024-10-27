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
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 182.16 251">
                                            <g style="isolation: isolate;">
                                            <g id="Layer_2" data-name="Layer 2">
                                                <g id="OBJECTS">
                                                <g>
                                                    <g>
                                                    <path d="m182.16,67.55v91.83c-11.56-23.06-63-38.57-63-38.57v-60.53c0-36.53,52.52-43.24,61.2-7.75,1.18,4.81,1.8,9.84,1.8,15.02Z" style="fill: #7367f0;"/>
                                                    <path d="m0,188.71v-91.83c11.56,23.06,63,38.57,63,38.57v54.92c0,40.24-60.14,42.8-62.85,2.65-.1-1.43-.15-2.86-.15-4.31Z" style="fill: #7367f0;"/>
                                                    </g>
                                                    <path d="m182.16,127.58v24.5c-11.56-23.06-63-38.57-63-38.57v-27.26h.42c27.89,0,52.17,16.82,62.58,41.33Z" style="fill: #1f1e21; mix-blend-mode: overlay; opacity: .2;"/>
                                                    <path d="m0,123.42v-24.5c11.56,23.06,63,38.57,63,38.57v27.26h-.42c-27.89,0-52.17-16.82-62.58-41.33Z" style="fill: #1f1e21; mix-blend-mode: overlay; opacity: .2;"/>
                                                    <g>
                                                    <path d="m182.16,149.77v38.23c0,7.91-1.46,15.49-4.13,22.46-10.37-30.66-39.13-52.84-73.16-53.4-.44-.04-.88-.06-1.33-.06h-40.62c-33.71,0-61.23-26.47-62.92-59.76v-34.24c0-7.91,1.46-15.47,4.12-22.44,3.91,11.58,10.45,21.95,18.91,30.41,14.23,14.23,33.89,23.03,55.6,23.03h40.95c32.34,0,59,24.38,62.58,55.77Z" style="fill: #00b5e8;"/>
                                                    <path d="m182.16,149.77v38.23c0,7.91-1.46,15.49-4.13,22.46-10.37-30.66-39.13-52.84-73.16-53.4-.44-.04-.88-.06-1.33-.06h-40.62c-33.71,0-61.23-26.47-62.92-59.76v-34.24c0-7.91,1.46-15.47,4.12-22.44,3.91,11.58,10.45,21.95,18.91,30.41,14.23,14.23,33.89,23.03,55.6,23.03h40.95c32.34,0,59,24.38,62.58,55.77Z" style="fill: #7367f0;"/>
                                                    <path d="m182.16,149.77v7.29c-3.63-31.85-30.68-56.59-63.5-56.59h-41.55c-22.03,0-41.81-9.1-56.42-23.37C4.08,60.88,3.39,42.47,4.12,40.56c3.91,11.58,10.45,21.95,18.91,30.41,14.23,14.23,33.89,23.03,55.6,23.03h40.95c32.34,0,59,24.38,62.58,55.77Z" style="fill: #fff; mix-blend-mode: overlay; opacity: .5;"/>
                                                    <path d="m178.03,210.46c-3.74,9.82-9.87,18.46-17.68,25.21-11.04,9.55-25.44,15.33-41.19,15.33v-78.38c0-8.18-6.28-14.89-14.29-15.56,34.03.56,62.79,22.74,73.16,53.4Z" style="fill: #017dc0;"/>
                                                    </g>
                                                    <g>
                                                    <path d="m78.63,94c-21.71,0-41.37-8.8-55.6-23.03-8.46-8.46-15-18.83-18.91-30.41,3.73-9.8,9.84-18.43,17.63-25.18C32.8,5.8,47.22,0,63,0v78.38c0,8.63,7,15.62,15.63,15.62Z" style="fill: #7367f0;"/>
                                                    <path d="m78.63,94c-21.71,0-41.37-8.8-55.6-23.03-8.46-8.46-15-18.83-18.91-30.41,1.19-3.14,2.63-6.16,4.29-9.03,3.25,11.42,10.45,25.32,17.32,33.78,11.88,14.66,29,25.06,48.89,28.17h.01c1.27.34,2.62.52,4,.52Z" style="fill: #7367f0; mix-blend-mode: overlay; opacity: .7;"/>
                                                    </g>
                                                    <g>
                                                    <path d="m103.53,157c21.71,0,41.37,8.8,55.6,23.03,8.46,8.46,15,18.83,18.91,30.41-3.73,9.8-9.84,18.43-17.63,25.18-11.05,9.58-25.47,15.38-41.25,15.38v-78.38c0-8.63-7-15.62-15.63-15.62Z" style="fill: #7367f0;"/>
                                                    <path d="m103.53,157c21.71,0,41.37,8.8,55.6,23.03,8.46,8.46,15,18.83,18.91,30.41-1.19,3.14-2.63,6.16-4.29,9.03-3.25-11.42-10.45-25.32-17.32-33.78-11.88-14.66-29-25.06-48.89-28.17h0c-1.27-.34-2.62-.52-4-.52Z" style="fill: #7367f0; mix-blend-mode: overlay; opacity: .7;"/>
                                                    <path d="m103.53,157c24.71-.99,49.23,11.36,63.6,31.41,4.78,6.64,8.52,14.05,10.86,21.88-1.49-3.79-3.14-7.51-5.15-11.04-13.57-25.1-40.84-41.52-69.31-42.25h0Z" style="fill: #f5f6f6;"/>
                                                    </g>
                                                    <path d="m78.63,94c-24.71.99-49.23-11.36-63.6-31.41-4.78-6.64-8.52-14.05-10.86-21.88,1.49,3.79,3.14,7.51,5.15,11.04,13.57,25.1,40.84,41.52,69.31,42.25h0Z" style="fill: #f5f6f6;"/>
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