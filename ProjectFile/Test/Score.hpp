#pragma once
namespace sf
{
	class RenderWindow;
	class Font;
	class Text;
}

class Score
{
	short mBlueScore;
	short mRedScore;
	sf::Font* mFont;
	sf::Text* mText;

public:
	Score();
	~Score() { delete mFont; delete mText; };
	void printScore(sf::RenderWindow* window);
	void blueScore();
	void redScore();
};

