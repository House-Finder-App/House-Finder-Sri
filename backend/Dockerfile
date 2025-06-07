# Use Node.js LTS as the base image
FROM node:18-bullseye

# Install OpenCV dependencies and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libopencv-dev \
    python3-opencv \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies)
RUN npm install --no-package-lock && npm install opencv-build && npm install opencv4nodejs

# Copy the rest of the source code
COPY . .

# Download the cascade classifier
RUN mkdir -p models && \
    curl -L https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -o models/haarcascade_frontalface_default.xml

# Build TypeScript
RUN npm run build

# Expose port
EXPOSE 5000

# Start the app using compiled JavaScript
CMD ["node", "dist/index.js"] 