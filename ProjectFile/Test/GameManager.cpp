#include "GameManager.hpp"
#include "StateMachine/Behaviour.hpp"
#include "StateMachine/Action.hpp"
#include "StateMachine/Transition.hpp"
#include "StateMachine/Condition.hpp"
#include "Player.hpp"
#include "Ball.hpp"
#include "Score.hpp"
#include <SFML/Graphics/RenderWindow.hpp>
#include <SFML/Graphics/Shape.hpp>
#include <iostream>
#include <stack>

#define ATTACK_MIDDLE_BLUE sf::Vector2f(500.f, 360.f)
#define ATTACK_TOP_FRONT_BLUE sf::Vector2f(400.f, 180.f)
#define ATTACK_BOTTOM_FRONT_BLUE sf::Vector2f(400.f, 540.f)
#define ATTACK_TOP_BACK_BLUE sf::Vector2f(300.f, 100.f)
#define ATTACK_BOTTOM_BACK_BLUE sf::Vector2f(300.f, 620.f)

#define ATTACK_MIDDLE_RED sf::Vector2f(780.f, 360.f)
#define ATTACK_TOP_FRONT_RED sf::Vector2f(880.f, 180.f)
#define ATTACK_BOTTOM_FRONT_RED sf::Vector2f(880, 540.f)
#define ATTACK_TOP_BACK_RED sf::Vector2f(980.f, 100.f)
#define ATTACK_BOTTOM_BACK_RED sf::Vector2f(980.f, 620.f)

/* Define all players positions *//**/
#define DEFENSE_MIDDLE_BLUE sf::Vector2f(400.f, 360.f)
#define DEFENSE_TOP_FRONT_BLUE sf::Vector2f(300.f, 180.f)
#define DEFENSE_BOTTOM_FRONT_BLUE sf::Vector2f(300.f, 540.f)
#define DEFENSE_TOP_BACK_BLUE sf::Vector2f(200.f, 100.f)
#define DEFENSE_BOTTOM_BACK_BLUE sf::Vector2f(200.f, 620.f)

#define DEFENSE_MIDDLE_RED sf::Vector2f(880.f, 360.f)
#define DEFENSE_TOP_FRONT_RED sf::Vector2f(980.f, 180.f)
#define DEFENSE_BOTTOM_FRONT_RED sf::Vector2f(980.f, 540.f)
#define DEFENSE_TOP_BACK_RED sf::Vector2f(1080.f, 100.f)
#define DEFENSE_BOTTOM_BACK_RED sf::Vector2f(1080.f, 620.f)

namespace 
{
static GameManager* mInstance = nullptr;
}

/*
   Constru & Destru
*/
GameManager::GameManager() {}

GameManager::~GameManager()
{
	for (int i = 0; i < mPlayerList.size(); i++) delete mPlayerList[i];
	delete mBall;
	delete mField;
}

void GameManager::Init(sf::RenderWindow* window)
{
	mScore = new Score();
	mWindow = window;
	Behaviour* playerBehaviour = new Behaviour();
	mField = new Field(window);


	/*
	   Action & Condition creation
	*//**/
	Action* playerActIdle = (Action*) new Act_PlayerIdle();
	Action* playerActChaseBall = (Action*) new Act_PlayerChaseBall();
	Action* playerActGoatedRun = (Action*) new Act_PlayerGoatedRun();
	Action* playerActRunAtGoal = (Action*) new Act_PlayerRunAtGoal();
	Action* playerActSupportBud = (Action*) new Act_PlayerSupportBud();
	Action* playerActAttackOpp = (Action*) new Act_PlayerAttackOpp();
	Action* playerActMakePass = (Action*) new Act_PlayerMakePass();
	Condition* playerCondIdle = (Condition*) new Cond_PlayerIdle();
	Condition* playerCondChaseBall = (Condition*) new Cond_PlayerChaseBall();
	Condition* playerCondGoatedRun = (Condition*) new Cond_PlayerGoatedRun();
	Condition* playerCondRunAtGoal = (Condition*) new Cond_PlayerRunAtGoal();
	Condition* playerCondSupportBud = (Condition*) new Cond_PlayerSupportBud();
	Condition* playerCondAttackOpp = (Condition*) new Cond_PlayerAttackOpp();
	Condition* playerCondMakePass = (Condition*) new Cond_PlayerMakePass();


	/*
	   Transition creation
	*//**/
	Transition* playerTransIdleToChaseBall = new Transition();
	Transition* playerTransIdleToSupportBud = new Transition();
	Transition* playerTransIdleToAttackOpp = new Transition();

	Transition* playerTransChaseBallToGoatedRun = new Transition();
	Transition* playerTransChaseBallToSupportBud = new Transition();
	Transition* playerTransChaseBallToAttackOpp = new Transition();

	Transition* playerTransSupportBudToGoatedRun = new Transition();
	Transition* playerTransSupportBudToChaseBall = new Transition();
	Transition* playerTransSupportBudToAttackOpp = new Transition();

	Transition* playerTransAttackOppToGoatedRun = new Transition();
	Transition* playerTransAttackOppToChaseBall = new Transition();
	Transition* playerTransAttackOppToSupportBud = new Transition();

	Transition* playerTransGoatedRunToRunAtGoal = new Transition();

	Transition* playerTransRunAtGoalToAttackOpp = new Transition();
	Transition* playerTransRunAtGoalToMakePass = new Transition();

	Transition* playerTransMakePassToChaseBall = new Transition();
	Transition* playerTransMakePassToSupportBud = new Transition();
	Transition* playerTransMakePassToAttackOpp = new Transition();

	/*
	  Transition filling
	*//**/
	playerTransIdleToChaseBall->setTargetState(Context::State::ChaseBall);
	playerTransIdleToChaseBall->addCondition(playerCondChaseBall);
	playerTransIdleToSupportBud->setTargetState(Context::State::SupportBud);
	playerTransIdleToSupportBud->addCondition(playerCondSupportBud);
	playerTransIdleToAttackOpp->setTargetState(Context::State::AttackOpp);
	playerTransIdleToAttackOpp->addCondition(playerCondAttackOpp);

	playerTransChaseBallToGoatedRun->setTargetState(Context::State::GoatedRun);
	playerTransChaseBallToGoatedRun->addCondition(playerCondAttackOpp);
	playerTransChaseBallToSupportBud->setTargetState(Context::State::SupportBud);
	playerTransChaseBallToSupportBud->addCondition(playerCondSupportBud);
	playerTransChaseBallToAttackOpp->setTargetState(Context::State::AttackOpp);
	playerTransChaseBallToAttackOpp->addCondition(playerCondAttackOpp);

	playerTransSupportBudToGoatedRun->setTargetState(Context::State::GoatedRun);
	playerTransSupportBudToGoatedRun->addCondition(playerCondGoatedRun);
	playerTransSupportBudToChaseBall->setTargetState(Context::State::ChaseBall);
	playerTransSupportBudToChaseBall->addCondition(playerCondChaseBall);
	playerTransSupportBudToAttackOpp->setTargetState(Context::State::AttackOpp);
	playerTransSupportBudToAttackOpp->addCondition(playerCondAttackOpp);

	playerTransAttackOppToGoatedRun->setTargetState(Context::State::GoatedRun);
	playerTransAttackOppToGoatedRun->addCondition(playerCondGoatedRun);
	playerTransAttackOppToChaseBall->setTargetState(Context::State::ChaseBall);
	playerTransAttackOppToChaseBall->addCondition(playerCondChaseBall);
	playerTransAttackOppToSupportBud->setTargetState(Context::State::SupportBud);
	playerTransAttackOppToSupportBud->addCondition(playerCondSupportBud);

	playerTransGoatedRunToRunAtGoal->setTargetState(Context::State::RunAtGoal);
	playerTransGoatedRunToRunAtGoal->addCondition(playerCondRunAtGoal);

	playerTransRunAtGoalToAttackOpp->setTargetState(Context::State::AttackOpp);
	playerTransRunAtGoalToAttackOpp->addCondition(playerCondAttackOpp);
	playerTransRunAtGoalToMakePass->setTargetState(Context::State::MakePass);
	playerTransRunAtGoalToMakePass->addCondition(playerCondMakePass);

	playerTransMakePassToChaseBall->setTargetState(Context::State::ChaseBall);
	playerTransMakePassToChaseBall->addCondition(playerCondChaseBall);
	playerTransMakePassToSupportBud->setTargetState(Context::State::SupportBud);
	playerTransMakePassToSupportBud->addCondition(playerCondSupportBud);
	playerTransMakePassToAttackOpp->setTargetState(Context::State::AttackOpp);
	playerTransMakePassToAttackOpp->addCondition(playerCondAttackOpp);


	/* Filling behaviour *//**/
	playerBehaviour->AddAction(Context::State::Idle, playerActIdle);
	playerBehaviour->AddAction(Context::State::ChaseBall, playerActChaseBall);
	playerBehaviour->AddAction(Context::State::GoatedRun, playerActGoatedRun);
	playerBehaviour->AddAction(Context::State::RunAtGoal, playerActRunAtGoal);
	playerBehaviour->AddAction(Context::State::SupportBud, playerActSupportBud);
	playerBehaviour->AddAction(Context::State::AttackOpp, playerActAttackOpp);
	playerBehaviour->AddAction(Context::State::MakePass, playerActMakePass);
	playerBehaviour->AddTransition(Context::State::Idle, playerTransIdleToChaseBall);
	playerBehaviour->AddTransition(Context::State::Idle, playerTransIdleToSupportBud);
	playerBehaviour->AddTransition(Context::State::Idle, playerTransIdleToAttackOpp);
	playerBehaviour->AddTransition(Context::State::ChaseBall, playerTransChaseBallToGoatedRun);
	playerBehaviour->AddTransition(Context::State::ChaseBall, playerTransChaseBallToSupportBud);
	playerBehaviour->AddTransition(Context::State::ChaseBall, playerTransChaseBallToAttackOpp);
	playerBehaviour->AddTransition(Context::State::SupportBud, playerTransSupportBudToGoatedRun);
	playerBehaviour->AddTransition(Context::State::SupportBud, playerTransSupportBudToChaseBall);
	playerBehaviour->AddTransition(Context::State::SupportBud, playerTransSupportBudToAttackOpp);
	playerBehaviour->AddTransition(Context::State::AttackOpp, playerTransAttackOppToGoatedRun);
	playerBehaviour->AddTransition(Context::State::AttackOpp, playerTransAttackOppToChaseBall);
	playerBehaviour->AddTransition(Context::State::AttackOpp, playerTransAttackOppToSupportBud);
	playerBehaviour->AddTransition(Context::State::GoatedRun, playerTransGoatedRunToRunAtGoal);
	playerBehaviour->AddTransition(Context::State::RunAtGoal, playerTransRunAtGoalToAttackOpp);
	playerBehaviour->AddTransition(Context::State::RunAtGoal, playerTransRunAtGoalToMakePass);


	playerBehaviour->AddTransition(Context::State::MakePass, playerTransMakePassToChaseBall);
	playerBehaviour->AddTransition(Context::State::MakePass, playerTransMakePassToSupportBud);
	playerBehaviour->AddTransition(Context::State::MakePass, playerTransMakePassToAttackOpp);

	/* Player creations *//**/
    Player* p1 = new Player(Context::Team::Blue, ATTACK_MIDDLE_BLUE, playerBehaviour, Context::FieldPlace::MidLane);
    mPlayerList.push_back(p1);
	Player* p2 = new Player(Context::Team::Blue, ATTACK_TOP_FRONT_BLUE, playerBehaviour, Context::FieldPlace::TopLane);
    mPlayerList.push_back(p2);
	Player* p3 = new Player(Context::Team::Blue, ATTACK_BOTTOM_FRONT_BLUE, playerBehaviour, Context::FieldPlace::BotLane);
    mPlayerList.push_back(p3);	
	Player* p4 = new Player(Context::Team::Blue, ATTACK_TOP_BACK_BLUE, playerBehaviour, Context::FieldPlace::TopLane);
    mPlayerList.push_back(p4);	
	Player* p5 = new Player(Context::Team::Blue, ATTACK_BOTTOM_BACK_BLUE, playerBehaviour, Context::FieldPlace::BotLane);
    mPlayerList.push_back(p5);

	Player* e1 = new Player(Context::Team::Red, ATTACK_MIDDLE_RED, playerBehaviour, Context::FieldPlace::MidLane);
	mPlayerList.push_back(e1);
	Player* e2 = new Player(Context::Team::Red, ATTACK_TOP_FRONT_RED, playerBehaviour, Context::FieldPlace::TopLane);
	mPlayerList.push_back(e2);
	Player* e3 = new Player(Context::Team::Red, ATTACK_BOTTOM_FRONT_RED, playerBehaviour, Context::FieldPlace::BotLane);
	mPlayerList.push_back(e3);
	Player* e4 = new Player(Context::Team::Red, ATTACK_TOP_BACK_RED, playerBehaviour, Context::FieldPlace::TopLane);
	mPlayerList.push_back(e4);	
	Player* e5 = new Player(Context::Team::Red, ATTACK_BOTTOM_BACK_RED, playerBehaviour, Context::FieldPlace::BotLane);
	mPlayerList.push_back(e5);

	/* Ball creation *//**/
    Ball * ball = new Ball(sf::Vector2f(640.f, 360.f));
	mBall = ball;
}

GameManager* GameManager::Instantiate()
{
	if (!mInstance)
    {
        mInstance = new GameManager();
        return mInstance;
    }
    return nullptr;
}
GameManager* GameManager::Get()
{
	return mInstance;
}


/*
  Getters & Setters
*//**/
void GameManager::setWindow(sf::RenderWindow* window)
{
	mWindow = window;
}

void GameManager::setDeltaTime(float deltaTime)
{
	mDeltaTime = deltaTime;
}

float GameManager::getDeltaTime() const
{
	return mDeltaTime;
}

Ball* GameManager::getBall() { return mBall; }

Context::Team GameManager::getBallTeamOwner()
{
	Player* owner = mBall->getOwner();
	if (owner == nullptr)
		return Context::Team::NONE;
	else
		return owner->getTeam();
}

Field* GameManager::getField()
{
	return mField;
}

/*
   Ball tools
*//**/
bool GameManager::isBallFree() { return getBallTeamOwner() == Context::Team::NONE ? true : false; }

void GameManager::forcePass()
{
	if (mBall->getOwner() != nullptr)
	{
		mBall->getOwner()->setState(Context::State::MakePass);
	}
}

/*
   Collision checkers
*//**/
void GameManager::checkCollisions()
{
	checkBallCollision();
	checkPlayersCollisions();
}
// Allows the ball to get a new owner if it currently doesn't have one (on the ground or being passed). Give priority to first member in mPlayerList
void GameManager::checkBallCollision()
{
	Player* lastOwner = mBall->getLastOwner();
	sf::FloatRect ballLocalBounds = mBall->getShape().getLocalBounds();
	sf::Vector2f ballCenter = mBall->getPosition() + sf::Vector2f{ ballLocalBounds.width / 2, ballLocalBounds.height / 2 };

	if (mField->isInGoal())
	{
		switch (mBall->getOwner()->getTeam())
		{
		case Context::Team::Blue:
			mScore->blueScore();
			reset(Context::Team::Red);
			break;

		case Context::Team::Red:
			mScore->redScore();
			reset(Context::Team::Blue);
			break;
		}
	}

	// Only checks for collision if the ball doesn't already have an owner
	else if (mBall->getOwner() == nullptr)
		for (Player* player : mPlayerList)
		{
			// Ignores the last owner (in case of a pass, to avoid lastOwner instantly grabbing it back)
			if (player == lastOwner) continue;
			
			sf::FloatRect playerLocalBounds = player->getShape().getLocalBounds();
			sf::Vector2f playerCenter = player->getPosition() + sf::Vector2f{ playerLocalBounds.width / 2, playerLocalBounds.height / 2 };
			sf::Vector2f centerDist { abs(ballCenter.x - playerCenter.x), abs(ballCenter.y - playerCenter.y) };

			// If the distance is smaller than both radius, detect collision and gives the Ball its new owner's pointer
			if (Utils::Vector2fGetNorm(centerDist) <= mBall->getRadius() + player->getRadius())
			{
				mBall->setOwner(player);
				break;
			}
		}	
}

void GameManager::checkPlayersCollisions()
{
	for (auto& checkedPlayer : mPlayerList)
	{
		mField->CheckIfInZone(checkedPlayer);

		sf::FloatRect checkedPLayerLocalBounds = checkedPlayer->getShape().getLocalBounds();
		sf::Vector2f checkedPlayerCenter = checkedPlayer->getPosition() + sf::Vector2f{ checkedPLayerLocalBounds.width / 2, checkedPLayerLocalBounds.height / 2 };

		for (auto& otherPlayer : mPlayerList)
		{
			/* Ignores collision with itself */
			if (checkedPlayer == otherPlayer) continue;
			
			sf::FloatRect othPlayerLocalBounds = otherPlayer->getShape().getLocalBounds();
			sf::Vector2f othPlayerCenter = otherPlayer->getPosition() + sf::Vector2f{ othPlayerLocalBounds.width / 2, othPlayerLocalBounds.height / 2 };
			sf::Vector2f centerDist{ abs(checkedPlayerCenter.x - othPlayerCenter.x), abs(checkedPlayerCenter.y - othPlayerCenter.y) };

			// If the distance is smaller than both radius, players need to push each other in some way
			if (Utils::Vector2fGetNorm(centerDist) <= checkedPlayer->getRadius() + otherPlayer->getRadius())
			{
				/* By default, each player will move the extra distance equally */
				float chkPlayerLambda = .6f, othPlayerLambda = .6f;

				/* If the collision involves a goated player, the other player will move the entire distance */
				if (checkedPlayer->getState() == Context::State::GoatedRun) {
					chkPlayerLambda = 0.f;
					othPlayerLambda = 1.2f;
				}
				if (otherPlayer->getState() == Context::State::GoatedRun) {
					chkPlayerLambda = 1.2f;
					othPlayerLambda = 0.f;
				}

				/* Determines the direcitonal vectors of both players and moves them */
				sf::Vector2f chkPlayerOldPos = checkedPlayer->getPosition();
				sf::Vector2f othPlayerOldPos = otherPlayer->getPosition();

				sf::Vector2f closestPosAllowed = (checkedPlayer->getRadius() + otherPlayer->getRadius()) * Utils::Vector2fNormalize(centerDist);
				sf::Vector2f extraDist = closestPosAllowed - centerDist;

				checkedPlayer->setPosition(chkPlayerOldPos + (extraDist * chkPlayerLambda));
				otherPlayer->setPosition(othPlayerOldPos + (extraDist * othPlayerLambda * -1.f));
			}
		}
	}
}

/*
   GameManager shenaningans
*/
void GameManager::Update()
{
	for (Player* player: mPlayerList)
	{
		player->Update();
	}
	mBall->Update();
	checkCollisions();
}

void GameManager::Draw()
{
	mField->Draw();
	mScore->printScore(mWindow);
	/* Draws the players */
	for (Player* player: mPlayerList)
	{
		mWindow->draw(player->getShape());
	}
	/* Draws the lonely ball */
	mWindow->draw(mBall->getShape());

}

void GameManager::CreateField()
{
	mField = new Field(mWindow);
}

//void GameManager::addEntity(Entity* entity)
//{
//	mEntityList.push_back(entity);
//}

std::vector<Player*>* GameManager::getPlayers()
{
	return &mPlayerList;
}


#ifdef _DEBUG
Player* GameManager::getPlayerFromMousePos(sf::Vector2f ARGmousePos)
{
	for (Player* player : mPlayerList)
	{
		sf::Vector2f distToMousePos = ARGmousePos - player->getPosition();
		if (Utils::Vector2fGetNorm(distToMousePos) <= player->getRadius())
			return player;
	}
	return nullptr;
}
#endif

void GameManager::reset(Context::Team teamWhoAttack)
{
	mBall->reset();
	std::stack<sf::Vector2f> bluePos;
	std::stack<sf::Vector2f> redPos;
	switch (teamWhoAttack)
	{
	case Context::Team::Blue:
		bluePos.push(ATTACK_BOTTOM_BACK_BLUE);
		bluePos.push(ATTACK_TOP_BACK_BLUE);
		bluePos.push(ATTACK_BOTTOM_FRONT_BLUE);
		bluePos.push(ATTACK_TOP_FRONT_BLUE);
		bluePos.push(ATTACK_MIDDLE_BLUE);

		redPos.push(DEFENSE_BOTTOM_BACK_RED);
		redPos.push(DEFENSE_TOP_BACK_RED);
		redPos.push(DEFENSE_BOTTOM_FRONT_RED);
		redPos.push(DEFENSE_TOP_FRONT_RED);
		redPos.push(DEFENSE_MIDDLE_RED);
		break;

	case Context::Team::Red:
		bluePos.push(DEFENSE_BOTTOM_BACK_BLUE);
		bluePos.push(DEFENSE_TOP_BACK_BLUE);
		bluePos.push(DEFENSE_BOTTOM_FRONT_BLUE);
		bluePos.push(DEFENSE_TOP_FRONT_BLUE);
		bluePos.push(DEFENSE_MIDDLE_BLUE);

		redPos.push(ATTACK_BOTTOM_BACK_RED);
		redPos.push(ATTACK_TOP_BACK_RED);
		redPos.push(ATTACK_BOTTOM_FRONT_RED);
		redPos.push(ATTACK_TOP_FRONT_RED);
		redPos.push(ATTACK_MIDDLE_RED);
		break;
	}

	for (auto& player : mPlayerList)
	{
		player->setState(Context::State::Idle);
		if (player->getTeam() == Context::Team::Blue)
		{
			player->setPosition(bluePos.top());
			bluePos.pop();
		}

		else
		{
			player->setPosition(redPos.top());
			redPos.pop();
		}
	}
}