class Question { constructor(id, points, correct) { Object.assign(this,{id,points,correct}); } }
class QuizResult { constructor(quizId, studentId, score) { Object.assign(this,{quizId,studentId,score}); } }
class ScoringStrategy { score() { throw new Error('abstract strategy'); } }
class StandardScoringStrategy extends ScoringStrategy { score(qs, as) { let n=0; for(const q of qs) if(as[q.id]===q.correct)n+=q.points; return n; } }
class NegativeMarkingStrategy extends ScoringStrategy { score(qs,as) { let n=0; for(const q of qs){const a=as[q.id];if(!a)continue;n+=a===q.correct?q.points:-Math.max(1,Math.floor(q.points/2));}return Math.max(0,n); } }
class QuizGrader { constructor(strategy){this.strategy=strategy;} grade(q,a){return this.strategy.score(q,a);} }
class QuizResultObserver { onResult(){throw new Error('abstract observer');} }
class QuizResultPublisher { constructor(){this.observers=[];} subscribe(o){this.observers.push(o);} publish(r){for(const o of [...this.observers])o.onResult(r);} }
class StudentResultObserver extends QuizResultObserver { constructor(){super();this.count=0;this.last='';} onResult(r){this.count++;this.last=`student:${r.studentId} quiz:${r.quizId} score:${r.score}`;} }
class InstructorResultObserver extends QuizResultObserver { constructor(){super();this.count=0;this.last='';} onResult(r){this.count++;this.last=`quiz:${r.quizId} score:${r.score}`;} }
module.exports={Question,QuizResult,StandardScoringStrategy,NegativeMarkingStrategy,QuizGrader,QuizResultPublisher,StudentResultObserver,InstructorResultObserver};
