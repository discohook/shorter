import Router from "@koa/router"
import * as yup from "yup"
import { PUBLIC_URL } from "../config"
import { db } from "../db"
import { validate } from "../middleware/validate"
import { nanoid } from "../nanoid"
import { allowedOrigin } from "../validation/allowedOrigin"

export const router = new Router()

const schema = yup.object().shape({
  url: allowedOrigin.required(),
})

router.post("/create", validate(schema), async (context) => {
  const { url } = context.request.body

  const id = await nanoid()
  await db.set(id, url, "EX", 60 * 60 * 6)

  context.body = {
    id,
    url: `${PUBLIC_URL ?? context.origin}/go/${id}`,
  }
})
