#include <SFML/System/Vector2.hpp>
#include <cmath>

namespace Utils 
{

sf::Vector2f Vector2fNormalize(const sf::Vector2f& vector)
{
    float magnitude = std::sqrt(vector.x * vector.x + vector.y * vector.y);

    if (magnitude == 0) {
        return { 0, 0 };
    }

    sf::Vector2f normalized = { vector.x / magnitude, vector.y / magnitude };

    return normalized;
}

float Vector2fGetNorm(const sf::Vector2f& vector) { return std::sqrt(vector.x * vector.x + vector.y * vector.y); }

// wtf ???
float GetDeltaTime()
{
    return 0.016f;
}

}
