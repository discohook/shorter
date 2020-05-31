export const PORT = Number(process.env.PORT ?? 8000)
export const PUBLIC_URL = process.env.PUBLIC_URL

export const REDIS_HOST = process.env.REDIS_HOST ?? "127.0.0.1"
export const REDIS_PORT = Number(process.env.REDIS_PORT ?? 6379)

export const ALLOWED_SHORTEN_ORIGINS = new Set(
  process.env.ALLOWED_SHORTEN_ORIGINS?.split(","),
)
