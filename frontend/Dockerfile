# STAGE 1: Build
FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# STAGE 2: Development (Stop here for local work)
FROM base AS development
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

# STAGE 3: Build (Only runs when creating a production image)
FROM base AS build
RUN npm run build

# STAGE 4: Production Server (Nginx)
FROM nginx:stable-alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]