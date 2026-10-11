import java.util.*;
public class TestMain {
  static void check(boolean ok) { if(!ok) throw new AssertionError(); }
  public static void main(String[] args) {
    var q=List.of(new Question(1,10,"A"),new Question(2,5,"B"),new Question(3,5,"A")); var a=Map.of(1,"A",2,"B",3,"C");
    check(new QuizGrader(new StandardScoringStrategy()).grade(q,a)==15);
    check(new QuizGrader(new NegativeMarkingStrategy()).grade(q,a)==13);
    check(new QuizGrader(new StandardScoringStrategy()).grade(q,Map.of())==0);
    check(new QuizGrader(new StandardScoringStrategy()).grade(q,Map.of(1,"A",2,"B",3,"C",999,"A"))==15);
    var p=new QuizResultPublisher(); var s=new StudentResultObserver(); var i=new InstructorResultObserver(); p.subscribe(s);p.subscribe(i);p.publish(new QuizResult(101,7,15));
    check(s.count==1&&s.last.equals("student:7 quiz:101 score:15")); check(i.count==1&&i.last.equals("quiz:101 score:15")); System.out.println("PASS 6/6");
  }
}
