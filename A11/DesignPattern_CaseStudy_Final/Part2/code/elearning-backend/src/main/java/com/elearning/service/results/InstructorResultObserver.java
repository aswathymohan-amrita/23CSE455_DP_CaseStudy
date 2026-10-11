package com.elearning.service.results;

import com.elearning.model.QuizResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class InstructorResultObserver implements QuizResultObserver {
  private static final Logger log = LoggerFactory.getLogger(InstructorResultObserver.class);
  @Override public void onResult(QuizResult result) {
    log.info("Quiz {} result {} for student {} is available to the instructor", result.getQuizId(), result.getScore(), result.getStudentId());
  }
}
