import Redis from "ioredis"

export const db = new Redis(
  Number(process.env.REDIS_PORT ?? 6379),
  process.env.REDIS_HOST ?? "127.0.0.1",
)
