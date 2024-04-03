# ESDG5T3

---

# Project Title : Spick

## Overview

Spick is a free event management platform designed to tackle the challenges of scheduling and coordinating meetings or events for all. It offers a solution to frequent scheduling conflicts and disjointed communication by providing a central system for scheduling meetings and responding to invites. The application enhances productivity by finding the best meeting times for all attendees and suggests conveniently located venues, simplifying the booking process.

## Prerequisites

Makre sure all of these are running and installed on your local machine before you start the project:

-   Docker
-   Node.js

## Installation

```
git clone https://github.com/bokiex/Spick.git
cd spick
```

1. Backend Setup: To set up the backend, navigate to the flask-server directory and use Docker Compose to build and run the project:

```
// You should be in Spick/flask-server
cd flask-server
docker-compose up --build
```

1. Frontend Setup: Open a new terminal window or tab for the frontend setup. Navigate to the frontend directory, install the necessary packages, and start the development server:

```
// You should be in Spick/frontend/
npm install
npm run dev
```

This will start the frontend development server. Make sure you have Node.js and npm installed on your machine.

---
