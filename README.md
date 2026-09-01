# Success Journal – Academics & Lifestyle Planner

A full-stack productivity and lifestyle management web application that brings academic planning, personal activity tracking, and AI assistance together in one platform.

## Overview

Success Journal is designed to help users organize their academic responsibilities while maintaining healthy daily routines. The application provides separate modules for managing assignments, notes, daily tasks, weekly planning, and lifestyle activities such as sleep, water intake, and workouts.

An integrated AI assistant is also included to provide academic assistance, productivity guidance, and general wellness suggestions.

## Features

### Academic Management

- Assignment management
- Daily task management
- Notes management
- Weekly academic planner
- Create, view, update, and delete operations

### Lifestyle Tracking

- Water intake tracking
- Sleep tracking
- Workout tracking
- Activity and progress monitoring

### AI Assistant

- Integrated Google Gemini API
- Academic question assistance
- Productivity suggestions
- General wellness recommendations

### Data Management

- MySQL database integration
- Persistent storage of application data
- Structured relational data management
- CRUD operations across application modules

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| AI | Google Gemini API |
| Development | VS Code |
| Version Control | Git / GitHub |

## Application Architecture

The application follows a client-server architecture in which the frontend communicates with the Flask backend. The backend handles application logic and database operations, while the Gemini API provides AI-assisted functionality.

```text
User
  |
  v
Web Interface
(HTML / CSS / JavaScript)
  |
  v
Flask Application
  |
  +------> MySQL Database
  |
  +------> Google Gemini API
