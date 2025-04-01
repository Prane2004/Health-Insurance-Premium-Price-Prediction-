document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const predictionResult = document.getElementById('prediction-result');
    const interpretationElement = document.getElementById('interpretation');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission behavior
        resultContainer.classList.add('hidden'); // Hide the result container initially

        // Show a loading indicator
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading-indicator';
        loadingIndicator.textContent = 'Calculating...';
        form.appendChild(loadingIndicator);

        try {
            // Collect the form data
            const formData = new FormData(form);

            // Send the form data as a POST request to the Flask server
            const response = await fetch('/', {
                method: 'POST',
                body: formData,
            });

            // Handle response from server
            if (!response.ok) {
                throw new Error('Failed to fetch the prediction from server');
            }

            // Parse the JSON result from the server
            const data = await response.json();

            // Remove loading indicator
            loadingIndicator.remove();

            // Display the results
            resultContainer.classList.remove('hidden');
            predictionResult.textContent = `$${data.price}`;
            interpretationElement.textContent = data.interpretation;

            // Fade in the result container for a smooth effect
            resultContainer.style.opacity = '0';
            setTimeout(() => {
                resultContainer.style.transition = 'opacity 0.5s ease-in-out';
                resultContainer.style.opacity = '1';
            }, 50);

        } catch (error) {
            // Handle any errors
            console.error('Error fetching prediction:', error);
            loadingIndicator.remove();
            resultContainer.classList.remove('hidden');
            predictionResult.textContent = 'An error occurred. Please try again.';
            interpretationElement.textContent = '';
        }
    });
});
