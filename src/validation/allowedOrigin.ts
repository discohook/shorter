import * as yup from "yup"
import { ALLOWED_SHORTEN_ORIGINS } from "../config"

export const allowedOrigin = yup
  .string()
  .url()
  .test({
    name: "-allowed-origin",
    message: "${path} must be in origin whitelist",
    test: function (value) {
      // Allowed origins list is empty, allow all by default
      if (ALLOWED_SHORTEN_ORIGINS.size === 0) return true

      try {
        const url = new URL(value)
        return ALLOWED_SHORTEN_ORIGINS.has(url.origin)
      } catch {}
      return false
    },
  })
