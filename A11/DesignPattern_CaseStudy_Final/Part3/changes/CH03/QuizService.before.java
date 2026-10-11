class QuizService {
  Result submit(Quiz quiz, Student student, Answers answers) {
    int score = grader.grade(quiz.questions(), answers.asMap());
    Result result = resultRepository.save(new Result(quiz.id(), student.id(), score));
    notificationService.notifyStudent(student, result);
    notificationService.notifyInstructor(quiz.instructor(), result);
    return result;
  }
}
