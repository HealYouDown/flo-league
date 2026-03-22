import { useGetSeasons } from "@/api/hooks/seasons"
import { EditSeasonModal } from "@/components/edit-season-modal"
import { NewRoundModal } from "@/components/new-round-modal"
import { NewSeasonModal } from "@/components/new-season-modal"
import { PageLayout } from "@/components/page-layout"
import { Item, ItemActions, ItemContent, ItemDescription, ItemTitle } from "@/components/ui/item"
import { createFileRoute } from "@tanstack/react-router"
import { useMemo } from "react"

export const Route = createFileRoute("/admin/seasons")({
  component: RouteComponent,
})

function RouteComponent() {
  const { data: seasons, isPending } = useGetSeasons()

  const sortedSeasons = useMemo(() => {
    if (!seasons) return []
    return [...seasons].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )
  }, [seasons])

  return (
    <PageLayout title="Manage Seasons">
      <div>
        <NewSeasonModal />
      </div>
      <hr />
      {isPending && <p>Loading...</p>}
      {sortedSeasons.length == 0 && <p>No seasons found</p>}
      {sortedSeasons.map((season) => {
        return (
          <Item key={season.id} variant="muted">
            <ItemContent>
              <ItemTitle>{season.name}</ItemTitle>
              <ItemDescription>{season.description}</ItemDescription>
              <ItemDescription>
                {season.is_running ? (
                  <span className="text-green-600">Active</span>
                ) : (
                  <span>Finished</span>
                )}
              </ItemDescription>
              <ItemDescription>
                Created at: {new Date(season.created_at).toLocaleString()}
              </ItemDescription>
            </ItemContent>
            <ItemActions>
              <NewRoundModal season={season} />
              <EditSeasonModal season={season} />
            </ItemActions>
          </Item>
        )
      })}
    </PageLayout>
  )
}
