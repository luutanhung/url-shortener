# Stage 1: Build the app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first
COPY package.json package-lock.json ./

# Install all dependencies including devDependencies (needed for build)
RUN npm ci

# Copy source code
COPY . .

ARG API_URL
ENV NEXT_PUBLIC_API_URL=$API_URL

# Build the Next.js app
RUN npm run build

# Stage 2: Run the app
FROM node:20-alpine AS runner

WORKDIR /app

# Only copy necessary files from build stage
COPY --from=builder /app/package.json ./
COPY --from=builder /app/package-lock.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.mjs ./

# Install only production dependencies
RUN npm ci --omit=dev

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Start the Next.js server
CMD ["npm", "start"]
