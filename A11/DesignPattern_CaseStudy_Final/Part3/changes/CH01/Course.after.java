import java.util.ArrayList;
import java.util.List;

class Course {
  private Long id;
  private String title;
  private List<Quiz> quizzes = new ArrayList<>();

  public Long getId() { return id; }
  public String getTitle() { return title; }
  public List<Quiz> getQuizzes() { return quizzes; }
}
