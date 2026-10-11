import java.util.ArrayList;
import java.util.List;

final class QuizResultPublisher {
  private final List<QuizResultObserver> observers = new ArrayList<>();
  void subscribe(QuizResultObserver observer) { observers.add(observer); }
  void publish(Result result) {
    for (QuizResultObserver observer : List.copyOf(observers)) {
      observer.onResult(result);
    }
  }
}
