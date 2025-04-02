#pragma once

#include <SFML/Graphics/Color.hpp>
#include "Entity.hpp"
#include "Context.hpp"

#define NORMAL_SPEED 60.f
#define ATTACK_SPEED 65.f
#define GOATED_SPEED 110.f
#define SUPPORT_HORIZ_DIST 170.f
#define SUPPORT_VERTI_DIST 50.f
#define DISTANCE_TO_PASS 30.f
#define ATTACK_RADIUS 300.f

#ifdef _DEBUG
#define IDLE_COLOR sf::Color(140, 255, 251)
#define CHASE_BALL_COLOR sf::Color(255, 202, 24)
#define RUN_AT_GOAL_COLOR sf::Color(14, 209, 69)
#define TOUCHDOWN_ATT_COLOR sf::Color(196, 255, 14)
#define SUPPORT_BUD_COLOR sf::Color(184, 61, 186)
#define ATTACK_OPP_COLOR sf::Color(236, 28, 36)
#define MAKE_PASS_COLOR sf::Color(185, 122, 86)
#endif

class Behaviour;

class Player : public Entity
{
private:
    Context::Team mTeam;
    Context::State mState;
    Behaviour* mBehaviour;

public:
    Player(Context::Team team, const sf::Vector2f& position, Behaviour* behaviour, Context::FieldPlace field);
    ~Player();

    void Update() override;

    /* Getters & Setters *//**/
    Context::State getState() const;
    void setState(Context::State);
    Context::Team getTeam();
    float getSpeed();
    sf::Vector2f getDirection();
    float getRadius();
    Behaviour* getBehaviour();
    void setSpeed(float new_speed);
    void setFillColor(sf::Color ARGcolor);
    Context::FieldPlace getField();
};
