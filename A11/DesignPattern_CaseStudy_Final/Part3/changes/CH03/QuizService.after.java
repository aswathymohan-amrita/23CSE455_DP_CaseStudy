class QuizService {
  Result submit(Quiz quiz, Student student, Answers answers) {
    int score = grader.grade(quiz.questions(), answers.asMap());
    Result result = resultRepository.save(new Result(quiz.id(), student.id(), score));
    resultPublisher.publish(result);
    return result;
  }
}
