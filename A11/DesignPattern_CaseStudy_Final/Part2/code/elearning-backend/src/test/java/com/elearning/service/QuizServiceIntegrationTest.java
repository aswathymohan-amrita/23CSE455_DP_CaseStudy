package com.elearning.service;

import com.elearning.controller.QuizController;
import com.elearning.model.Course;
import com.elearning.model.Question;
import com.elearning.model.QuizResult;
import com.elearning.model.User;
import com.elearning.repository.CourseRepository;
import com.elearning.repository.QuizRepository;
import com.elearning.repository.QuizResultRepository;
import com.elearning.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assertions.assertThrows;

@SpringBootTest
class QuizServiceIntegrationTest {
  @Autowired QuizService quizService;
  @Autowired CourseRepository courseRepository;
  @Autowired QuizRepository quizRepository;
  @Autowired QuizResultRepository resultRepository;
  @Autowired UserRepository userRepository;

  @Test void createsCourseQuizGradesPersistsAndPublishesResult() throws Exception {
    Course course = courseRepository.findAll().get(0);
    User student = userRepository.save(new User("Quiz Student", "quiz-student@example.com", "test", "STUDENT"));
    assertThrows(org.springframework.web.server.ResponseStatusException.class,
        () -> quizService.createQuiz(course.getId(), -1L, "Unauthorized", List.of(new Question("Q", "A", 1))));
    assertThrows(org.springframework.web.server.ResponseStatusException.class,
        () -> quizService.createQuiz(course.getId(), course.getInstructor().getId(), "Invalid", List.of(new Question(" ", "A", 1))));
    var quiz = quizService.createQuiz(course.getId(), course.getInstructor().getId(), "Basics", List.of(
        new Question("Two plus two?", "4", 10), new Question("Capital of France?", "Paris", 5)));

    String publicQuizJson = new com.fasterxml.jackson.databind.ObjectMapper()
        .writeValueAsString(QuizController.QuizView.from(quiz));
    assertFalse(publicQuizJson.contains("correctAnswer"));

    assertEquals(1, quizService.quizzesForCourse(course.getId()).stream()
        .filter(item -> "Basics".equals(item.getTitle())).count());
    var saved = quizRepository.findById(quiz.getId()).orElseThrow();
    Map<Long, String> answers = Map.of(saved.getQuestions().get(0).getId(), "4",
        saved.getQuestions().get(1).getId(), "London");
    QuizResult result = quizService.grade(quiz.getId(), student.getId(), answers, true);

    assertEquals(7.5, result.getScore());
    assertTrue(resultRepository.findById(result.getId()).isPresent());
    assertEquals(quiz.getId(), result.getQuizId());
    assertEquals(student.getId(), result.getStudentId());
  }
}
