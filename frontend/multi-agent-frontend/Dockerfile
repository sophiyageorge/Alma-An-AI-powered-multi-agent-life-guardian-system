# frontend/Dockerfile (Dev Mode)
FROM node:20

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the source code
COPY . .

# Expose the port your dev server will run on
EXPOSE 3000

# Start React development server
CMD ["npm", "run", "dev"]


# # frontend/Dockerfile
# # Step 1: build react app
# FROM node:20 AS build

# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# # Step 2: serve build with nginx
# FROM nginx:alpine
# # COPY --from=build /app/build /usr/share/nginx/html

# # Copy custom nginx config if you want
# # COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]