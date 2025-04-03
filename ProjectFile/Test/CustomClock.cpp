#include "CustomClock.hpp"

namespace
{
	static CustomClock* _Instance = nullptr;
}

/*
   Constru & Destru
*//**/
CustomClock::CustomClock() { mTimeElapsed_MS = 0; }
CustomClock::~CustomClock() { /* Does nothing */ }
CustomClock* CustomClock::Instantiate()
{
	if (_Instance == nullptr)
	{
		_Instance = new CustomClock();
		return _Instance;
	}
	return nullptr;
}
CustomClock* CustomClock::Get() { return _Instance; }


/*
   Time-related
*//**/
void CustomClock::reset() { mTimeStamp = mClock.restart(); }
void CustomClock::setTimeElasped_MS() { mTimeElapsed_MS = mTimeStamp.asMilliseconds(); }
void CustomClock::setTimeElasped_MS(int ARGtime_MS) { mTimeElapsed_MS = ARGtime_MS; }
unsigned int CustomClock::getTimeElapsed_MS() { return mTimeElapsed_MS; }