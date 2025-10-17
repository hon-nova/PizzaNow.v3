# === Stage 1: Build the Vite app ===
FROM node:20 AS build

WORKDIR /app

# Copy only dependency files first for better caching
COPY package*.json ./
COPY tsconfig*.json ./

RUN npm ci

COPY . .

ARG VITE_AUTH_BACKEND_URL
ARG VITE_PROFILE_BACKEND_URL
ARG VITE_BOT_BACKEND_URL
ARG VITE_PAYPAL_BACKEND_URL
ARG VITE_PAYPAL_CLIENT_ID

RUN echo "VITE_AUTH_BACKEND_URL=$VITE_AUTH_BACKEND_URL" >> .env \
 && echo "VITE_PROFILE_BACKEND_URL=$VITE_PROFILE_BACKEND_URL" >> .env \
 && echo "VITE_BOT_BACKEND_URL=$VITE_BOT_BACKEND_URL" >> .env \
 && echo "VITE_PAYPAL_BACKEND_URL=$VITE_PAYPAL_BACKEND_URL" >> .env \
 && echo "VITE_PAYPAL_CLIENT_ID=$VITE_PAYPAL_CLIENT_ID" >> .env

RUN npm run build

# === Stage 2: Serve with NGINX ===
FROM nginx:1.25-alpine

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.prod.conf /etc/nginx/conf.d/nginx.prod.conf

EXPOSE 80

# Run NGINX
CMD ["nginx", "-g", "daemon off;"]
