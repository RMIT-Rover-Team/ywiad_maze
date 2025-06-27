# Cave Explorer Game

## Overview

This is a 2D cave exploration game built with Python and Pygame. The game features a procedurally generated cave environment with tile-based graphics and wall-following algorithms. The application is designed as a single-player exploration game where players can navigate through dynamically created cave systems.

## System Architecture

The application follows a simple monolithic architecture with a single main.py file containing all game logic. The architecture is structured around object-oriented programming principles with clear separation of concerns:

- **Game Loop**: Standard Pygame game loop handling events, updates, and rendering
- **Environment System**: Cave generation and tile management
- **Rendering System**: Sprite-based tile rendering with fallback graphics
- **Input System**: Pygame event handling for user interaction

## Key Components

### CaveEnvironment Class
- **Purpose**: Manages the cave world, including tile generation and sprite loading
- **Responsibilities**: 
  - Procedural cave generation using numpy arrays
  - Tileset loading with fallback mechanisms
  - Tile state management
- **Data Structure**: Uses 2D numpy array for efficient tile storage

### Graphics System
- **Tile-based Rendering**: 32x32 pixel tiles for consistent visual presentation
- **Asset Management**: Supports external cave.png tileset with automatic fallback
- **Color Palette**: Predefined color constants for consistent theming

### Constants and Configuration
- **Screen Resolution**: 1024x768 optimized for desktop gameplay
- **Performance**: 60 FPS target for smooth gameplay
- **Grid System**: 32-pixel tile size for balanced detail and performance

## Data Flow

1. **Initialization**: Pygame initializes, screen setup, environment creation
2. **Cave Generation**: Procedural algorithm creates cave layout in numpy array
3. **Asset Loading**: Attempts to load tileset, falls back to generated graphics
4. **Game Loop**: Event handling → Update logic → Rendering → Frame timing
5. **Tile Rendering**: Environment tiles mapped to screen coordinates

## External Dependencies

### Core Dependencies
- **Pygame**: Primary game engine for graphics, input, and audio
- **NumPy**: Efficient array operations for cave generation and tile management
- **Python Standard Library**: sys, os, math modules for core functionality

### Asset Dependencies
- **Optional Tileset**: assets/cave.png (256x256 tile sheet)
- **Fallback Graphics**: Programmatically generated tiles when assets unavailable

## Deployment Strategy

The application is designed for local execution with minimal setup requirements:

- **Platform**: Cross-platform Python application
- **Dependencies**: pip-installable packages (pygame, numpy)
- **Assets**: Optional external graphics with built-in fallbacks
- **Configuration**: All settings defined as constants in main.py

## Changelog

- June 27, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.