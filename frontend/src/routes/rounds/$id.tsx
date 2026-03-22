import { RoundStatus } from "@/api/generated"
import { useGetRound } from "@/api/hooks/rounds"
import { DraftView } from "@/components/round-draft-view"
import { LoadingIndicator } from "@/components/loading-indicator"
import { PageLayout } from "@/components/page-layout"
import { createFileRoute } from "@tanstack/react-router"
import { RoundMatchesView } from "@/components/round-matches-view"

export const Route = createFileRoute("/rounds/$id")({
  component: RouteComponent,
  params: {
    parse: ({ id }) => ({
      id: Number(id),
    }),
  },
})

const roundStatusContent = {
  [RoundStatus.DRAFT]: DraftView,
  [RoundStatus.RUNNING]: RoundMatchesView,
  [RoundStatus.COMPLETED]: RoundMatchesView, // It just shows matches + result anyways
} satisfies Record<RoundStatus, React.ComponentType<{ id: number }>>

function RouteComponent() {
  const { id } = Route.useParams()
  const { data: round, isPending } = useGetRound(id)

  if (isPending || !round) return <LoadingIndicator />

  const Content = roundStatusContent[round.status]

  return (
    <PageLayout title={`${round.season?.name + " - "} ${round.name}`}>
      <Content id={id} />
    </PageLayout>
  )
}
