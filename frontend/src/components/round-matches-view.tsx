import { RoundStatus } from "@/api/generated"
import { useGetRound, useGetRoundMatches } from "@/api/hooks/rounds"
import { LoadingIndicator } from "@/components/loading-indicator"
import { MatchCard } from "@/components/match-card"
import { useSecondsAgo } from "@/hooks/seconds-ago"

interface RunningViewProps {
  id: number
}

export function RoundMatchesView({ id }: RunningViewProps) {
  const { data: round } = useGetRound(id)
  const { data: matches, isPending, dataUpdatedAt } = useGetRoundMatches(id)

  const secondsAgo = useSecondsAgo(dataUpdatedAt)

  if (isPending) return <LoadingIndicator />

  return (
    <div className="flex gap-4 flex-col">
      <h2 className="text-bold text-2xl">Matches</h2>
      <div className="flex flex-col gap-y-4">
        {round?.status !== RoundStatus.COMPLETED && (
          <span className="text-muted-foreground text-sm">Last refreshed {secondsAgo}s ago</span>
        )}
        {matches
          ?.sort((a, b) => a.id - b.id)
          .map((match) => (
            <MatchCard match={match} />
          ))}
      </div>
    </div>
  )
}
