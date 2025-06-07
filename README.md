# House Finder App

## Project Overview

This project is a mobile application (using React Native + Expo) that identifies houses from photos and returns Zillow property links. The backend (FastAPI) captures location data, uses computer vision (CLIP) to match the photo against nearby properties (within a 50-meter radius), and returns the most similar property's Zillow listing.

## Project Organization

- **backend/** – Contains the FastAPI (Python) backend (models, services, API endpoints, Dockerfile, etc.)
- **house-finder-app/** – Contains the React Native (Expo) frontend (screens, components, services, stores, etc.)
- **docker-compose.yml** – Orchestrates the backend (FastAPI), frontend (Expo), and database (PostGIS) services.

## Prerequisites

- Docker (and Docker Compose) installed.
- Node (and npm) installed (for local frontend development).
- (Optional) Expo CLI installed (`npm install -g expo-cli`).

## Running the Backend (using Docker Compose)

1. (Optional) Create a `.env` file (or set environment variables) for your backend (for example, ZILLOW_API_KEY, AWS keys, etc.).  
2. From the project root, run:

   ```bash
   docker-compose up --build
   ```

   This starts the backend (FastAPI) and the PostGIS database. The backend is available at [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health).

## Running the Frontend (using Expo)

### Option 1: Using Docker Compose (integrated)

- The `docker-compose.yml` file now includes a "frontend" service (using a Node image) that mounts the `house-finder-app` folder and runs Expo (in production mode).  
- (Note: In production, you might want to build a static bundle or use a CI/CD pipeline.)

### Option 2: Local Development (using Expo CLI)

1. Navigate into the frontend folder:

   ```bash
   cd house-finder-app
   ```

2. Install dependencies (if not already done):

   ```bash
   npm install
   ```

3. Start the Expo development server:

   ```bash
   npx expo start
   ```

   (You can then run the app on an iOS simulator, Android emulator, or a physical device using Expo Go.)

## Additional Notes

- **Backend:**  
  - The backend (FastAPI) is built using Python (FastAPI, SQLAlchemy, geoalchemy2, CLIP, etc.).  
  - The Dockerfile (in `backend/`) installs system dependencies (for OpenCV) and Python dependencies (from `backend/requirements.txt`).  
  - The backend's "func" (for PostGIS functions) is imported from `sqlalchemy.sql` (not from geoalchemy2).

- **Frontend:**  
  - The frontend (React Native + Expo) is located in the `house-finder-app` folder.  
  - It uses Expo's Camera, Location, and Image Manipulator modules (installed via `expo install expo-camera expo-location expo-image-manipulator`).  
  - The app's entry point (`App.js`) sets up navigation (using React Navigation) and a global state (using Zustand).

- **Docker Compose:**  
  - The `docker-compose.yml` orchestrates the backend, frontend (if integrated), and the PostGIS database.  
  - (Optional) You can remove the "version" attribute (as it is obsolete) to avoid warnings.

- **Environment Variables:**  
  - (Optional) Create a `.env` file (or set environment variables) for your backend (for example, `DATABASE_URL`, `ZILLOW_API_KEY`, AWS keys, etc.).  
  - (Optional) For the frontend, you can use Expo's app.config (or a .env file) if needed.

---

Happy coding! 