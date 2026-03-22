import type { CharacterClass } from "@/api/generated"

export const CHARACTER_CLASS_LABELS: Record<CharacterClass, string> = {
  0: "Mercenary",
  2: "Explorer",
  3: "Noble",
  4: "Saint",
  5: "Gladiator",
  6: "Guardian Swordsman",
  7: "Excavator",
  8: "Sniper",
  9: "Court Magician",
  10: "Magic Knight",
  11: "Priest",
  12: "Shaman",
}

export const CHARACTER_CLASS_OPTIONS = Object.entries(CHARACTER_CLASS_LABELS).map(
  ([value, label]) => ({
    value: Number(value) as CharacterClass,
    label,
  }),
)
