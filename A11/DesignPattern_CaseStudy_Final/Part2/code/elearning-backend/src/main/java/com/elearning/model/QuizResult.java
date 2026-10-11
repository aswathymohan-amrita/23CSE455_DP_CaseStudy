package com.elearning.model;

import jakarta.persistence.*;

@Entity
public class QuizResult {
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  @Column(nullable = false) private Long quizId;
  @Column(nullable = false) private Long studentId;
  @Column(nullable = false) private double score;

  protected QuizResult() {}
  public QuizResult(Long quizId, Long studentId, double score) {
    this.quizId = quizId; this.studentId = studentId; this.score = score;
  }
  public Long getId() { return id; }
  public Long getQuizId() { return quizId; }
  public Long getStudentId() { return studentId; }
  public double getScore() { return score; }
}
