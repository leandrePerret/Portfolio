#include "Field.hpp"
#include <SFML/Graphics.hpp>
#include <string>
#include <iostream>
#include "Context.hpp"
#include "Player.hpp"
#include "Ball.hpp"
#include "GameManager.hpp"

Field::Field(sf::RenderWindow* window)
{
	mWindow = window;
	defineHitboxes();
}

Field::~Field()
{
	mHitboxes.erase(mHitboxes.begin(), mHitboxes.end());
}

//Créer les Hitboxes du terrains
void Field::defineHitboxes()
{
	/*
	Taille des buts : Largeur = Largeur de fenêtre / 10 Hauteur = hauteur de fenêtre
	Taille des voies : Largeur = Largeur de fenêtre - largeur des buts Hauteur = moitié de la hauteur de la fenêtre
	*/
	unsigned int lenght = mWindow->getSize().x;
	unsigned int height = mWindow->getSize().y;

	sf::RectangleShape* BackField = new sf::RectangleShape(sf::Vector2f(lenght, height));
	BackField->setFillColor(sf::Color(205,97,85));
	mHitboxes[Context::FieldPlace::BackField] = BackField;	
	
	sf::RectangleShape* BlueGoal = new sf::RectangleShape(sf::Vector2f(lenght / 10.f, height));
	BlueGoal->setFillColor(sf::Color(0,0,255,200));
	mHitboxes[Context::FieldPlace::BlueGoal] = BlueGoal;
	mBlueGoal = BlueGoal->getLocalBounds().width;

	sf::RectangleShape* RedGoal = new sf::RectangleShape(sf::Vector2f(lenght / 10.f, height));
	RedGoal->setPosition(sf::Vector2f(9 * lenght / 10, 0));
	RedGoal->setFillColor(sf::Color(255,0,0,200));
	mHitboxes[Context::FieldPlace::RedGoal] = RedGoal;
	mRedGoal = RedGoal->getPosition().x;

	sf::RectangleShape* TopLane = new sf::RectangleShape(sf::Vector2f(4 * lenght / 5, height / 2.f));
	TopLane->setPosition(sf::Vector2f(lenght / 10, 0));
	TopLane->setFillColor(sf::Color::Transparent);
	TopLane->setOutlineColor(sf::Color::Yellow);
	TopLane->setOutlineThickness(1.f);
	mHitboxes[Context::FieldPlace::TopLane] = TopLane;

	sf::RectangleShape* BotLane = new sf::RectangleShape(sf::Vector2f(4 * lenght / 5, height / 2));
	BotLane->setPosition(sf::Vector2f(lenght / 10, height / 2));
	BotLane->setFillColor(sf::Color::Transparent);
	BotLane->setOutlineColor(sf::Color::Green);
	BotLane->setOutlineThickness(1.f);
	mHitboxes[Context::FieldPlace::BotLane] = BotLane;

	sf::RectangleShape* MidLane = new sf::RectangleShape(sf::Vector2f(4 * lenght / 5, height / 2.f));
	MidLane->setPosition(sf::Vector2f(lenght / 10, height / 4));
	MidLane->setFillColor(sf::Color::Transparent);
	MidLane->setOutlineColor(sf::Color::Magenta);
	MidLane->setOutlineThickness(1.f);
	mHitboxes[Context::FieldPlace::MidLane] = MidLane;
}

//Dessine les hitboxes
void Field::Draw()
{
	for (auto& it : mHitboxes)
	{
		mWindow->draw(*it.second);
	}
}

//Permet de récupérer une hitbox
sf::RectangleShape* Field::getHitbox(Context::FieldPlace place)
{
	return mHitboxes[place];
}

//Permet de savoir si un essai et marquer.
bool Field::isInGoal()
{
	float ballPos = GameManager::Get()->getBall()->getPosition().x + GameManager::Get()->getBall()->getRadius();
	if (ballPos <= mBlueGoal && GameManager::Get()->getBall()->getOwner()->getTeam() == Context::Team::Red || 
		ballPos >= mRedGoal && GameManager::Get()->getBall()->getOwner()->getTeam() == Context::Team::Blue)
		return true;
	return false;
}

void Field::CheckIfInZone(Player* player)
{
	const sf::Vector2f* bufferPos = &player->getPosition();
	float bufferRadius = player->getRadius();

	if (player == GameManager::Get()->getBall()->getOwner())
	{


		float bufferHitPosX = mHitboxes[Context::FieldPlace::BackField]->getPosition().x;
		float bufferWidth = mHitboxes[Context::FieldPlace::BackField]->getLocalBounds().width;
		float bufferHitPosY = mHitboxes[player->getField()]->getPosition().y;
		float bufferHeight = mHitboxes[player->getField()]->getLocalBounds().height;

		if (bufferPos->x - bufferRadius < bufferHitPosX)
			player->setPosition(sf::Vector2f(bufferHitPosX + bufferRadius, bufferPos->y));

		else if (bufferPos->x + bufferRadius > bufferHitPosX + bufferWidth)
			player->setPosition(sf::Vector2f(bufferHitPosX + bufferWidth - bufferRadius, bufferPos->y));

		if (bufferPos->y - bufferRadius < bufferHitPosY)
			player->setPosition(sf::Vector2f(bufferPos->x, bufferHitPosY + bufferRadius));

		else if (bufferPos->y + bufferRadius > bufferHitPosY + bufferHeight)
			player->setPosition(sf::Vector2f(bufferPos->x, bufferHitPosY + bufferHeight - bufferRadius));
	}

	else
	{
		float bufferHitPosX = mHitboxes[player->getField()]->getPosition().x;
		float bufferWidth = mHitboxes[player->getField()]->getLocalBounds().width;
		float bufferHitPosY = mHitboxes[player->getField()]->getPosition().y;
		float bufferHeight = mHitboxes[player->getField()]->getLocalBounds().height;

		if (bufferPos->x - bufferRadius < bufferHitPosX)
			player->setPosition(sf::Vector2f(bufferHitPosX + bufferRadius, bufferPos->y));

		else if (bufferPos->x + bufferRadius > bufferHitPosX + bufferWidth)
			player->setPosition(sf::Vector2f(bufferHitPosX + bufferWidth - bufferRadius, bufferPos->y));
	
		if (bufferPos->y - bufferRadius < bufferHitPosY)
			player->setPosition(sf::Vector2f(bufferPos->x, bufferHitPosY + bufferRadius));

		else if (bufferPos->y + bufferRadius > bufferHitPosY + bufferHeight)
			player->setPosition(sf::Vector2f(bufferPos->x, bufferHitPosY + bufferHeight - bufferRadius));
	}
}
