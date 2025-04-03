#pragma once
#include <map>

namespace sf
{
	class RenderWindow;
	class RectangleShape;
};

namespace Context
{
	enum class FieldPlace;
}

class Player;

class Field
{
	sf::RenderWindow* mWindow;
	std::map<Context::FieldPlace, sf::RectangleShape*> mHitboxes;
	float mBlueGoal;
	float mRedGoal;
	void defineHitboxes();

public:
	Field(sf::RenderWindow* window);
	~Field();
	void Draw();
	sf::RectangleShape* getHitbox(Context::FieldPlace place);
	bool isInGoal();
	void CheckIfInZone(Player* player);
};

