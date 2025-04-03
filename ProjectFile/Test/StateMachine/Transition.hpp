#pragma once

#include <vector>
#include "../Context.hpp"
#include "Condition.hpp"


class Player;

class Transition
{
protected:
    Context::State mTargetState;
    std::vector<Condition*> mConditions;

public:
    Transition();
    ~Transition();

    void Try(Player * Player);
    void setTargetState(Context::State target_state);
    void addCondition(Condition* condition);
};

