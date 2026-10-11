package com.elearning.service.scoring;

import com.elearning.model.Question;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.assertEquals;

class ScoringStrategyTest {
  private Question question(long id, String answer, double points) {
    Question question = new Question("Question " + id, answer, points);
    ReflectionTestUtils.setField(question, "id", id);
    return question;
  }

  @Test void standardScoringAwardsOnlyCorrectAnswersAndIgnoresMissingOrUnknownAnswers() {
    var questions = List.of(question(1, "A", 10), question(2, "B", 5), question(3, "C", 5));
    assertEquals(15, new StandardScoringStrategy().score(questions, Map.of(1L, "A", 2L, "B", 99L, "A")));
    assertEquals(0, new StandardScoringStrategy().score(questions, Map.of()));
  }

  @Test void negativeScoringPenalizesAnsweredWrongAnswersButNeverGoesBelowZero() {
    var questions = List.of(question(1, "A", 10), question(2, "B", 5), question(3, "C", 5));
    var strategy = new NegativeMarkingScoringStrategy();
    assertEquals(12.5, strategy.score(questions, Map.of(1L, "A", 2L, "X", 3L, "C")));
    assertEquals(0, strategy.score(questions, Map.of(1L, "X", 2L, "X", 3L, "X")));
    assertEquals(0, strategy.score(questions, Map.of()));
  }
}
