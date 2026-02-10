# Dockerfile for Frontend React Dashboard
# Multi-stage build: development and production

# ============================================================================
# STAGE 1: Development (with hot-reload via Vite)
# ============================================================================
FROM node:20-alpine AS development

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start development server with hot-reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ============================================================================
# STAGE 2: Build (compile React app)
# ============================================================================
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Set production environment variables for build
ARG VITE_PHISHING_API_URL=http://localhost:8000
ARG VITE_ATO_API_URL=http://localhost:8001
ARG VITE_BRUTE_FORCE_API_URL=http://localhost:8002
ARG VITE_AUTH_API_URL=http://localhost:8003
ARG VITE_API_TIMEOUT=10000
ARG VITE_DEBUG_MODE=false

ENV VITE_PHISHING_API_URL=$VITE_PHISHING_API_URL \
    VITE_ATO_API_URL=$VITE_ATO_API_URL \
    VITE_BRUTE_FORCE_API_URL=$VITE_BRUTE_FORCE_API_URL \
    VITE_AUTH_API_URL=$VITE_AUTH_API_URL \
    VITE_API_TIMEOUT=$VITE_API_TIMEOUT \
    VITE_DEBUG_MODE=$VITE_DEBUG_MODE

# Build the application
RUN npm run build

# ============================================================================
# STAGE 3: Production (serve with Nginx)
# ============================================================================
FROM nginx:alpine AS production

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built static files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
