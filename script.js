$(document).ready(function () {
    // Logic for initial choice submission
    $('#initial-choice-form').submit(function (event) {
        event.preventDefault();
        const choice = $('input[name="choice"]:checked').val();
        localStorage.setItem('userChoice', choice);
        window.location.href = 'quiz.html'; // Redirect to the quiz page
    });

    // Check if on the quiz page
    if (window.location.pathname.endsWith('quiz.html')) {
        // Quiz questions and options
        const questions = [
            { question: "Question 1", options: ["Option A", "Option B", "Option C", "Option D"], answer: "Option A" },
            { question: "Question 2", options: ["Option A", "Option B", "Option C", "Option D"], answer: "Option A" },
            { question: "Question 3", options: ["Option A", "Option B", "Option C", "Option D"], answer: "Option A" },
            { question: "Question 4", options: ["Option A", "Option B", "Option C", "Option D"], answer: "Option A" },
            // ... Add more questions in similar format
            // { question: "Question N", options: ["Option A", "Option B", "Option C", "Option D"], answer: "Option A" }
        ];

        // Dynamically generate quiz questions
        questions.forEach((q, index) => {
            let optionsHtml = q.options.map((option, i) => {
                return `<div class="form-check">
                            <input class="form-check-input" type="radio" name="question${index}" id="question${index}option${i}" value="${option}">
                            <label class="form-check-label" for="question${index}option${i}">${option}</label>
                        </div>`;
            }).join('');

            $('#questions-container').append(
                `<div class="mb-4">
                    <p>${q.question}</p>
                    ${optionsHtml}
                </div>`
            );
        });

        // Handle quiz form submission
        $('#quiz-form').submit(function (event) {
            event.preventDefault();
            let correctAnswers = 0;
            questions.forEach((q, index) => {
                let selectedOption = $(`input[name="question${index}"]:checked`).val();
                if (selectedOption === q.answer) {
                    correctAnswers++;
                }
            });

            const userChoice = parseInt(localStorage.getItem('userChoice'));
            const score = calculateScore(userChoice, correctAnswers);
            localStorage.setItem('quizScore', score);
            window.location.href = 'results.html'; // Redirect to results page
        });

        // Display the score on results.html
        if (window.location.pathname.includes('results.html')) {
            const score = localStorage.getItem('quizScore');
            $('#score-display').text('Your Score: ' + score);
        }
    }
});

// Function to calculate score based on choice and correct answers
function calculateScore(choice, correctAnswers) {
    if (choice === 1 || choice === 2) {
        if (correctAnswers > 3) {
            return 40 + (correctAnswers - 4) * 4; // Ensures score is within 40-60
        } else {
            return correctAnswers; // Ensures score is within 1-10
        }
    } else if (choice === 3) {
        if (correctAnswers < 2) {
            return correctAnswers;
        } else if (correctAnswers < 8) {
            return 41 + (correctAnswers - 2) * 6; // Avoids 20-40 range
        } else {
            return 89 + correctAnswers; // Ensures high scores for good performance
        }
    } else if (choice === 4 || choice === 5) {
        if (correctAnswers < 5) {
            return 20 + correctAnswers * 4; // Ensures score is within 20-40
        } else {
            return 60 + (correctAnswers - 5) * 8; // Ensures score is within 60-100
        }
    }
}

// Function to display result dot
function displayResultDot(score) {
    const lineLength = $('#result-line').width();
    const position = (lineLength * score) / 100 - 5; // Adjust for dot size
    $('#result-dot').css('left', position + 'px').show(); // Show the dot
}