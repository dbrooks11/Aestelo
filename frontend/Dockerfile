# STAGE 1: Dependencies
FROM node:22-alpine AS deps
WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# STAGE 2: Build 
FROM deps AS build
WORKDIR /app

COPY . .

RUN pnpm run build

# STAGE 3: Production Server (Non-Root Nginx)
FROM nginxinc/nginx-unprivileged:alpine AS prod

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
