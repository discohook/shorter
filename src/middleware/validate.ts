import { Middleware } from "koa"
import { Schema } from "yup"

export const validate = <T>(schema: Schema<T>): Middleware => {
  return async (context, next) => {
    try {
      const body = await schema.validate(context.request.body, {
        abortEarly: false,
        stripUnknown: true,
      })

      context.request.body = body

      await next()
    } catch (error) {
      if (error.name !== "ValidationError") throw error

      context.response.status = 400
      context.response.body = error
    }
  }
}
