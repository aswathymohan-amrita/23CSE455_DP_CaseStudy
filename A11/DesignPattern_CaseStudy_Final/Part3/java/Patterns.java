import java.util.*;

record Question(int id, int points, String correct) {}
record QuizResult(int quizId, int studentId, int score) {}
interface ScoringStrategy { int score(List<Question> questions, Map<Integer,String> answers); }
final class StandardScoringStrategy implements ScoringStrategy {
  public int score(List<Question> questions, Map<Integer,String> answers) {
    int total=0; for (Question q: questions) if (q.correct().equals(answers.get(q.id()))) total+=q.points(); return total;
  }
}
final class NegativeMarkingStrategy implements ScoringStrategy {
  public int score(List<Question> questions, Map<Integer,String> answers) {
    int total=0; for (Question q: questions) { String a=answers.get(q.id()); if (a==null||a.isBlank()) continue; if(q.correct().equals(a)) total+=q.points(); else total-=Math.max(1,q.points()/2); } return Math.max(0,total);
  }
}
final class QuizGrader {
  private final ScoringStrategy strategy;
  QuizGrader(ScoringStrategy strategy) { this.strategy=Objects.requireNonNull(strategy); }
  int grade(List<Question> questions, Map<Integer,String> answers) { return strategy.score(questions,answers); }
}
interface QuizResultObserver { void onResult(QuizResult result); }
final class QuizResultPublisher {
  private final List<QuizResultObserver> observers=new ArrayList<>();
  void subscribe(QuizResultObserver observer) { observers.add(Objects.requireNonNull(observer)); }
  void publish(QuizResult result) { for (QuizResultObserver observer: List.copyOf(observers)) observer.onResult(result); }
}
final class StudentResultObserver implements QuizResultObserver {
  int count; String last="";
  public void onResult(QuizResult r) { count++; last="student:"+r.studentId()+" quiz:"+r.quizId()+" score:"+r.score(); }
}
final class InstructorResultObserver implements QuizResultObserver {
  int count; String last="";
  public void onResult(QuizResult r) { count++; last="quiz:"+r.quizId()+" score:"+r.score(); }
}
