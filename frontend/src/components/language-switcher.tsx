import { Button } from "@/components/ui/button"
import type { Language } from "@/lib/language"

const flags: Record<Language, string> = {
  en: "🇬🇧", // or 🇺🇸
  de: "🇩🇪",
  es: "🇪🇸",
}

interface LanguageSwitcherProps {
  lang: Language
  setLang: (lang: Language) => void
}

export function LanguageSwitcher({ lang, setLang }: LanguageSwitcherProps) {
  return (
    <div className="flex gap-2 mb-4">
      {(["en", "de", "es"] as Language[]).map((code) => (
        <Button
          key={code}
          variant={lang === code ? "default" : "outline"}
          size="sm"
          onClick={() => setLang(code)}
        >
          <span className="mr-1">{flags[code]}</span>
          {code.toUpperCase()}
        </Button>
      ))}
    </div>
  )
}
