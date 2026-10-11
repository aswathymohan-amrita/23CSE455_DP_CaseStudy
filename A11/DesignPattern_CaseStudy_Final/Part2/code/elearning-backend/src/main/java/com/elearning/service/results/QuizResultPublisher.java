package com.elearning.service.results;

import com.elearning.model.QuizResult;
import org.springframework.stereotype.Component;
import java.util.List;

@Component
public class QuizResultPublisher {
  private final List<QuizResultObserver> observers;
  public QuizResultPublisher(List<QuizResultObserver> observers) { this.observers = List.copyOf(observers); }
  public void publish(QuizResult result) { observers.forEach(observer -> observer.onResult(result)); }
}
