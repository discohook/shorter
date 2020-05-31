import Router from "@koa/router"
import Koa from "koa"
import bodyParser from "koa-bodyparser"
import { PORT } from "./config"
import { router as createRouter } from "./routes/create"
import { router as goRouter } from "./routes/go"

const app = new Koa()
const router = new Router()

app.use(bodyParser())

router.use(createRouter.routes())
router.use(goRouter.routes())

app.use(router.routes())

app.listen(PORT, () => {
  console.log(`App ready on http://127.0.0.1:${PORT}/`)
})
