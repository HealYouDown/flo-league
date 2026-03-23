import { PageLayout } from "@/components/page-layout"
import { createFileRoute } from "@tanstack/react-router"
import type { Language, LanguageContent } from "@/lib/language"
import { useLanguage } from "@/hooks/use-language"
import { LanguageSwitcher } from "@/components/language-switcher"
import { Highlight } from "@/components/highlight"
import { useDocumentTitle } from "@uidotdev/usehooks"

export const Route = createFileRoute("/guide")({
  component: RouteComponent,
})

const githubLink = (
  <a
    href="https://github.com/HealYouDown/flo-league"
    target="_blank"
    rel="noreferrer"
    className="text-primary underline"
  >
    GitHub
  </a>
)
const content: Record<Language, LanguageContent> = {
  en: {
    title: "How it works",
    paragraphs: [
      <>
        To participate in the league, you need a character with at least{" "}
        <Highlight>Land Level 110</Highlight>.
      </>,
      <>
        To join, simply be present at <Highlight>Ron</Highlight> every Sunday at{" "}
        <Highlight>20:00 CEST</Highlight> on <Highlight>Server Flandria</Highlight>.
      </>,
      <>
        The PVP League staff will collect all participant names (you will most likely need to{" "}
        <span className="italic">whisper a specific word</span>) and enter them into the system. The
        system will then generate <Highlight>random matchups</Highlight>.
      </>,
      <>You can find more information about the matchmaking algorithm on {githubLink}.</>,
      <>
        When it is your turn to fight, the moderators will <Highlight>announce your name</Highlight>{" "}
        and you must step forward.
      </>,
      <>
        The league matches are conducted for <Highlight>one hour every Sunday</Highlight>.
      </>,
    ],
  },

  de: {
    title: "So funktioniert es",
    paragraphs: [
      <>
        Um an der Liga teilzunehmen, benötigst du einen Charakter mit mindestens{" "}
        <Highlight>Land Level 110</Highlight>.
      </>,
      <>
        Um teilzunehmen, musst du sonntags um <Highlight>20:00 Uhr (CEST)</Highlight> auf{" "}
        <Highlight>Ron</Highlight>, auf dem Server <Highlight>Flandria</Highlight>, anwesend sein.
      </>,
      <>
        Der PVP-League-Staff sammelt die Namen aller Teilnehmer (wahrscheinlich musst du ihnen ein
        bestimmtes Wort im <span className="italic">Whisper-Chat</span> schreiben) und trägt sie in
        das System ein. Anschließend generiert das System{" "}
        <Highlight>zufällige Begegnungen</Highlight>.
      </>,
      <>Weitere Informationen zum Matchmaking-Algorithmus findest du auf {githubLink}.</>,
      <>
        Wenn du an der Reihe bist, wird dein Name von den Moderatoren aufgerufen und du musst{" "}
        <Highlight>nach vorne treten</Highlight>.
      </>,
      <>
        Die Liga wird jeden Sonntag für <Highlight>eine Stunde</Highlight> durchgeführt.
      </>,
    ],
  },

  es: {
    title: "Cómo funciona",
    paragraphs: [
      <>
        Para participar en la liga, necesitas un personaje con al menos{" "}
        <Highlight>Land Level 110</Highlight>.
      </>,
      <>
        Para unirte, simplemente debes estar presente en <Highlight>Ron</Highlight> todos los
        domingos a las <Highlight>20:00 CEST</Highlight> en el servidor{" "}
        <Highlight>Flandria</Highlight>.
      </>,
      <>
        El equipo de la Liga PVP recopilará los nombres de todos los participantes (lo más probable
        es que tengas que <span className="italic">susurrarles una palabra específica</span>) y los
        ingresará en el sistema. El sistema generará{" "}
        <Highlight>enfrentamientos aleatorios</Highlight> automáticamente.
      </>,
      <>Puedes leer más sobre el algoritmo de emparejamiento en {githubLink}.</>,
      <>
        Cuando sea tu turno de pelear, los moderadores anunciarán tu nombre y deberás{" "}
        <Highlight>dar un paso al frente</Highlight>.
      </>,
      <>
        La liga se llevará a cabo durante <Highlight>una hora cada domingo</Highlight>.
      </>,
    ],
  },
}

function RouteComponent() {
  useDocumentTitle("Guide")
  const { lang, setLang } = useLanguage("en")
  const current = content[lang]

  return (
    <PageLayout title="Guide">
      <LanguageSwitcher lang={lang} setLang={setLang} />

      <div className="max-w-2xl space-y-4">
        <h2 className="text-xl font-semibold">{current.title}</h2>

        {current.paragraphs.map((text, index) => (
          <p key={index} className="text-muted-foreground leading-relaxed">
            {text}
          </p>
        ))}
      </div>
    </PageLayout>
  )
}
