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
        terminalGridContainer.appendChild(boxWrapper);
    });
});