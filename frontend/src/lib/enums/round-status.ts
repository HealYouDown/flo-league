import type { RoundStatus } from "@/api/generated"

export const ROUND_STATUS_LABELS: Record<RoundStatus, string> = {
  1: "Draft",
  2: "Running",
  3: "Finished",
}

export const ROUND_STATUS_OPTIONS = Object.entries(ROUND_STATUS_LABELS).map(([value, label]) => ({
  value: Number(value) as RoundStatus,
  label,
}))
