# Use a lightweight Node image
FROM node:22-alpine

WORKDIR /app

# Copy package files first
COPY package*.json ./
RUN npm install

# Copy the rest
COPY . .

EXPOSE 5173

# "--host" is required for Vite to work in Docker
CMD ["npm", "run", "dev", "--", "--host"]