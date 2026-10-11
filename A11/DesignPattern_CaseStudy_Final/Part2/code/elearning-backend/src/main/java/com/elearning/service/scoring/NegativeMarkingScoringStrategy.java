package com.elearning.service.scoring;

import com.elearning.model.Question;
import org.springframework.stereotype.Component;
import java.util.List;
import java.util.Map;
import java.util.Objects;

@Component("negativeMarkingScoring")
public class NegativeMarkingScoringStrategy implements ScoringStrategy {
  @Override
  public double score(List<Question> questions, Map<Long, String> answers) {
    double score = 0;
    for (Question question : questions) {
      String answer = answers.get(question.getId());
      if (answer == null || answer.isBlank()) continue;
      score += Objects.equals(question.getCorrectAnswer(), answer)
          ? question.getPoints() : -question.getPoints() * 0.5;
    }
    return Math.max(0, score);
  }
}
