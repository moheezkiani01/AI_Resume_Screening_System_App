// Form validation and UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resumeForm');
    const fileInput = document.getElementById('resume');
    const textarea = document.getElementById('job_description');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Validate file
            if (fileInput && fileInput.files.length === 0) {
                e.preventDefault();
                showAlert('Please select a PDF file', 'error');
                return false;
            }
            
            // Validate job description
            if (textarea && !textarea.value.trim()) {
                e.preventDefault();
                showAlert('Please enter a job description', 'error');
                return false;
            }
            
            // Show loading indicator
            const submitBtn = form.querySelector('.btn-submit');
            submitBtn.textContent = 'Analyzing...';
            submitBtn.disabled = true;
        });
    }
    
    // File validation
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file && !file.name.toLowerCase().endsWith('.pdf')) {
                showAlert('Only PDF files are allowed', 'error');
                this.value = '';
            }
        });
    }
    
    // Animate score circles
    const scoreCircle = document.querySelector('.score-circle');
    if (scoreCircle) {
        const score = parseFloat(scoreCircle.getAttribute('data-score'));
        const valueSpan = scoreCircle.querySelector('.score-value');
        let currentScore = 0;
        const interval = setInterval(() => {
            if (currentScore >= score) {
                clearInterval(interval);
            } else {
                currentScore++;
                valueSpan.textContent = currentScore + '%';
            }
        }, 20);
    }
});

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    const formCard = document.querySelector('.form-card');
    
    if (container && formCard) {
        container.insertBefore(alertDiv, formCard);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}