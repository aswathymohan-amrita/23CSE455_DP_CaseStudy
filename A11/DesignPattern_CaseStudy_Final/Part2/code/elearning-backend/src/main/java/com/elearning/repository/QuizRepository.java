package com.elearning.repository;

import com.elearning.model.Quiz;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.EntityGraph;
import java.util.Optional;
import java.util.List;

public interface QuizRepository extends JpaRepository<Quiz, Long> {
  @EntityGraph(attributePaths = "questions")
  List<Quiz> findByCourseId(Long courseId);

  @Override
  @EntityGraph(attributePaths = "questions")
  Optional<Quiz> findById(Long id);
}
