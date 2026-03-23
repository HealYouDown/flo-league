import { useGetLeaderboard, useGetSeason, useGetSeasonRounds } from "@/api/hooks/seasons"
import { LoadingIndicator } from "@/components/loading-indicator"
import { PageLayout } from "@/components/page-layout"
import { PlayerIcon } from "@/components/player-icon"
import { Item, ItemActions, ItemContent, ItemDescription, ItemTitle } from "@/components/ui/item"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ROUND_MODE_LABELS, ROUND_STATUS_LABELS } from "@/lib/enums"
import { createFileRoute, Link } from "@tanstack/react-router"
import { useDocumentTitle } from "@uidotdev/usehooks"
import { ChevronRightIcon, Crown, Medal, SwordsIcon, TrophyIcon } from "lucide-react"
import { useMemo } from "react"

export const Route = createFileRoute("/seasons/$id")({
  component: RouteComponent,
  params: {
    parse: ({ id }) => ({
      id: Number(id),
    }),
  },
})

interface TabProps {
  seasonId: number
}

function getRankStyle(rank: number) {
  switch (rank) {
    case 1:
      return "bg-yellow-500/10 border border-yellow-500/20"
    case 2:
      return "bg-gray-400/10 border border-gray-400/20"
    case 3:
      return "bg-amber-600/10 border border-amber-600/20"
    default:
      return "bg-muted/40"
  }
}

function RankIcon({ rank }: { rank: number }) {
  if (rank === 1) return <Crown className="w-5 h-5 text-yellow-500" />
  if (rank <= 3) return <Medal className="w-5 h-5 text-muted-foreground" />
  return <span className="text-sm font-semibold w-5 text-center">{rank}</span>
}

function Leaderboard({ seasonId }: TabProps) {
  const { data: leaderboard, isPending } = useGetLeaderboard(seasonId)
  const sortedLeaderboard = useMemo(() => {
    if (!leaderboard) return []
    return [...leaderboard].sort((a, b) => b.elo - a.elo)
  }, [leaderboard])

  if (isPending) return <LoadingIndicator />
  if (sortedLeaderboard.length === 0) return <p>No data available.</p>

  return (
    <div className="flex flex-col gap-2">
      {sortedLeaderboard.map((playerStats, index) => {
        const rank = index + 1

        return (
          <div
            key={playerStats.player.id}
            className={`flex items-center justify-between p-3 rounded-md ${getRankStyle(rank)}`}
          >
            <div className="flex items-center gap-3">
              <div className="w-6 flex justify-center">
                <RankIcon rank={rank} />
              </div>

              <PlayerIcon player={playerStats.player} />

              <div className="flex flex-col">
                <span className="font-semibold leading-none">{playerStats.player.name}</span>
                <span className="text-xs text-muted-foreground">
                  Lv {playerStats.player.level_land} / {playerStats.player.level_sea}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-4 text-sm">
              <span className="font-semibold">{playerStats.elo}</span>

              <span className="text-green-500">{playerStats.wins}W</span>
              <span className="text-red-500">{playerStats.losses}L</span>
              <span className="text-muted-foreground">{playerStats.draws}D</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function Rounds({ seasonId }: TabProps) {
  const { data: rounds, isPending } = useGetSeasonRounds(seasonId)

  const sortedRounds = useMemo(() => {
    if (!rounds) return []
    return [...rounds].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )
  }, [rounds])

  if (isPending) return <LoadingIndicator />
  if (sortedRounds.length === 0) return <p>No rounds found.</p>

  return (
    <div className="flex flex-col gap-y-4 py-2">
      {sortedRounds.map((round) => (
        <Item key={round.id} variant="outline" asChild>
          <Link to="/rounds/$id" params={{ id: round.id }}>
            <ItemContent>
              <ItemTitle>{round.name}</ItemTitle>
              <ItemDescription>
                {ROUND_STATUS_LABELS[round.status]} • {ROUND_MODE_LABELS[round.mode]}
              </ItemDescription>
              <ItemDescription>{new Date(round.created_at).toLocaleString()}</ItemDescription>
            </ItemContent>
            <ItemActions>
              <ChevronRightIcon className="size-4" />
            </ItemActions>
          </Link>
        </Item>
      ))}
    </div>
  )
}

function RouteComponent() {
  const { id: seasonId } = Route.useParams()
  const { data: season, isPending } = useGetSeason(seasonId)
  useDocumentTitle(season?.name || "")

  if (isPending) return <LoadingIndicator />
  if (!season) return <p>An error occured.</p>

  return (
    <PageLayout title={season.name}>
      <p className="text-muted-foreground text-sm">{season.description}</p>
      <Tabs defaultValue="leaderboard">
        <TabsList variant="line">
          <TabsTrigger value="leaderboard">
            <TrophyIcon /> Ranking
          </TabsTrigger>
          <TabsTrigger value="rounds">
            <SwordsIcon />
            Rounds
          </TabsTrigger>
        </TabsList>
        <TabsContent value="leaderboard" asChild>
          <Leaderboard seasonId={season.id} />
        </TabsContent>
        <TabsContent value="rounds" asChild>
          <Rounds seasonId={season.id} />
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
