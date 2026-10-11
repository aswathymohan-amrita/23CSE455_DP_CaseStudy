from dataclasses import dataclass
from abc import ABC, abstractmethod
@dataclass(frozen=True)
class Question:
    id: int
    points: int
    correct: str
@dataclass(frozen=True)
class QuizResult:
    quiz_id: int
    student_id: int
    score: int
class ScoringStrategy(ABC):
    @abstractmethod
    def score(self, questions, answers): ...
class StandardScoringStrategy(ScoringStrategy):
    def score(self, questions, answers):
        return sum(q.points for q in questions if answers.get(q.id) == q.correct)
class NegativeMarkingStrategy(ScoringStrategy):
    def score(self, questions, answers):
        total = 0
        for q in questions:
            answer = answers.get(q.id)
            if not answer: continue
            total += q.points if answer == q.correct else -max(1, q.points // 2)
        return max(0, total)
class QuizGrader:
    def __init__(self, strategy): self.strategy = strategy
    def grade(self, questions, answers): return self.strategy.score(questions, answers)
class QuizResultObserver(ABC):
    @abstractmethod
    def on_result(self, result): ...
class QuizResultPublisher:
    def __init__(self): self.observers = []
    def subscribe(self, observer): self.observers.append(observer)
    def publish(self, result):
        for observer in tuple(self.observers): observer.on_result(result)
class StudentResultObserver(QuizResultObserver):
    def __init__(self): self.count, self.last = 0, ""
    def on_result(self, r): self.count += 1; self.last = f"student:{r.student_id} quiz:{r.quiz_id} score:{r.score}"
class InstructorResultObserver(QuizResultObserver):
    def __init__(self): self.count, self.last = 0, ""
    def on_result(self, r): self.count += 1; self.last = f"quiz:{r.quiz_id} score:{r.score}"
