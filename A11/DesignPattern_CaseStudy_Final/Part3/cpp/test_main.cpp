#include "patterns.hpp"
#include <cassert>
#include <iostream>
int main(){std::vector<Question>q{{1,10,"A"},{2,5,"B"},{3,5,"A"}};std::unordered_map<int,std::string>a{{1,"A"},{2,"B"},{3,"C"}};StandardScoringStrategy s;NegativeMarkingStrategy n;assert(QuizGrader(s).grade(q,a)==15);assert(QuizGrader(n).grade(q,a)==13);assert(QuizGrader(s).grade(q,{})==0);assert(QuizGrader(s).grade(q,{{1,"A"},{2,"B"},{3,"C"},{999,"A"}})==15);QuizResultPublisher p;StudentResultObserver so;InstructorResultObserver io;p.subscribe(so);p.subscribe(io);p.publish({101,7,15});assert(so.count==1&&so.last=="student:7 quiz:101 score:15");assert(io.count==1&&io.last=="quiz:101 score:15");std::cout<<"PASS 6/6\n";}
