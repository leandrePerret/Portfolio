#pragma once

#include <utility>
#include <vector>
#include <SFML/System/Vector2.hpp>
#include "Context.hpp"
#include "Field.hpp"

class Entity;
class Player;
class Ball;
class Score;

namespace sf 
{
	class RenderWindow;
}

class GameManager
{
private:
	/* Fields *//**/
	std::vector<Player*> mPlayerList;
	Ball* mBall;
	sf::RenderWindow* mWindow;
	float mDeltaTime;
	Field* mField;
	Score* mScore;

	GameManager();
	void CreateField();
	void setWindow(sf::RenderWindow* window);

	/* Collision checkers *//**/
	void checkCollisions();
	void checkBallCollision();
	void checkPlayersCollisions();
	//void addEntity(Entity* entity);

public:
	/* Constru & Destru & Init*//**/
	~GameManager();
	static GameManager* Instantiate();
	static GameManager* Get();
	void Init(sf::RenderWindow* window);

	/* GameManager shenaningans *//**/
	void Update();
	void Draw();

	/* Getters & Setters *//**/
	float getDeltaTime() const;
	void setDeltaTime(float deltaTime);
	Ball* getBall();
	Context::Team getBallTeamOwner();
	std::vector<Player*>* getPlayers();
	Field* getField();

	/* Ball tools *//**/
	bool isBallFree();
	void forcePass();

	#ifdef _DEBUG
	Player* getPlayerFromMousePos(sf::Vector2f ARGmousePos);
	#endif

	void reset(Context::Team);

	friend Entity;
};

