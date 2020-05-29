import Router from "@koa/router"
import shortid from "shortid"
import * as yup from "yup"
import { db } from "../db"
import { validate } from "../middleware/validate"

export const router = new Router()

const schema = yup.object().shape({
  url: yup.string().url().required(),
})

const PUBLIC_URL = process.env.PUBLIC_URL
const ALLOWED_SHORTEN_ORIGINS = new Set(
  process.env.ALLOWED_SHORTEN_ORIGINS?.split(","),
)

router.post("/create", validate(schema), async (context) => {
  const { url } = context.request.body

  if (
    ALLOWED_SHORTEN_ORIGINS.size > 0 &&
    !ALLOWED_SHORTEN_ORIGINS.has(new URL(url).origin)
  ) {
    context.status = 400
    context.body = {
      message: "URL not in allowed origins",
    }
    return
  }

  const id = shortid()
  await db.set(id, url, "EX", 60 * 60 * 6)

  context.body = {
    id,
    url: `${PUBLIC_URL ?? context.origin}/go/${id}`,
  }
})
