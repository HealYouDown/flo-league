import { type MatchParticipant, type PlayerRead, CharacterClass } from "@/api/generated"
import { cn } from "@/lib/utils"

interface PlayerIconProps {
  className?: string
  player: PlayerRead | MatchParticipant
}

const CLASS_TO_ICON = {
  [CharacterClass.EXPLORER]: "explorer.png",
  [CharacterClass.EXCAVATOR]: "excavator.png",
  [CharacterClass.SNIPER]: "sniper.png",
  [CharacterClass.NOBLE]: "noble.png",
  [CharacterClass.COURT_MAGICIAN]: "court_magician.png",
  [CharacterClass.MAGIC_KNIGHT]: "magic_knight.png",
  [CharacterClass.SAINT]: "saint.png",
  [CharacterClass.SHAMAN]: "shaman.png",
  [CharacterClass.PRIEST]: "priest.png",
  [CharacterClass.MERCENARY]: "mercenary.png",
  [CharacterClass.GLADIATOR]: "gladiator.png",
  [CharacterClass.GUARDIAN_SWORDSMAN]: "guardian_swordsman.png",
}

export function PlayerIcon({ player, className }: PlayerIconProps) {
  const iconName = CLASS_TO_ICON[player.character_class]
  const iconPath = `/class-icons/${player.is_female ? "female" : "male"}/${iconName}`
  return (
    <img className={cn("size-8 border border-gray-400 rounded-full", className)} src={iconPath} />
  )
}
