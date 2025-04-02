#pragma once

#include <SFML/System/Vector2.hpp>

namespace Utils
{
	sf::Vector2f Vector2fNormalize(const sf::Vector2f& vector);
	float Vector2fGetNorm(const sf::Vector2f& vector);
}