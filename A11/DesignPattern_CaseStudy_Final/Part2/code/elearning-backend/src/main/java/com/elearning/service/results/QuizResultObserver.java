package com.elearning.service.results;

import com.elearning.model.QuizResult;

public interface QuizResultObserver {
  void onResult(QuizResult result);
}
