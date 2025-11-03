# Single-stage: Build and serve with Node
FROM node:18-alpine

WORKDIR /app

# Copy package files and install all deps (including serve for runtime)
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source and build
COPY . .
RUN npm run build

# Install serve globally for runtime (or add to package.json as dep)
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the build folder
CMD ["serve", "-s", "build", "-l", "3000"]