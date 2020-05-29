import Router from "@koa/router"
import shortid from "shortid"
import * as yup from "yup"
import { db } from "../db"
import { validate } from "../middleware/validate"
export const router = new Router()

const schema = yup.object().shape({
  url: yup.string().url().required(),
})

router.post("/create", validate(schema), async (context) => {
  const { url } = context.request.body

  const id = shortid()
  await db.set(id, url, "EX", 60 * 60 * 6)

  context.body = {
    id,
    url: `${context.origin}/go/${id}`,
  }
})
