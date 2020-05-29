import Router from "@koa/router"
import { db } from "../db"

export const router = new Router()

router.get("/go/:id", async (context) => {
  const { id } = context.params

  const location = await db.get(id)

  if (!location) {
    context.status = 404
    context.body = "Not Found"
    return
  }

  context.redirect(location)
})
