#include <SFML/Graphics.hpp>
#include <iostream>
#include "GameManager.hpp"
#include "CustomClock.hpp"

#ifdef _DEBUG
#include "Player.hpp"
#endif

int main(void)
{
    sf::RenderWindow window(sf::VideoMode(1280, 720), "GamingCampus - Rugby - IA/StateMachines");
    window.setFramerateLimit(60);

    sf::Font font;
    if (!font.loadFromFile("./Hack-Regular.ttf"))
    {
        std::cerr << "Failed to load font" << std::endl;
        return -1;
    }

    CustomClock* clock = CustomClock::Instantiate();
    GameManager* game_manager = GameManager::Instantiate();
    game_manager->Init(&window);

    #ifdef _DEBUG
    bool debugPause = false;
    sf::Vector2f instantMoveMouseStartingPoint;
    Player* instantMoveTarget = nullptr;
    #endif

    while (window.isOpen())
    {
        /* Start counting time for the next loop */
        clock->reset();

        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed  ||  (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Escape))
                window.close();

            #ifdef _DEBUG
            // Start forced instant move
            if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Right)
            {
                /* Artificially pauses the game and sets the moving Player with the first position of the cursor */
                debugPause = true;
                instantMoveMouseStartingPoint = { static_cast<float>(event.mouseButton.x), static_cast<float>(event.mouseButton.y) };
                instantMoveTarget = game_manager->getPlayerFromMousePos(instantMoveMouseStartingPoint);
            }
            if (event.type == sf::Event::MouseMoved && debugPause)
            {
                /* If we did not click on anything, ignores this */
                if (instantMoveTarget != nullptr)
                {
                    /* Moves the Player of the distance moves by the curosr, and reset the cursor's starting point */
                    sf::Vector2f curPlayerPos = instantMoveTarget->getPosition();
                    sf::Vector2f distMouseMoved{ static_cast<float>(event.mouseMove.x) - instantMoveMouseStartingPoint.x, static_cast<float>(event.mouseMove.y) - instantMoveMouseStartingPoint.y };
                    std::cout << "Init: " << instantMoveMouseStartingPoint.x << ", " << instantMoveMouseStartingPoint.y << " | Moved: " << distMouseMoved.x << ", " << distMouseMoved.y << std::endl;;
                    instantMoveTarget->setPosition(curPlayerPos + distMouseMoved);
                    instantMoveMouseStartingPoint = { static_cast<float>(event.mouseMove.x), static_cast<float>(event.mouseMove.y) };
                }
            }
            if (event.type == sf::Event::MouseButtonReleased && event.mouseButton.button == sf::Mouse::Right)
            {
                /* Stops the artificial game pause */
                debugPause = false;
            }   
            
            if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Middle)
            {
                game_manager->forcePass();
            }
            #endif
        }

        window.clear();

        //if (!debugPause)
            game_manager->Update();
        game_manager->Draw();

        window.display();

        /* Stop couting time for the next loop */
        clock->setTimeElasped_MS();
        #ifdef _DEBUG
        if (debugPause) clock->setTimeElasped_MS(0);
        #endif
        game_manager->setDeltaTime((float)clock->getTimeElapsed_MS() / 1000);
    }
}
