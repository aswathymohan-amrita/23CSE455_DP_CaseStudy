import java.util.List;
import java.util.Map;

class QuizService {
  int calculateScore(List<Question> questions, Map<Integer, String> answers) {
    int score = 0;
    for (Question q : questions) {
      String answer = answers.get(q.id());
      if (answer == null || answer.isBlank()) continue;
      if (q.correct().equals(answer)) score += q.points();
      else score -= Math.max(1, q.points() / 2);
    }
    return Math.max(0, score);
  }
}
