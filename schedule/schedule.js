document.addEventListener('DOMContentLoaded', () => {
    const scheduleContainer = document.getElementById('dynamic-schedule');
    
    // Use the Fetch API to get the agenda data
    fetch('agenda.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(agendaData => {
            // Clear the loading message
            scheduleContainer.innerHTML = ''; 
            
            // Loop through each item in the agenda and create the HTML
            agendaData.forEach(item => {
                let itemHtml = '';

                // Check if the item is a break or a regular session
                if (item.isBreak) {
                    const timeRange = item.endTime ? `<p>${item.startTime} - ${item.endTime}</p>` : '';
                    itemHtml = `
                        <div class="col-md-12 col-sm-12 schedule animate__animated ${item.animation} text-center break">
                            <p class="time"><i class="fa-solid fa-clock"></i> ${item.startTime}</p>
                            <p class="title">${item.title}</p>
                            ${timeRange}
                        </div>`;
                } else {
                    // Build presenter line
                    let presenterLine = `${item.startTime} - ${item.endTime}`;
                    if (item.presenter) {
                        presenterLine += `, Presenter: ${item.presenter}`;
                    }

                    // Build speaker images HTML
                    let speakerImagesHtml = '';
                    if (item.speakerImages && item.speakerImages.length > 0) {
                        item.speakerImages.forEach(src => {
                            speakerImagesHtml += `<img src="${src}" width="200px" alt="speaker photo" style="margin: 0 5px;" /> `;
                        });
                        speakerImagesHtml += '<br><br>';
                    }

                    // Create HTML for the session entry and its corresponding modal
                    itemHtml = `
                        <div class="col-md-12 col-sm-12 schedule animate__animated ${item.animation}" data-toggle="modal" data-target="#${item.modalId}">
                            <div class="front">
                                <p class="time"><i class="fa-solid fa-clock"></i> ${item.startTime}</p>
                                <p class="title">${item.title}</p>
                                <p class="presenter">${presenterLine}</p>
                            </div>
                        </div>

                        <div class="modal fade" id="${item.modalId}" tabindex="-1" role="dialog" aria-labelledby="${item.modalId}Label">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                        <h4 class="modal-title title" id="${item.modalId}Label">${item.title}</h4>
                                    </div>
                                    <div class="modal-body text-center">
                                        ${speakerImagesHtml}
                                        <p class="description">${item.description}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }
                // Add the newly created HTML to the container
                scheduleContainer.innerHTML += itemHtml;
            });
        })
        .catch(error => {
            console.error('Error fetching schedule:', error);
            scheduleContainer.innerHTML = '<p class="text-center text-danger">Could not load the conference schedule. Please check back later.</p>';
        });
});
