#include "Score.hpp"
#include <SFML/Graphics.hpp>
#include <iostream>
#define FONT_SIZE 48

Score::Score()
{
	mBlueScore = 0;
	mRedScore = 0;
	mFont = new sf::Font();
	mFont->loadFromFile("./Hack-Regular.ttf"); // TROUVER LE CHEMIN ALED
	mText = new sf::Text();
	mText->setFont(*mFont);
	mText->setCharacterSize(FONT_SIZE);
}

void Score::printScore(sf::RenderWindow* window)
{
	sf::FloatRect textRect = mText->getLocalBounds();
	mText->setOrigin(textRect.left + textRect.width / 2.0f,
		textRect.top + textRect.height / 2.0f);
	mText->setPosition(sf::Vector2f(window->getSize().x / 2.0f, 30));
	mText->setString(std::to_string(mBlueScore) + " / " + std::to_string(mRedScore));
	window->draw(*mText);
}

void Score::blueScore()
{
	++mBlueScore;
}

void Score::redScore()
{
	++mRedScore;
}