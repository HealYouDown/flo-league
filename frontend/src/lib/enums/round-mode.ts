import type { RoundMode } from "@/api/generated"

export const ROUND_MODE_LABELS: Record<RoundMode, string> = {
  1: "1 vs. 1",
  2: "2 vs. 2",
  3: "3 vs. 3",
  4: "4 vs. 4",
  5: "5 vs. 5",
  6: "6 vs. 6",
}

export const ROUND_MODE_OPTIONS = Object.entries(ROUND_MODE_LABELS).map(([value, label]) => ({
  value: Number(value) as RoundMode,
  label,
}))
