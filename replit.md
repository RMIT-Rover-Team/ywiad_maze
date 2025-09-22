# Overview

This project is an educational programming workshop for RMIT Rover x YWiAD, designed to teach programming fundamentals through a Mars rover escape game. Students learn basic programming logic by implementing movement algorithms for a rover navigating obstacles in a cave-like environment on Mars. The project uses Python and Pygame to create an interactive 2D game where students program a rover to find the exit using wall-following algorithms.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Game Engine**: Built on Pygame framework for 2D graphics rendering and game loop management
- **Display System**: 800x580 pixel window with separate game area (480px) and UI area (100px)
- **Tile-Based Grid**: 40x40 pixel tiles creating a grid-based world for simplified movement and collision detection
- **Sprite System**: Image-based rendering for rover, walls, goals, and environmental elements

## Game Logic Architecture
- **State Management**: Simple variable-based state tracking for rover position (x, y coordinates) and orientation (0-3 directional values)
- **Movement System**: Grid-based movement with collision detection and boundary checking
- **Algorithm Implementation**: Wall-follower pathfinding algorithm for autonomous navigation
- **Event-Driven Updates**: Pygame event loop handling user interactions and game state updates

## Code Structure
- **Modular Functions**: Separate functions for movement validation (`can_move`), directional changes (`turn_left`, `turn_right`), and rover movement (`move_rover`)
- **Educational Progression**: Step-by-step implementation approach with clearly defined phases from setup to algorithm implementation
- **Constants Configuration**: Centralized game settings for easy modification of window size, tile dimensions, and colors

# External Dependencies

## Core Framework
- **Pygame**: Primary game development library for graphics, input handling, and game loop management
- **Python Standard Library**: 
  - `sys` module for system operations
  - `random` module for procedural generation (if implemented in extensions)

## Asset Management
- **Image Assets**: Sprite files for rover, walls, background, and goal markers (referenced but not included in current codebase)
- **Font Rendering**: Pygame's built-in font system for UI text display

## Development Platform
- **Replit Integration**: Designed to run entirely in web browser environment through Replit's online IDE
- **Web-Based Deployment**: No local installation required, accessible via shared Replit links