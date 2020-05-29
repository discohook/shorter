import Router from "@koa/router"
import Koa from "koa"
import bodyParser from "koa-bodyparser"
import { router as createRouter } from "./routes/create"
import { router as goRouter } from "./routes/go"

const app = new Koa()
const router = new Router()

app.use(bodyParser())

router.use(createRouter.routes())
router.use(goRouter.routes())

app.use(router.routes())

const port = Number(process.env.PORT ?? 8000)
app.listen(port, () => {
  console.log(`App ready on http://127.0.0.1:${port}/`)
})
