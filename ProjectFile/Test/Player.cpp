#include "Player.hpp"
#include "StateMachine/Behaviour.hpp"
#include <SFML/Graphics/CircleShape.hpp>
#include <iostream>

namespace
{
	std::map<Player*, Context::FieldPlace> playerFieldMap;
}

Player::Player(Context::Team team, const sf::Vector2f& position, Behaviour* behaviour, Context::FieldPlace field) :
	mState(Context::State::Idle)
{
	mTeam = team;
    mBehaviour = behaviour;
	mSize = 50.f;
	mSpeed = NORMAL_SPEED;

    sf::CircleShape* shape = new sf::CircleShape(10);
	shape->setRadius(mSize / 2.f);
	shape->setFillColor(team == Context::Team::Blue ? sf::Color::Blue : sf::Color::Red);
	shape->setOrigin(mSize / 2.f, mSize / 2.f);
	shape->setPosition(position);
    mShape = shape;
	playerFieldMap[this] = field;
}

Player::~Player()
{
}

void Player::Update()
{
	mBehaviour->Update(this);
	Entity::Update();
}

Context::State Player::getState() const
{
    return mState;
}

void Player::setState(Context::State new_state) 
{
	mBehaviour->End(this);
    mState = new_state;
	mBehaviour->Start(this);
}


/*
   Getters & Setters
*//**/
float Player::getSpeed() { return mSpeed; }
sf::Vector2f Player::getDirection() { return mDirection; }
Context::Team Player::getTeam() { return mTeam; }
float Player::getRadius() { return ((sf::CircleShape*)mShape)->getRadius(); }
Behaviour* Player::getBehaviour() { return mBehaviour; }
void Player::setSpeed(float new_speed) { mSpeed = new_speed; }
void Player::setFillColor(sf::Color ARGcolor) { mShape->setFillColor(ARGcolor); }
Context::FieldPlace Player::getField(){	return playerFieldMap[this]; }