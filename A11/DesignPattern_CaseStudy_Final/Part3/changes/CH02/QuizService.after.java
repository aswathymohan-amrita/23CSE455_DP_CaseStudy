import java.util.List;
import java.util.Map;
import java.util.Objects;

class QuizService {
  private final ScoringStrategy strategy;

  QuizService(ScoringStrategy strategy) {
    this.strategy = Objects.requireNonNull(strategy);
  }

  int calculateScore(List<Question> questions, Map<Integer, String> answers) {
    return strategy.score(questions, answers);
  }
}
