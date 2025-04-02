#pragma once
namespace Context
{
    enum class State 
    {
        // Ajoutez vos états ici
        UNKNOWN = 0,
        Idle,
        ChaseBall,
        GoatedRun,
        RunAtGoal,
        SupportBud,
        AttackOpp,
        MakePass,
    };
    enum class Team
    {
        NONE = 0,
        Blue,
        Red
    };

    // Used for an Entity to "remember" derived type it is
    enum class EntityType
    {
        Player = 0,
        Ball,
    };
    enum class FieldPlace
    {
        UNKNOWN = 0,
        BackField,
        BlueGoal,
        RedGoal,
        TopLane,
        MidLane,
        BotLane,
    };
};
