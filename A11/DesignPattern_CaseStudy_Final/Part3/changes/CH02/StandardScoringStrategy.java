import java.util.List;
import java.util.Map;

final class StandardScoringStrategy implements ScoringStrategy {
  public int score(List<Question> questions, Map<Integer, String> answers) {
    int total = 0;
    for (Question q : questions) {
      if (q.correct().equals(answers.get(q.id()))) total += q.points();
    }
    return total;
  }
}
