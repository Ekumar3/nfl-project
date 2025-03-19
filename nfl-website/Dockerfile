# Step 1: Build the React app
FROM node:18 AS build

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all project files and build React app
COPY . .
RUN npm run build

# Step 2: Serve the React app using Nginx
FROM nginx:alpine

# Copy built React app from previous step to Nginx's web root
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for web traffic
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]