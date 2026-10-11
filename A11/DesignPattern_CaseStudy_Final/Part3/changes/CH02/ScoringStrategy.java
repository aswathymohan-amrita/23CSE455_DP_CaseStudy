import java.util.List;
import java.util.Map;

interface ScoringStrategy {
  int score(List<Question> questions, Map<Integer, String> answers);
}
