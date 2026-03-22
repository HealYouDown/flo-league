# Stage 1: Build
FROM node:24-bullseye AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./  
RUN npm ci

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Pass API URL as build argument
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the frontend for production
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.29-alpine

# Copy the built files from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]