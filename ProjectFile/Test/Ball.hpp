#pragma once

#include "Entity.hpp"
#include <SFML/Graphics/CircleShape.hpp>

#define GOATED_TIME 1500

class Player;

class Ball : public Entity
{
private:
    Player* mOwner;
    Player* mLastOwner;
    int mGoatedTime_MS;

public:
    Ball(const sf::Vector2f& position);
    ~Ball();

    void Update() override;

    /* Getters & Setters *//**/
    Player* getOwner();
    Player* getLastOwner();
    float getRadius();
    int getGoatedTime_MS();
    void setOwner(Player* ARGplayer);

    /* Timer related *//**/
    void resetGoatedTime();
    void substractGoatedTime(int time_MS);

    void reset();
};
