package com.elearning.service.scoring;

import com.elearning.model.Question;
import java.util.List;
import java.util.Map;

public interface ScoringStrategy {
  double score(List<Question> questions, Map<Long, String> answers);
}
