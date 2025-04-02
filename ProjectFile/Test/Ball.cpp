#include "Ball.hpp"
#include "Player.hpp"
#include <iostream>


/*
   Constru & Destru
*//**/
Ball::Ball(const sf::Vector2f& position)
{
    sf::CircleShape* shape = new sf::CircleShape();

    mSize = 30.f;
    shape->setRadius(mSize / 2.f);
    shape->setFillColor(sf::Color::Yellow);
    shape->setOrigin(mSize / 2.f, mSize / 2.f);
    shape->setPosition(position);
    mShape = shape;
    mOwner = nullptr;
    mLastOwner = nullptr;
}
Ball::~Ball()
{
}


void Ball::Update()
{
    Entity::Update();

    // Teleport onto the carrying player (if any)
    if (mOwner != nullptr)
        mShape->setPosition(mOwner->getPosition());
}


/*
   Getters & Setters
*//**/
Player* Ball::getOwner() { return mOwner; }
Player* Ball::getLastOwner() { return mLastOwner; }
float Ball::getRadius() { return ((sf::CircleShape*)mShape)->getRadius(); }
int Ball::getGoatedTime_MS() { return mGoatedTime_MS; }
void Ball::setOwner(Player* ARGplayer) {
    mLastOwner = mOwner;
    mOwner = ARGplayer;
    #ifdef _DEBUG
    std::cout << "Ball Owner set!\n";
    #endif
}


/*
   Timer related
*//**/
void Ball::resetGoatedTime() { mGoatedTime_MS = GOATED_TIME; std::cout << "Goated time at : " << mGoatedTime_MS << std::endl; }
void Ball::substractGoatedTime(int time_MS) { mGoatedTime_MS -= time_MS; std::cout << "Goated time at : " << mGoatedTime_MS << std::endl; }

void Ball::reset()
{
    mLastOwner = nullptr;
    mOwner = nullptr;
    mShape->setPosition(sf::Vector2f(640.f, 360.f));
    mSpeed = 0.f;
    resetGoatedTime();
}
