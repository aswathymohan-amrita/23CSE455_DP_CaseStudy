package com.elearning.service;

import com.elearning.model.*;
import com.elearning.repository.*;
import com.elearning.service.results.QuizResultPublisher;
import com.elearning.service.scoring.ScoringStrategy;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import java.util.List;
import java.util.Map;

@Service
public class QuizService {
  private final QuizRepository quizRepository;
  private final CourseRepository courseRepository;
  private final UserRepository userRepository;
  private final QuizResultRepository resultRepository;
  private final ScoringStrategy standardScoring;
  private final ScoringStrategy negativeMarkingScoring;
  private final QuizResultPublisher resultPublisher;

  public QuizService(QuizRepository quizRepository, CourseRepository courseRepository,
      UserRepository userRepository, QuizResultRepository resultRepository,
      @Qualifier("standardScoring") ScoringStrategy standardScoring,
      @Qualifier("negativeMarkingScoring") ScoringStrategy negativeMarkingScoring,
      QuizResultPublisher resultPublisher) {
    this.quizRepository = quizRepository;
    this.courseRepository = courseRepository;
    this.userRepository = userRepository;
    this.resultRepository = resultRepository;
    this.standardScoring = standardScoring;
    this.negativeMarkingScoring = negativeMarkingScoring;
    this.resultPublisher = resultPublisher;
  }

  @Transactional
  public Quiz createQuiz(Long courseId, Long instructorId, String title, List<Question> questions) {
    if (title == null || title.isBlank() || questions == null || questions.isEmpty())
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "A title and at least one question are required");
    Course course = courseRepository.findById(courseId)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Course not found"));
    if (instructorId == null || course.getInstructor() == null
        || !instructorId.equals(course.getInstructor().getId()))
      throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Only the course instructor may create quizzes");
    Quiz quiz = new Quiz(title.trim(), course);
    for (Question question : questions) {
      if (question == null || question.getPrompt() == null || question.getPrompt().isBlank()
          || question.getCorrectAnswer() == null || question.getCorrectAnswer().isBlank()
          || !Double.isFinite(question.getPoints()) || question.getPoints() <= 0)
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Questions need a prompt, answer, and positive points");
      question.setQuiz(quiz);
    }
    quiz.setQuestions(questions);
    return quizRepository.save(quiz);
  }

  public List<Quiz> quizzesForCourse(Long courseId) {
    if (!courseRepository.existsById(courseId))
      throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Course not found");
    return quizRepository.findByCourseId(courseId);
  }

  @Transactional
  public QuizResult grade(Long quizId, Long studentId, Map<Long, String> answers, boolean negativeMarking) {
    Quiz quiz = quizRepository.findById(quizId)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Quiz not found"));
    User student = userRepository.findById(studentId)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Student not found"));
    if (!"STUDENT".equalsIgnoreCase(student.getRole()))
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Only students may submit quiz answers");
    Map<Long, String> safeAnswers = answers == null ? Map.of() : answers;
    double score = (negativeMarking ? negativeMarkingScoring : standardScoring)
        .score(quiz.getQuestions(), safeAnswers);
    QuizResult result = resultRepository.save(new QuizResult(quizId, studentId, score));
    resultPublisher.publish(result);
    return result;
  }
}
