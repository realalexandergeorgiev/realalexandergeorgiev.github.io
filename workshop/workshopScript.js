document.addEventListener('DOMContentLoaded', () => {
    const terminalGridContainer = document.querySelector('.terminal-grid-container');
    if (!terminalGridContainer) {
        console.error('Terminal grid container not found.');
        return;
    }

    terminalGridContainer.innerHTML = ''; // Clear existing content

    workshopDetails.forEach(workshop => {
        // Create box-wrapper
        const boxWrapper = document.createElement('div');
        boxWrapper.classList.add('box-wrapper');

        // Create box-title
        const boxTitle = document.createElement('h2');
        boxTitle.classList.add('box-title');
        boxTitle.textContent = workshop.title;
        boxWrapper.appendChild(boxTitle);

        // Create container-box
        const containerBox = document.createElement('div');
        containerBox.classList.add('container-box');

        // Create description-half
        const descriptionHalf = document.createElement('div');
        descriptionHalf.classList.add('description-half');
        const descriptionParagraph = document.createElement('p');
        descriptionParagraph.textContent = workshop.description;
        descriptionHalf.appendChild(descriptionParagraph);
        containerBox.appendChild(descriptionHalf);

        // Create lower-half
        const lowerHalf = document.createElement('div');
        lowerHalf.classList.add('lower-half');

        // Create lower-half-left
        const lowerHalfLeft = document.createElement('div');
        lowerHalfLeft.classList.add('lower-half-left');
        const leftList = document.createElement('ul');
        leftList.classList.add('row-list');
        workshop.leftContent.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            leftList.appendChild(li);
        });
        lowerHalfLeft.appendChild(leftList);
        lowerHalf.appendChild(lowerHalfLeft);

        // Create lower-half-right
        const lowerHalfRight = document.createElement('div');
        lowerHalfRight.classList.add('lower-half-right');
        const rightList = document.createElement('ul');
        rightList.classList.add('row-list');
        workshop.rightContent.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            rightList.appendChild(li);
        });
        lowerHalfRight.appendChild(rightList);
        lowerHalf.appendChild(lowerHalfRight);

        containerBox.appendChild(lowerHalf);
        boxWrapper.appendChild(containerBox);

        // Create "Register here" box
        const registerBox = document.createElement('div');
        registerBox.classList.add('register-box');
        const registerLink = document.createElement('a');
        registerLink.href = workshop.registrationLink || '#'; // Use registrationLink or a fallback
        registerLink.textContent = 'Register here';
        registerBox.appendChild(registerLink);
        boxWrapper.appendChild(registerBox);

        terminalGridContainer.appendChild(boxWrapper);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const terminalGridContainer = document.querySelector('.terminal-grid-container');
    if (!terminalGridContainer) {
        console.error('Terminal grid container not found.');
        return;
    }

    terminalGridContainer.innerHTML = ''; // Clear existing content

    workshopDetails.forEach(workshop => {
        // Create box-wrapper
        const boxWrapper = document.createElement('div');
        boxWrapper.classList.add('box-wrapper');

        // Create box-title
        const boxTitle = document.createElement('h2');
        boxTitle.classList.add('box-title');
        boxTitle.textContent = workshop.title;
        boxWrapper.appendChild(boxTitle);

        // Create container-box
        const containerBox = document.createElement('div');
        containerBox.classList.add('container-box');

        // Create description-half
        const descriptionHalf = document.createElement('div');
        descriptionHalf.classList.add('description-half');
        const descriptionParagraph = document.createElement('p');
        descriptionParagraph.textContent = workshop.description;
        descriptionHalf.appendChild(descriptionParagraph);
        containerBox.appendChild(descriptionHalf);

        // Create lower-half
        const lowerHalf = document.createElement('div');
        lowerHalf.classList.add('lower-half');

        // Create lower-half-left
        const lowerHalfLeft = document.createElement('div');
        lowerHalfLeft.classList.add('lower-half-left');
        const leftList = document.createElement('ul');
        leftList.classList.add('row-list');
        workshop.leftContent.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            leftList.appendChild(li);
        });
        lowerHalfLeft.appendChild(leftList);
        lowerHalf.appendChild(lowerHalfLeft);

        // Create lower-half-right
        const lowerHalfRight = document.createElement('div');
        lowerHalfRight.classList.add('lower-half-right');
        const rightList = document.createElement('ul');
        rightList.classList.add('row-list');
        workshop.rightContent.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            rightList.appendChild(li);
        });
        lowerHalfRight.appendChild(rightList);
        lowerHalf.appendChild(lowerHalfRight);

        containerBox.appendChild(lowerHalf);
        boxWrapper.appendChild(containerBox);

        // Create "Register here" box (from previous turn)
        const registerBox = document.createElement('div');
        registerBox.classList.add('register-box');
        const registerLink = document.createElement('a');
        registerLink.href = workshop.registrationLink || '#'; // Use registrationLink or a fallback
        registerLink.textContent = 'Register here';
        registerBox.appendChild(registerLink);
        boxWrapper.appendChild(registerBox);

        terminalGridContainer.appendChild(boxWrapper);
    });

    // Countdown Timer Logic
    const countdownElement = document.getElementById('countdown');
    const targetDate = new Date('2025-07-08T18:00:00+02:00').getTime(); // Target: July 8, 2025, 18:00 CET (UTC+2)

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = targetDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        if (distance < 0) {
            clearInterval(countdownInterval);
            countdownElement.innerHTML = "WORKSHOPS ARE LIVE!";
            countdownElement.style.color = "#FF0000"; // Red text for "Live"
            countdownElement.style.textShadow = "0 0 10px #FF0000"; // Red glow
        } else {
            countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }
    }

    // Update the countdown every 1 second
    const countdownInterval = setInterval(updateCountdown, 1000);

    // Initial call to display the countdown immediately
    updateCountdown();
});