# === Stage 1: Build the Vite app ===
FROM node:20 AS build

WORKDIR /app

# Copy only dependency files first for better caching
COPY package*.json ./
COPY tsconfig*.json ./

RUN npm ci

COPY . .

# Build Vite app
RUN npm run build

# === Stage 2: Serve with NGINX ===
FROM nginx:1.25-alpine

# Create the mount directory
RUN mkdir -p /etc/config

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

# Run NGINX
CMD ["nginx", "-g", "daemon off;"]
