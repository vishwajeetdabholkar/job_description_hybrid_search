$(document).ready(function() {
    $("#keyword, #location").autocomplete({
        source: function(request, response) {
            $.getJSON("/autocomplete", {
                query: request.term,
                field: this.element.attr('id')
            }, response);
        },
        minLength: 2
    });
});

function searchJobs() {
    const keyword = document.getElementById('keyword').value;
    const location = document.getElementById('location').value;
    const locationType = document.getElementById('location-type').value;
    const seniority = document.getElementById('seniority').value;
    const employmentType = document.getElementById('employment-type').value;
    const company = document.getElementById('company').value;

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `keyword=${encodeURIComponent(keyword)}&location=${encodeURIComponent(location)}&locationType=${encodeURIComponent(locationType)}&seniority=${encodeURIComponent(seniority)}&employmentType=${encodeURIComponent(employmentType)}&company=${encodeURIComponent(company)}`
    })
    .then(response => response.json())
    .then(data => {
        const resultsContainer = document.getElementById('results-container');
        resultsContainer.innerHTML = '';

        const executionTimeElement = document.createElement('p');
        executionTimeElement.textContent = `Results found in ${data.execution_time.toFixed(3)} seconds`;
        executionTimeElement.className = 'execution-time';
        resultsContainer.appendChild(executionTimeElement);

        const jobListings = document.createElement('div');
        jobListings.className = 'job-listings';

        const jobDetails = document.createElement('div');
        jobDetails.className = 'job-details';

        data.results.forEach((job, index) => {
            const jobListing = document.createElement('div');
            jobListing.className = 'job-listing';
            jobListing.innerHTML = `
                <h3>${job.title}</h3>
                <p>${job.company_name}</p>
                <p>${job.location}</p>
            `;
            jobListing.addEventListener('click', () => displayJobDetails(job, jobDetails));
            jobListings.appendChild(jobListing);

            if (index === 0) {
                displayJobDetails(job, jobDetails);
            }
        });

        resultsContainer.appendChild(jobListings);
        resultsContainer.appendChild(jobDetails);
    })
    .catch(error => console.error('Error:', error));
}

function displayJobDetails(job, container) {
    container.innerHTML = `
        <h2>${job.title}</h2>
        <h3>${job.company_name}</h3>
        <p>${job.location}</p>
        <p>Work Type: ${job.formatted_work_type}</p>
        <p>Experience Level: ${job.formatted_experience_level}</p>
        <h4>Job Description</h4>
        <div class="job-description">${formatJobDescription(job.description)}</div>
        <a href="${job.apply_url}" target="_blank" class="apply-btn">Apply Now</a>
    `;
}

function formatJobDescription(description) {
    return description.split('\n').map(line => `<p>${line}</p>`).join('');
}

function resetFilters() {
    document.getElementById('keyword').value = '';
    document.getElementById('location').value = '';
    document.getElementById('location-type').value = '';
    document.getElementById('seniority').value = '';
    document.getElementById('employment-type').value = '';
    document.getElementById('company').value = '';
    document.getElementById('results-container').innerHTML = '';
}

// Make sure the search button is properly linked to the searchJobs function
document.addEventListener('DOMContentLoaded', (event) => {
    const searchButton = document.getElementById('search-button');
    if (searchButton) {
        searchButton.addEventListener('click', searchJobs);
    }
});
