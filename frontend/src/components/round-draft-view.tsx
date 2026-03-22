import { type PlayerRead } from "@/api/generated"
import { useCurrentUser } from "@/api/hooks/auth"
import {
  useGetRound,
  useGetRoundParticipants,
  useRemoveParticipant,
  useStartRound,
} from "@/api/hooks/rounds"
import { AddParticipantModal } from "@/components/add-participant-modal"
import { LoadingIndicator } from "@/components/loading-indicator"
import { PlayerIcon } from "@/components/player-icon"
import { Button } from "@/components/ui/button"
import { useSecondsAgo } from "@/hooks/seconds-ago"
import { TrashIcon } from "lucide-react"

import { toast } from "sonner"

interface DraftViewProps {
  id: number
}

export function DraftView({ id }: DraftViewProps) {
  const { data: round } = useGetRound(id)
  const { data: currentUser } = useCurrentUser()

  const { data: players, isPending: isPendingGetting, dataUpdatedAt } = useGetRoundParticipants(id)
  const { mutate: mutateRemoveParticipant, isPending: isRemoving } = useRemoveParticipant()
  const { mutate: startRound } = useStartRound()

  const secondsAgo = useSecondsAgo(dataUpdatedAt)

  const handleRemoveParticipant = (player: PlayerRead) => {
    if (!round) return
    mutateRemoveParticipant({ path: { round_id: round.id, player_id: player.id } })
    toast.success(`Player ${player.name} was removed`)
  }

  const handleStartMatches = () => {
    if (!round) return
    startRound({ round_id: round.id })
  }

  if (isPendingGetting) return <LoadingIndicator />

  return (
    <div className="flex gap-4 flex-col">
      <p className="text-muted-foreground">
        The round is currently being drafted. As soon as all players have joined, the moderators
        will start the round.
      </p>
      <div className="flex items-center gap-x-5 ">
        <h2 className="text-bold text-2xl">
          Current Participants {players && players.length > 0 && <span>({players.length})</span>}
        </h2>
        {round && currentUser && <AddParticipantModal round={round} />}
      </div>
      <div className="flex flex-col gap-4">
        <span className="text-muted-foreground text-sm">Last refreshed {secondsAgo}s ago</span>
        {!players ? (
          <span>Error loading participants</span>
        ) : players.length === 0 ? (
          <span>No participants have joined yet. Be the first!</span>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
            {players.map((player) => (
              <div
                key={player.id}
                className="flex flex-row border py-2 px-4 rounded-lg items-center"
              >
                <div>
                  <PlayerIcon player={player} />
                </div>
                <div className="flex flex-col ml-2">
                  <span className="font-semibold leading-none">{player.name}</span>
                  <span className="text-muted-foreground text-sm">
                    Lv {player.level_land} / {player.level_sea}
                  </span>
                </div>
                {currentUser && (
                  <>
                    <div className="flex-1"></div>
                    <div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleRemoveParticipant(player)}
                        disabled={isRemoving}
                      >
                        <TrashIcon />
                      </Button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
      {currentUser && (
        <div className="flex justify-end">
          <Button size="lg" onClick={handleStartMatches} variant="default">
            Start Matches
          </Button>
        </div>
      )}
    </div>
  )
}
