import type { Language } from "@/lib/language"
import { useState } from "react"

export function useLanguage(defaultLang: Language = "en") {
  const [lang, setLang] = useState<Language>(defaultLang)
  return { lang, setLang }
}
