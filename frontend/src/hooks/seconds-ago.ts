import { useEffect, useState } from "react"

export function useSecondsAgo(timestamp?: number) {
  const [secondsAgo, setSecondsAgo] = useState(0)

  useEffect(() => {
    if (!timestamp) return

    const update = () => setSecondsAgo(Math.floor((Date.now() - timestamp) / 1000))

    update()

    const interval = setInterval(update, 1000)
    return () => clearInterval(interval)
  }, [timestamp])

  return secondsAgo
}
