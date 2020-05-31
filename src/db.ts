import Redis from "ioredis"
import { REDIS_HOST, REDIS_PORT } from "./config"

export const db = new Redis(REDIS_PORT, REDIS_HOST)
