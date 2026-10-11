package com.elearning.service.results;

import com.elearning.model.QuizResult;
import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;

class QuizResultPublisherTest {
  @Test void publishesTheSameResultOnceToEveryObserver() {
    List<QuizResult> studentEvents = new ArrayList<>();
    List<QuizResult> instructorEvents = new ArrayList<>();
    QuizResultObserver student = studentEvents::add;
    QuizResultObserver instructor = instructorEvents::add;
    QuizResult result = new QuizResult(101L, 7L, 15);

    new QuizResultPublisher(List.of(student, instructor)).publish(result);

    assertEquals(List.of(result), studentEvents);
    assertEquals(List.of(result), instructorEvents);
  }

  @Test void anEmptyObserverListIsAllowed() {
    new QuizResultPublisher(List.of()).publish(new QuizResult(101L, 7L, 15));
  }
}
