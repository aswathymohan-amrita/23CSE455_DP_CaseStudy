from patterns import *
def check(value):
    if not value: raise AssertionError("test failed")
q=[Question(1,10,"A"),Question(2,5,"B"),Question(3,5,"A")]; a={1:"A",2:"B",3:"C"}
check(QuizGrader(StandardScoringStrategy()).grade(q,a)==15)
check(QuizGrader(NegativeMarkingStrategy()).grade(q,a)==13)
check(QuizGrader(StandardScoringStrategy()).grade(q,{})==0)
check(QuizGrader(StandardScoringStrategy()).grade(q,{1:"A",2:"B",3:"C",999:"A"})==15)
p=QuizResultPublisher(); s=StudentResultObserver(); i=InstructorResultObserver(); p.subscribe(s); p.subscribe(i); p.publish(QuizResult(101,7,15))
check(s.count==1 and s.last=="student:7 quiz:101 score:15")
check(i.count==1 and i.last=="quiz:101 score:15")
print("PASS 6/6")
