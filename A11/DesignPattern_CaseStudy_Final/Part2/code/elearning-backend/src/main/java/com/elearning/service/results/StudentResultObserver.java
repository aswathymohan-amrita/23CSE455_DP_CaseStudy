package com.elearning.service.results;

import com.elearning.model.QuizResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class StudentResultObserver implements QuizResultObserver {
  private static final Logger log = LoggerFactory.getLogger(StudentResultObserver.class);
  @Override public void onResult(QuizResult result) {
    log.info("Quiz {} result {} is available to student {}", result.getQuizId(), result.getScore(), result.getStudentId());
  }
}
