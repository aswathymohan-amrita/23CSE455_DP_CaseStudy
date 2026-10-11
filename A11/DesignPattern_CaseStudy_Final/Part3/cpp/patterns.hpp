#pragma once
#include <algorithm>
#include <string>
#include <unordered_map>
#include <vector>
struct Question { int id; int points; std::string correct; };
struct QuizResult { int quizId; int studentId; int score; };
class ScoringStrategy { public: virtual ~ScoringStrategy()=default; virtual int score(const std::vector<Question>&,const std::unordered_map<int,std::string>&)const=0; };
class StandardScoringStrategy final:public ScoringStrategy { public: int score(const std::vector<Question>& qs,const std::unordered_map<int,std::string>& as)const override { int n=0;for(const auto&q:qs){auto it=as.find(q.id);if(it!=as.end()&&it->second==q.correct)n+=q.points;}return n;} };
class NegativeMarkingStrategy final:public ScoringStrategy { public: int score(const std::vector<Question>& qs,const std::unordered_map<int,std::string>& as)const override { int n=0;for(const auto&q:qs){auto it=as.find(q.id);if(it==as.end()||it->second.empty())continue;n+=it->second==q.correct?q.points:-std::max(1,q.points/2);}return std::max(0,n);} };
class QuizGrader { const ScoringStrategy& strategy; public: explicit QuizGrader(const ScoringStrategy&s):strategy(s){} int grade(const std::vector<Question>&q,const std::unordered_map<int,std::string>&a)const{return strategy.score(q,a);} };
class QuizResultObserver { public: virtual ~QuizResultObserver()=default; virtual void onResult(const QuizResult&)=0; };
class QuizResultPublisher { std::vector<QuizResultObserver*> observers; public: void subscribe(QuizResultObserver&o){observers.push_back(&o);} void publish(const QuizResult&r)const{for(auto*o:observers)o->onResult(r);} };
class StudentResultObserver final:public QuizResultObserver { public: int count=0;std::string last;void onResult(const QuizResult&r)override{++count;last="student:"+std::to_string(r.studentId)+" quiz:"+std::to_string(r.quizId)+" score:"+std::to_string(r.score);} };
class InstructorResultObserver final:public QuizResultObserver { public: int count=0;std::string last;void onResult(const QuizResult&r)override{++count;last="quiz:"+std::to_string(r.quizId)+" score:"+std::to_string(r.score);} };
