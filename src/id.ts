import { customAlphabet } from "nanoid/async"
import { db } from "./db"

const alphabet = "123456789abcdefghjkmnpqrstuvwxyz"

export const getUniqueId = async () => {
  let attempt = 0
  let length = 8
  let nanoid = customAlphabet(alphabet, length)

  while (true) {
    attempt += 1

    const id = await nanoid()
    if (!db.exists(id)) {
      return id
    }

    if (attempt >= 16) {
      attempt = 0
      length += 1
      nanoid = customAlphabet(alphabet, length)
    }
  }
}
