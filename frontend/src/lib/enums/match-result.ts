import type { MatchResult } from "@/api/generated"

export const MATCH_RESULT_LABELS: Record<MatchResult, string> = {
  1: "Unset",
  2: "Canceled",
  3: "Win Team 1",
  4: "Win Team 2",
  5: "Draw",
}

export const MATCH_RESULT_OPTIONS = Object.entries(MATCH_RESULT_LABELS).map(([value, label]) => ({
  value: Number(value) as MatchResult,
  label,
}))
