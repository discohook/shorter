import Router from "@koa/router"
import * as yup from "yup"
import { MAX_TTL, PUBLIC_URL } from "../config"
import { db } from "../db"
import { validate } from "../middleware/validate"
import { nanoid } from "../nanoid"
import { allowedOrigin } from "../validation/allowedOrigin"

export const router = new Router()

const schema = yup.object().shape({
  url: allowedOrigin.required(),
  ttl: yup.number().positive().integer().max(MAX_TTL).default(MAX_TTL),
})

router.post("/create", validate(schema), async (context) => {
  const { url, expires } = context.request.body

  const id = await nanoid()

  const expiresAt = new Date(Date.now() + expires * 1000)
  await db.set(id, url)
  await db.pexpireat(id, expiresAt.getTime())

  context.body = {
    id,
    url: `${PUBLIC_URL ?? context.origin}/go/${id}`,
    expires: expiresAt,
  }
})
