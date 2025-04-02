#pragma once

#include <SFML/System/Clock.hpp>

class CustomClock
{
private:
	sf::Clock mClock;
	sf::Time mTimeStamp;
	unsigned int mTimeElapsed_MS;

	CustomClock();

public:
	static CustomClock* Instantiate();
	static CustomClock* Get();
	~CustomClock();
	
	/* Time-related *//**/
	void reset();
	void setTimeElasped_MS();
	void setTimeElasped_MS(int ARGtime_MS);
	unsigned int getTimeElapsed_MS();
};

