import Router from "@koa/router"
import * as yup from "yup"
import { MAX_TTL, PUBLIC_URL } from "../config"
import { db } from "../db"
import { getUniqueId } from "../id"
import { validate } from "../middleware/validate"
import { allowedOrigin } from "../validation/allowedOrigin"

export const router = new Router()

const schema = yup.object().shape({
  url: allowedOrigin.required(),
  ttl: yup.number().positive().integer().max(MAX_TTL).default(MAX_TTL),
})

router.post("/create", validate(schema), async (context) => {
  const { url, ttl } = context.request.body

  const id = await getUniqueId()
  await db.set(id, url, "PX", ttl * 1000)

  context.body = {
    id,
    url: `${PUBLIC_URL ?? context.origin}/go/${id}`,
    expires: new Date(Date.now() + ttl * 1000),
  }
})
