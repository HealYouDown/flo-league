import { Button } from "@/components/ui/button"
import { PlusCircleIcon } from "lucide-react"

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { useAddParticipant } from "@/api/hooks/rounds"
import { useSearchPlayers } from "@/api/hooks/players"
import { LoadingIndicator } from "@/components/loading-indicator"
import { type PlayerRead, type RoundRead } from "@/api/generated"
import { useDebounce } from "@uidotdev/usehooks"
import { toast } from "sonner"
import { PlayerIcon } from "@/components/player-icon"

interface AddParticipantModalProps {
  round: RoundRead
}

export function AddParticipantModal({ round }: AddParticipantModalProps) {
  const [open, setOpen] = useState(false)

  const { mutate, isPending: isAdding } = useAddParticipant()

  const [searchTerm, setSearchTerm] = useState("")
  const debouncedSearch = useDebounce(searchTerm, 300)

  const { data: players, isPending: isSearching, isEnabled } = useSearchPlayers(debouncedSearch)

  const handleAddPlayer = (player: PlayerRead) => {
    mutate(
      {
        path: { round_id: round.id, player_id: player.id },
      },
      {
        onSuccess: () => {
          setSearchTerm("")
          toast.success(`Player ${player.name} added`)
        },
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <PlusCircleIcon />
          Add Participants
        </Button>
      </DialogTrigger>

      <DialogContent className="max-w-fit">
        <DialogHeader>
          <DialogTitle>Add Participants</DialogTitle>
        </DialogHeader>

        <Input
          placeholder="Search players..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          autoComplete="off"
        />

        {isEnabled && (
          <div className="mt-4 max-h-60 overflow-y-auto">
            {isSearching ? (
              <LoadingIndicator />
            ) : players?.length === 0 ? (
              <p className="text-sm text-muted-foreground">No players found</p>
            ) : (
              <div className="space-y-1 flex flex-col">
                {players?.map((player) => (
                  <Button
                    asChild
                    onClick={() => handleAddPlayer(player)}
                    disabled={isAdding}
                    variant="outline"
                    className="justify-start py-6"
                  >
                    <div className="flex flex-row">
                      <div>
                        <PlayerIcon player={player} />
                      </div>
                      <div className="flex flex-col">
                        <span className="font-semibold leading-none">{player.name}</span>
                        <span className="text-muted-foreground text-sm">
                          Lv {player.level_land} / {player.level_sea}
                        </span>
                      </div>
                    </div>
                  </Button>
                ))}
              </div>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
