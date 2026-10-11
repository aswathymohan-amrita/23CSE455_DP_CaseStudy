package com.elearning.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;

@Entity
public class Question {
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  @Column(nullable = false, length = 2000)
  private String prompt;
  @Column(nullable = false)
  private String correctAnswer;
  @Column(nullable = false)
  private double points;
  @ManyToOne(optional = false)
  @JoinColumn(name = "quiz_id", nullable = false)
  @JsonIgnore
  private Quiz quiz;

  public Question() {}
  public Question(String prompt, String correctAnswer, double points) {
    this.prompt = prompt; this.correctAnswer = correctAnswer; this.points = points;
  }
  public Long getId() { return id; }
  public String getPrompt() { return prompt; }
  public void setPrompt(String prompt) { this.prompt = prompt; }
  public String getCorrectAnswer() { return correctAnswer; }
  public void setCorrectAnswer(String correctAnswer) { this.correctAnswer = correctAnswer; }
  public double getPoints() { return points; }
  public void setPoints(double points) { this.points = points; }
  public Quiz getQuiz() { return quiz; }
  public void setQuiz(Quiz quiz) { this.quiz = quiz; }
}
