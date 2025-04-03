#pragma once
#include <SFML/Graphics/Shape.hpp>
#include <SFML/Graphics/RectangleShape.hpp>
#include <thread>
#include <iostream>
#include <chrono>
#include "../GameManager.hpp"
#include "../CustomClock.hpp"
#include "../Utils.hpp"
#include "../Player.hpp"
#include "../Ball.hpp"

#define PASS_COST player->getPosition().x - ARGplayer->getPosition().x + player->getPosition().y - ARGplayer->getPosition().y
#define PASS_VELOCITY -exp(timeSinceStart/900)+301
class Action
{
public:
    virtual void Start(Player * ARGplayer) = 0;
    virtual void Update(Player * ARGplayer) = 0;
    virtual void End(Player * ARGplayer) = 0;
};

// ======================================================================================

// Actions performed when Players are idling
class Act_PlayerIdle : Action
{
public:
    Act_PlayerIdle() { /* Does nothing */ };
    ~Act_PlayerIdle() { /* Does nothing */ };

    void Start(Player* ARGplayer) override
    {
        /* Does nothing */

        #ifdef _DEBUG
        ARGplayer->setFillColor(IDLE_COLOR);
        #endif
    };
    void Update(Player* ARGplayer) override { /* Does nothing */ };
    void End(Player* ARGplayer) override { /* Does nothing */ };
};

// Actions performed when Players are Chasing a ball
class Act_PlayerChaseBall : Action
{
public:
    Act_PlayerChaseBall() { /* Does nothing */ };
    ~Act_PlayerChaseBall() { /* Does nothing */ };

    void Start(Player* ARGplayer) override
    {
        /* Sets a speed to make sure we move */
        ARGplayer->setSpeed(NORMAL_SPEED);

        #ifdef _DEBUG
        ARGplayer->setFillColor(CHASE_BALL_COLOR);
        #endif
    };
    void Update(Player* ARGplayer) override
    {
        /* Look in the direction of the ball */
        sf::Vector2f distToBall = GameManager::Get()->getBall()->getPosition() - ARGplayer->getPosition();
        ARGplayer->setDirection(Utils::Vector2fNormalize(distToBall));
    };
    void End(Player* ARGplayer) override
    {
        // Nothing yet
    };
};

// Actions performed when Players just got the ball
class Act_PlayerGoatedRun : Action
{
public:
    Act_PlayerGoatedRun() { /* Does nothing */ };
    ~Act_PlayerGoatedRun() { /* Does nothing */ };

    void Start(Player* ARGplayer) override
    {
        /* Sets a speed to make sure we move and look a the opponent's area and reset the timer */
        ARGplayer->setSpeed(GOATED_SPEED);
        GameManager::Get()->getBall()->resetGoatedTime();

        /* Look in the direction of the opponent's goal.  ! WARNING !> Doesn't account for Context::Team::NONE */
        Context::FieldPlace targetGoal = (ARGplayer->getTeam() == Context::Team::Blue) ? Context::FieldPlace::RedGoal : Context::FieldPlace::BlueGoal;
        sf::Vector2f distToOppGoal{ GameManager::Get()->getField()->getHitbox(targetGoal)->getPosition().x - ARGplayer->getPosition().x, 0 };
        ARGplayer->setDirection(Utils::Vector2fNormalize(distToOppGoal));

        #ifdef _DEBUG
        ARGplayer->setFillColor(GOATED_RUN_COLOR);
        #endif
    };
    void Update(Player* ARGplayer) override
    {
        GameManager::Get()->getBall()->substractGoatedTime(CustomClock::Get()->getTimeElapsed_MS());
    };
    void End(Player* ARGplayer) override
    {
        // Nothing yet
    };
};

// Actions performed when Players have add the ball for some time already
class Act_PlayerRunAtGoal : Action
{
public:
    Act_PlayerRunAtGoal() { /* Does nothing*/ };
    ~Act_PlayerRunAtGoal() { /* Does nothing*/ };

    void Start(Player* ARGplayer)
    {
        /* Sets the normal speed back */
        ARGplayer->setSpeed(NORMAL_SPEED);

        #ifdef _DEBUG
        ARGplayer->setFillColor(RUN_AT_GOAL_COLOR);
        #endif
    };
    void Update(Player* ARGplayer)
    {
        // Probably nothing, unless we want this to be advanced
    }
    void End(Player* ARGplayer)
    {
        // Nothing yet
    }
};

// Actions performed when a teammate Player have the ball
class Act_PlayerSupportBud : Action
{
public:
    Act_PlayerSupportBud() { /* Does nothing */ };
    ~Act_PlayerSupportBud() { /* Does nothing */ };

    void Start(Player* ARGplayer)
    {
        /* Sets the normal speed just in case */
        ARGplayer->setSpeed(NORMAL_SPEED);

        #ifdef _DEBUG
        ARGplayer->setFillColor(SUPPORT_BUD_COLOR);
        #endif
    };
    void Update(Player* ARGplayer)
    {
        Player* buddy = GameManager::Get()->getBall()->getOwner();
        if (buddy == nullptr) return;
        sf::Vector2f buddyPos = buddy->getPosition();
        sf::Vector2f playerPos = ARGplayer->getPosition();

        if (buddy == nullptr) return;
        sf::Vector2f distToBud = buddy->getPosition() - ARGplayer->getPosition();
        sf::Vector2f dirOfBud = buddy->getDirection();

        /* Checks if it is far enough behind the leading player */
        if (abs(distToBud.x) < SUPPORT_HORIZ_DIST || (ARGplayer->getTeam() == Context::Team::Blue && playerPos.x > buddyPos.x) || (ARGplayer->getTeam() == Context::Team::Red && playerPos.x < buddyPos.x))
            dirOfBud.x *= -1.f;

        /* Check if it is vertically away enough from the leading player */
        if (abs(distToBud.y) < SUPPORT_VERTI_DIST && playerPos.y > buddyPos.y)
            dirOfBud.y = 1.f;
        else if (abs(distToBud.y) < SUPPORT_VERTI_DIST && playerPos.y < buddyPos.y)
            dirOfBud.y = -1.f;
        else
            dirOfBud.y = buddy->getDirection().y;

        ARGplayer->setDirection(dirOfBud);

    }
    void End(Player* ARGplayer)
    {
        // Nothing yet
    }
};

// Actions performed when an opponenet Player have the ball
class Act_PlayerAttackOpp : Action
{
public:
    Act_PlayerAttackOpp() { /* Does nothing */ };
    ~Act_PlayerAttackOpp() { /* Does nothing */ };

    void Start(Player* ARGplayer)
    {
        /* Sets the normal speed just in case */
        ARGplayer->setSpeed(ATTACK_SPEED);

        #ifdef _DEBUG
        ARGplayer->setFillColor(ATTACK_OPP_COLOR);
        #endif
    }
    void Update(Player* ARGplayer)
    {
        Ball* ball = GameManager::Get()->getBall();
        if (ball->getOwner() == nullptr) return;
        /* Look in the direction of the opponent that has the ball */
        sf::Vector2f distToOpp = ball->getOwner()->getPosition() - ARGplayer->getPosition();
        ARGplayer->setDirection(Utils::Vector2fNormalize(distToOpp));

        /* Steals the ball if the player touches it */
        sf::Vector2f distToBall = ball->getPosition() - ARGplayer->getPosition();
        if (Utils::Vector2fGetNorm(distToBall) <= ARGplayer->getRadius() + ball->getOwner()->getRadius() && ball->getOwner()->getState() != Context::State::GoatedRun)
        {
            ball->setOwner(ARGplayer);
        }
    };
    void End(Player* ARGplayer)
    {
        // Nothing yet
    };
};

class Act_PlayerMakePass : Action
{
public:
    Act_PlayerMakePass() { /* Does nothing */ };
    ~Act_PlayerMakePass() { /* Does nothing */ };

    void Start(Player* ARGplayer)
    {
        #ifdef _DEBUG
        ARGplayer->setFillColor(MAKE_PASS_COLOR);
        #endif

        Ball* bufferBall = GameManager::Get()->getBall();
        float cost = 0.f;
        Player* playerToPass = nullptr;
        std::vector<Player*>* bufferPlayer = GameManager::Get()->getPlayers();

        for (auto& player : *bufferPlayer)
        {
            if (!checkCanPass(ARGplayer, player)) continue;
            if (playerToPass == nullptr)
            {
                cost = abs(PASS_COST);
                playerToPass = player;
            }

            else if (cost > abs(PASS_COST))
            {
                cost = abs(PASS_COST);
                playerToPass = player;
            }
        }

        if (playerToPass != nullptr)
        {
            bufferBall->setOwner(nullptr);
            bufferBall->goToPosition(playerToPass->getPosition());
            bufferBall->setSpeed(300);
        }
    }

    void Update(Player* ARGplayer)
    {
        // Nothing yet
    };
    void End(Player* ARGplayer)
    {
        // Nothing yet
    };


    bool checkCanPass(Player* playerA, Player* playerB)
    {
        if (playerA->getTeam() != playerB->getTeam() || playerA == playerB) return false;
        if (playerA->getTeam() == Context::Team::Blue)
        {
            if (playerA->getPosition().x > playerB->getPosition().x)
                return true;
            return false;
        }
        if (playerA->getPosition().x < playerB->getPosition().x)
            return true;
        return false;
    }
};