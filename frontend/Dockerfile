ARG NODE_VERSION=20-alpine

# 1. deps — install exactly the locked dependencies
FROM node:${NODE_VERSION} AS deps
WORKDIR /app
# libc compat for some native deps on alpine
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json ./
RUN npm ci

# 2. builder — compile the app
FROM node:${NODE_VERSION} AS builder
WORKDIR /app
RUN apk add --no-cache libc6-compat

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build-time env vars (NEXT_PUBLIC_* are inlined into the bundle at build time).
# Override via --build-arg if needed.
ARG NEXT_PUBLIC_API_BASSE_URL
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASSE_URL}
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build


# 3. runner — minimal production runtime
FROM node:${NODE_VERSION} AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3002
ENV HOSTNAME=0.0.0.0


# Run as an unprivileged user
RUN addgroup --system --gid 1001 nodejs \
  && adduser --system --uid 1001 nextjs

# Static assets and the standalone server output
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3002

# server.js is emitted by Next's standalone output
CMD ["node", "server.js"]