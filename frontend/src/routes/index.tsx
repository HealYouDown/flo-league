import { useGetActiveRounds } from "@/api/hooks/rounds"
import { useGetSeasons } from "@/api/hooks/seasons"
import { LoadingIndicator } from "@/components/loading-indicator"
import { PageLayout } from "@/components/page-layout"
import { Item, ItemActions, ItemContent, ItemDescription, ItemTitle } from "@/components/ui/item"
import { ROUND_MODE_LABELS, ROUND_STATUS_LABELS } from "@/lib/enums"
import { createFileRoute, Link } from "@tanstack/react-router"
import { useDocumentTitle } from "@uidotdev/usehooks"
import { ChevronRightIcon } from "lucide-react"
import { useMemo } from "react"

export const Route = createFileRoute("/")({
  component: RouteComponent,
})

function ActiveRounds() {
  const { data: activeRounds } = useGetActiveRounds()
  if (!activeRounds || activeRounds.length == 0) return null

  return (
    <div className="mb-6">
      <h2 className="text-2xl font-semibold mb-3">Active Rounds</h2>

      <div className="flex flex-col gap-3">
        {activeRounds.map((round) => (
          <Link key={round.id} to="/rounds/$id" params={{ id: round.id }} className="group">
            <div className="flex items-center justify-between p-4 rounded-lg border bg-primary/5 border-primary/20 hover:bg-primary/10 transition">
              <div className="flex items-center gap-3">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500" />
                </span>

                <div className="flex flex-col">
                  <span className="font-semibold text-primary">
                    {round.season === null ? "" : `${round.season.name} -`} {round.name}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    {ROUND_STATUS_LABELS[round.status]} • {ROUND_MODE_LABELS[round.mode]}
                  </span>
                </div>
              </div>
              <ChevronRightIcon className="size-5 text-primary transition group-hover:translate-x-1" />
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

function RouteComponent() {
  useDocumentTitle("Flo League")

  const { data: seasons, isPending } = useGetSeasons()

  const { activeSeasons, finishedSeasons } = useMemo(() => {
    if (!seasons) return { activeSeasons: [], finishedSeasons: [] }

    const sorted = [...seasons].sort(
      (a, b) =>
        new Date(b.created_at as string).getTime() - new Date(a.created_at as string).getTime(),
    )

    const activeSeasons = sorted.filter((s) => s.is_running)
    const finishedSeasons = sorted.filter((s) => !s.is_running)

    return { activeSeasons, finishedSeasons }
  }, [seasons])

  return (
    <PageLayout>
      <ActiveRounds />
      <div className="flex flex-col gap-4">
        <h2 className="text-2xl font-semibold">Running Seasons</h2>
        {isPending && <LoadingIndicator />}
        {activeSeasons.map((season) => (
          <Item key={season.id} variant="muted" asChild>
            <Link to="/seasons/$id" params={{ id: season.id }}>
              <ItemContent>
                <ItemTitle>{season.name}</ItemTitle>
                <ItemDescription>{season.description}</ItemDescription>
              </ItemContent>
              <ItemActions>
                <ChevronRightIcon className="size-4" />
              </ItemActions>
            </Link>
          </Item>
        ))}
      </div>
      <div className="flex flex-col gap-4">
        <h2 className="text-2xl font-semibold">Past Seasons</h2>
        {isPending && <LoadingIndicator />}
        {finishedSeasons.length === 0 && <p>There are no past seasons yet.</p>}
        {finishedSeasons.map((season) => (
          <Item key={season.id} variant="outline" asChild>
            <Link to="/seasons/$id" params={{ id: season.id }}>
              <ItemContent>
                <ItemTitle>{season.name}</ItemTitle>
                <ItemDescription>{season.description}</ItemDescription>
              </ItemContent>
              <ItemActions>
                <ChevronRightIcon className="size-4" />
              </ItemActions>
            </Link>
          </Item>
        ))}
      </div>
    </PageLayout>
  )
}
