package com.elearning.controller;

import com.elearning.model.Question;
import com.elearning.model.Quiz;
import com.elearning.model.QuizResult;
import com.elearning.service.QuizService;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class QuizController {
  private final QuizService quizService;
  public QuizController(QuizService quizService) { this.quizService = quizService; }

  @PostMapping("/courses/{courseId}/quizzes")
  public QuizView createQuiz(@PathVariable Long courseId, @RequestBody CreateQuizRequest request) {
    List<Question> questions = request.questions() == null ? null : request.questions().stream()
        .map(q -> q == null ? null : new Question(q.prompt(), q.correctAnswer(), q.points())).toList();
    return QuizView.from(quizService.createQuiz(courseId, request.instructorId(), request.title(), questions));
  }

  @GetMapping("/courses/{courseId}/quizzes")
  public List<QuizView> quizzesForCourse(@PathVariable Long courseId) {
    return quizService.quizzesForCourse(courseId).stream().map(QuizView::from).toList();
  }

  @PostMapping("/quizzes/{quizId}/grade")
  public QuizResult grade(@PathVariable Long quizId, @RequestBody GradeQuizRequest request) {
    return quizService.grade(quizId, request.studentId(), request.answers(), request.negativeMarking());
  }

  public record CreateQuizRequest(Long instructorId, String title, List<QuestionRequest> questions) {}
  public record QuestionRequest(String prompt, String correctAnswer, double points) {}
  public record GradeQuizRequest(Long studentId, Map<Long, String> answers, boolean negativeMarking) {}
  public record QuizView(Long id, String title, List<QuestionView> questions) {
    public static QuizView from(Quiz quiz) {
      return new QuizView(quiz.getId(), quiz.getTitle(), quiz.getQuestions().stream()
          .map(question -> new QuestionView(question.getId(), question.getPrompt(), question.getPoints())).toList());
    }
  }
  public record QuestionView(Long id, String prompt, double points) {}
}
