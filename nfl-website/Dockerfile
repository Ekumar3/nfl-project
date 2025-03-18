# Use an official lightweight Nginx image
FROM nginx:alpine

# Copy the React build files to Nginx's web root
COPY dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginxt when the container starts
CMD ["nginx", "-g", "daemon off;"]
