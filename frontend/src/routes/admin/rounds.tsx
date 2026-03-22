import { useGetRounds } from "@/api/hooks/rounds"
import { PageLayout } from "@/components/page-layout"
import { Button } from "@/components/ui/button"
import { Item, ItemActions, ItemContent, ItemDescription, ItemTitle } from "@/components/ui/item"
import { ROUND_MODE_LABELS, ROUND_STATUS_LABELS } from "@/lib/enums"
import { createFileRoute, Link } from "@tanstack/react-router"
import { useMemo } from "react"

export const Route = createFileRoute("/admin/rounds")({
  component: RouteComponent,
})

function RouteComponent() {
  const { data: rounds, isPending } = useGetRounds()

  const sortedRounds = useMemo(() => {
    if (!rounds) return []
    return [...rounds].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )
  }, [rounds])

  return (
    <PageLayout title="Manage Rounds">
      {isPending && <p>Loading...</p>}
      {sortedRounds.length == 0 && <p>No rounds found</p>}
      {sortedRounds.map((round) => {
        return (
          <Item key={round.id} variant="muted">
            <ItemContent>
              <ItemTitle>
                {round.season && <>{round.season.name} - </>}
                {round.name}
              </ItemTitle>
              <ItemDescription>
                {ROUND_STATUS_LABELS[round.status]} • {ROUND_MODE_LABELS[round.mode]}
              </ItemDescription>
              <ItemDescription>
                Created at: {new Date(round.created_at).toLocaleString()}
              </ItemDescription>
            </ItemContent>
            <ItemActions>
              <Button size="sm" asChild>
                <Link to="/rounds/$id" params={{ id: round.id }}>
                  View
                </Link>
              </Button>
            </ItemActions>
          </Item>
        )
      })}
    </PageLayout>
  )
}
