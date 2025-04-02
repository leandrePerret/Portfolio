#include "Transition.hpp"
#include "../Player.hpp"

#include <iostream>

/*
   Constu & Destru
*/
Transition::Transition() { mTargetState = Context::State::UNKNOWN; }
Transition::~Transition() { /* Does nothing */ }


void Transition::setTargetState(Context::State target_state)
{
    mTargetState = target_state;
}

void Transition::addCondition(Condition* condition)
{
    mConditions.push_back(condition);
}

void Transition::Try(Player * Player)
{
    if (Player->getState() == Context::State::RunAtGoal)
        int i = 0;

    int true_tests = 0;
    for (const auto &c : mConditions)
    {
        true_tests += c->Test(Player);
    }
    if (true_tests != 0 && true_tests == mConditions.size())
    {
        std::cout << "Changed State !\n";
        Player->setState(mTargetState);
    }
}
