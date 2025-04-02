#pragma once

#include "../GameManager.hpp"
#include "../Player.hpp"
#include "../Ball.hpp"
#include "../Utils.hpp"

#define CONDITION_TO_MAKE_PASS Utils::Vector2fGetNorm(centerDist) <= ARGplayer->getRadius() + player->getRadius() + DISTANCE_TO_PASS
class Condition 
{
public:
    virtual bool Test(Player* Player) = 0;
};

// ======================================================================================

// Condition to get into Idle state
class Cond_PlayerIdle : Condition
{
public:
    Cond_PlayerIdle() { /* Does nothing */ };
    ~Cond_PlayerIdle() { /* Does nothing */ };

    bool Test(Player* ARGplayer) override { return true; }
};

// Condition to get into ChaseBall state
class Cond_PlayerChaseBall : Condition
{
public:
    Cond_PlayerChaseBall() { /* Does nothing */ };
    ~Cond_PlayerChaseBall() { /* Does nothing */ };

    bool Test(Player* ARGplayer) override { return GameManager::Get()->isBallFree(); }
};

// Condition to get into GoatedRun state
class Cond_PlayerGoatedRun : Condition
{
public:
    Cond_PlayerGoatedRun() { /* Does nothing */ };
    ~Cond_PlayerGoatedRun() { /* Does nothing */ };

    bool Test(Player* ARGplayer) override
    {
        Ball* ball = GameManager::Get()->getBall();
        return ball->getOwner() == ARGplayer && ball->getLastOwner() != ARGplayer;
    };
};

// Condition to get into TouchdownAtt state
class Cond_PlayerRunAtGoal : Condition
{
public:
    Cond_PlayerRunAtGoal() { /* Does nothing */ };
    ~Cond_PlayerRunAtGoal() { /* Does nothing */ };

    //bool Test(Player* ARGplayer) override { return GameManager::Get()->getBall()->getGoatedTime_MS() <= 0; };
    bool Test(Player* ARGplayer) override
    {
        if (ARGplayer->getState() == Context::State::AttackOpp)
        {
            Player* ballOwner = GameManager::Get()->getBall()->getOwner();
            if (ballOwner == nullptr) return false;
            else if (Utils::Vector2fGetNorm(GameManager::Get()->getBall()->getOwner()->getPosition() - ARGplayer->getPosition()) > ATTACK_RADIUS) return true;
        }
        else return GameManager::Get()->getBall()->getGoatedTime_MS() <= 0;
    };
};

// Condition to get into SupportBud state
class Cond_PlayerSupportBud : Condition
{
public:
    Cond_PlayerSupportBud() { /* Does nothing */ };
    ~Cond_PlayerSupportBud() { /* Does nothing */ };

    bool Test(Player* ARGplayer) override
    {
        Player* ballOwner = GameManager::Get()->getBall()->getOwner();
        if (ballOwner == nullptr) return false;
        else return ballOwner->getTeam() == ARGplayer->getTeam();
    };
};

// Condition to get into AttackOpp state
class Cond_PlayerAttackOpp : Condition
{
public:
    Cond_PlayerAttackOpp() { /* Does nothing */ };
    ~Cond_PlayerAttackOpp() { /* Does nothing */ };

    bool Test(Player* ARGplayer) override
    {
        Player* ballOwner = GameManager::Get()->getBall()->getOwner();
        if (ballOwner == nullptr) return false;
        else return ballOwner->getTeam() != ARGplayer->getTeam();
    };
};


// Condition to get into MakePass state
class Cond_PlayerMakePass : Condition
{
public:
    Cond_PlayerMakePass() { /* Does nothing */ };
    ~Cond_PlayerMakePass() { /* Does nothing */ };

    bool Test(Player* ARGplayer) override 
    { 
        /* Doesn't get into that state if the player does not have the ball in the first place */
        Player* ballOwner = GameManager::Get()->getBall()->getOwner();
        if (ballOwner != ARGplayer) return false;

        std::vector<Player*>* bufferPlayer = GameManager::Get()->getPlayers();

        sf::FloatRect checkedPLayerLocalBounds = ARGplayer->getShape().getLocalBounds();
        sf::Vector2f ARGplayerCenter = ARGplayer->getPosition() + sf::Vector2f{ checkedPLayerLocalBounds.width / 2, checkedPLayerLocalBounds.height / 2 };

        for (auto& player : *bufferPlayer)
        {
            if (player->getTeam() == ARGplayer->getTeam()) continue;
            if (ARGplayer->getTeam() == Context::Team::Blue && ARGplayer->getPosition().x > player->getPosition().x) continue;
            if (ARGplayer->getTeam() == Context::Team::Red && ARGplayer->getPosition().x < player->getPosition().x) continue;
            sf::FloatRect playerLocalBounds = player->getShape().getLocalBounds();
            sf::Vector2f playerCenter = player->getPosition() + sf::Vector2f{ playerLocalBounds.width / 2, playerLocalBounds.height / 2 };
            sf::Vector2f centerDist{ abs(ARGplayerCenter.x - playerCenter.x), abs(ARGplayerCenter.y - playerCenter.y) };

            // If the distance is smaller than both radius, detect collision and gives the Ball its new owner's pointer
            if (CONDITION_TO_MAKE_PASS) 
                return true;
        }
        return false;
    };
};