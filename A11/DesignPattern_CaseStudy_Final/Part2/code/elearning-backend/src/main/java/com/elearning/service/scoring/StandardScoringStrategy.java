package com.elearning.service.scoring;

import com.elearning.model.Question;
import org.springframework.stereotype.Component;
import java.util.List;
import java.util.Map;
import java.util.Objects;

@Component("standardScoring")
public class StandardScoringStrategy implements ScoringStrategy {
  @Override
  public double score(List<Question> questions, Map<Long, String> answers) {
    return questions.stream()
        .filter(question -> Objects.equals(question.getCorrectAnswer(), answers.get(question.getId())))
        .mapToDouble(Question::getPoints).sum();
  }
}
