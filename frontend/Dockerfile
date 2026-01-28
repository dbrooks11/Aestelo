# STAGE 1: Build
FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci 
COPY . .

# STAGE 2: Development
FROM base AS development
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

# STAGE 3: Build Production Artifacts
FROM base AS build
RUN npm run build

# STAGE 4: Production Server (Non-Root Nginx)
FROM nginxinc/nginx-unprivileged:alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
