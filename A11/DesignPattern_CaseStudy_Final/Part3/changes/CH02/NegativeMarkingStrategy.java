import java.util.List;
import java.util.Map;

final class NegativeMarkingStrategy implements ScoringStrategy {
  public int score(List<Question> questions, Map<Integer, String> answers) {
    int total = 0;
    for (Question q : questions) {
      String answer = answers.get(q.id());
      if (answer == null || answer.isBlank()) continue;
      if (q.correct().equals(answer)) total += q.points();
      else total -= Math.max(1, q.points() / 2);
    }
    return Math.max(0, total);
  }
}
