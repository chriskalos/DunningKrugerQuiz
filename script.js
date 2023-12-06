$(document).ready(function() {
    const questions = [
        "Question 1", "Question 2", "Question 3", "Question 4", "Question 5", 
        "Question 6", "Question 7", "Question 8", "Question 9", "Question 10"
    ];
    const answers = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"];

    // Dynamically generate the question fields
    for (let i = 0; i < questions.length; i++) {
        $('#questions-container').append(
            '<div class="form-group question">' +
            '<label for="question' + i + '">' + questions[i] + ':</label>' +
            '<input type="text" id="question' + i + '" class="form-control">' +
            '</div>'
        );
    }

    // Handle the submit button click event
    $('#submit-btn').click(function() {
        let correctAnswers = 0;
        for (let i = 0; i < answers.length; i++) {
            if ($('#question' + i).val().trim() === answers[i]) {
                correctAnswers++;
            }
        }

        const userChoice = parseInt($('#userChoice').val());
        const score = calculateScore(userChoice, correctAnswers);
        $('#result').text('Your score is: ' + score);
    });

    // Scoring logic
    function calculateScore(choice, correctAnswers) {
        if (choice === 1 || choice === 2) {
            if (correctAnswers > 3) {
                return 40 + (correctAnswers - 4) * 4;  // Score within 40-60
            } else {
                return correctAnswers;  // Score within 1-10
            }
        } else if (choice === 3) {
            if (correctAnswers < 2) {
                return correctAnswers;
            } else if (correctAnswers < 8) {
                return 41 + (correctAnswers - 2) * 6;  // Avoids 20-40 range
            } else {
                return 89 + correctAnswers;  // High scores for good performance
            }
        } else if (choice === 4 || choice === 5) {
            if (correctAnswers < 5) {
                return 20 + correctAnswers * 4;  // Score within 20-40
            } else {
                return 60 + (correctAnswers - 5) * 8;  // Score within 60-100
            }
        }
    }
});
