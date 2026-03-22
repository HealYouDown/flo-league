import { MatchResult, type MatchParticipant, type MatchRead } from "@/api/generated"
import { useCurrentUser } from "@/api/hooks/auth"
import { useUpdateRoundMatch } from "@/api/hooks/rounds"
import { ConfirmDialog } from "@/components/confirm-dialog"
import { PlayerIcon } from "@/components/player-icon"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import { CrownIcon, SwordsIcon } from "lucide-react"

interface TeamColumnProps {
  players: MatchParticipant[]
}

function EloChange({
  elo_before,
  elo_change,
}: {
  elo_before: number | null
  elo_change: number | null
}) {
  if (elo_before === null || elo_change === null) return

  const prefix = elo_change > 0 ? "+" : elo_change === 0 ? "±" : null
  const className = elo_change < 0 ? "text-red-500" : elo_change > 0 ? "text-green-500" : null

  const deltaSpan = (
    <span className={cn("text-muted-foreground", className)}>
      {prefix}
      {elo_change}
    </span>
  )

  return (
    <span className="text-sm">
      {elo_before} → {elo_before + elo_change} ({deltaSpan})
    </span>
  )
}

function TeamColumn({ players }: TeamColumnProps) {
  return (
    <div className="flex flex-col gap-2">
      {players.map((player) => (
        <div key={player.player_id} className="flex items-center gap-2 px-3 py-2">
          <PlayerIcon player={player} />
          <div className="flex flex-col">
            <span className="font-semibold leading-none">{player.name}</span>
            <span className="text-muted-foreground text-sm">
              Lv {player.level_land} / {player.level_sea}
            </span>
            {player.elo_change !== null && (
              <EloChange elo_before={player.elo_before} elo_change={player.elo_change} />
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

interface MatchCardProps {
  match: MatchRead
}

export function MatchCard({ match }: MatchCardProps) {
  const { data: currentUser } = useCurrentUser()
  const { mutate, isPending } = useUpdateRoundMatch()

  const setMatchResult = (result: MatchResult) => {
    mutate({
      path: { round_id: match.round_id, match_id: match.id },
      body: {
        result: result,
      },
    })
  }

  return (
    <div className="border-b">
      <div className="p-4">
        <div
          className="
            grid gap-4 items-center
            grid-cols-1
            md:grid-cols-[1fr_auto_1fr]
          "
        >
          {/* Team 1 */}
          <div className="flex justify-center md:justify-end">
            <div
              className={cn(
                "flex flex-row justify-center items-center",
                match.match_result === MatchResult.WIN_TEAM_2 ? "opacity-50" : null,
              )}
            >
              {match.match_result === MatchResult.WIN_TEAM_1 && (
                <CrownIcon className="w-5 h-5 text-yellow-500" />
              )}
              <TeamColumn players={match.team_1.members} />
            </div>
          </div>

          {/* VS */}
          <div className="flex flex-col items-center justify-center gap-y-1">
            {match.match_result !== MatchResult.DRAW &&
              match.match_result !== MatchResult.CANCELED && (
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-muted">
                  <SwordsIcon className="w-5 h-5 text-primary" />
                </div>
              )}
            {match.match_result === MatchResult.DRAW && <Badge variant="outline">Draw</Badge>}
            {match.match_result === MatchResult.CANCELED && (
              <Badge variant="destructive">Canceled</Badge>
            )}
          </div>

          {/* Team 2 */}
          <div className="flex justify-center md:justify-start">
            <div
              className={cn(
                "flex flex-row justify-center items-center",
                match.match_result === MatchResult.WIN_TEAM_1 ? "opacity-50" : null,
              )}
            >
              {match.match_result === MatchResult.WIN_TEAM_2 && (
                <CrownIcon className="w-5 h-5 text-yellow-500" />
              )}
              <TeamColumn players={match.team_2.members} />
            </div>
          </div>
        </div>
      </div>
      {currentUser && match.match_result === MatchResult.UNSET && (
        <div className="flex flex-col md:flex-row gap-4 items-center justify-center p-3">
          <Tooltip>
            <TooltipTrigger asChild>
              <ConfirmDialog
                title="Winner Team 1"
                description="This will set the match result to 'Winner Team 1'. This action cannot be undone. Are you sure?"
                onConfirm={() => setMatchResult(MatchResult.WIN_TEAM_1)}
              >
                <Button disabled={isPending}>Winner Team 1</Button>
              </ConfirmDialog>
            </TooltipTrigger>
            <TooltipContent className="flex flex-col">
              {match.team_1.members.map((player) => (
                <span key={player.player_id} className="text-sm">
                  {player.name}
                </span>
              ))}
            </TooltipContent>
          </Tooltip>

          <Tooltip>
            <TooltipTrigger asChild>
              <ConfirmDialog
                title="Winner Team 2"
                description="This will set the match result to 'Winner Team 2'. This action cannot be undone. Are you sure?"
                onConfirm={() => setMatchResult(MatchResult.WIN_TEAM_2)}
              >
                <Button disabled={isPending}>Winner Team 2</Button>
              </ConfirmDialog>
            </TooltipTrigger>
            <TooltipContent className="flex flex-col">
              {match.team_2.members.map((player) => (
                <span key={player.player_id} className="text-sm">
                  {player.name}
                </span>
              ))}
            </TooltipContent>
          </Tooltip>

          <ConfirmDialog
            title="Draw"
            description="This will set the match result to 'Draw'. This action cannot be undone. Are you sure?"
            onConfirm={() => setMatchResult(MatchResult.DRAW)}
          >
            <Button disabled={isPending} variant="outline">
              Draw
            </Button>
          </ConfirmDialog>

          <ConfirmDialog
            title="Cancel Match"
            description="This will set the match result to 'Canceled'. This action cannot be undone. Are you sure?"
            onConfirm={() => setMatchResult(MatchResult.DRAW)}
          >
            <Button disabled={isPending} variant="destructive">
              Cancel Match
            </Button>
          </ConfirmDialog>
        </div>
      )}
    </div>
  )
}
