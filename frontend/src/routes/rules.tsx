import { useState } from "react"
import { PageLayout } from "@/components/page-layout"
import { createFileRoute } from "@tanstack/react-router"
import { LanguageSwitcher } from "@/components/language-switcher"
import type { Language } from "@/lib/language"
import { Highlight } from "@/components/highlight" // same Highlight wrapper as before

export const Route = createFileRoute("/rules")({
  component: RouteComponent,
})

type RulesContent = {
  title: string
  paragraphs: React.ReactNode[]
}

const content: Record<Language, RulesContent> = {
  en: {
    title: "Rules",
    paragraphs: [
      <>
        <Highlight>Consumable items</Highlight> (e.g. HP/MP potions, antidotes, etc.) are strictly
        prohibited.
      </>,
      <>Disconnecting during a fight will be counted as a loss.</>,
      <>Pets and tamed monsters are not allowed.</>,
      <>
        Only <Highlight>self-applied buffs</Highlight> are allowed. Buffs from pets, other players,
        or lord attendance are not allowed.
      </>,
      <>
        Intentionally running into spectator crowds to cause your opponent to lose target is
        prohibited.
      </>,
      <>
        Refusing to fight or deliberately trolling will result in{" "}
        <Highlight>immediate disqualification</Highlight> for the entire season.
      </>,
      <>
        Exploiting bugs (e.g. walking backwards or using Shift while affected by{" "}
        <Highlight>Thorn Trunk</Highlight>) is strictly prohibited and results in automatic loss.
      </>,
      <>
        Equipment trading is technically allowed; however, players are strongly encouraged to use
        their own equipment.
      </>,
      <>
        PvP matches lasting longer than <Highlight>5 minutes</Highlight> will be declared a draw.
      </>,
      <>
        If a player does not appear for their match, it will be counted as a win for the present
        player after maximum 2 minutes.
      </>,
      <>
        Failure to comply with any of these rules may result in disqualification for the day, the
        entire season, or permanent exclusion from future events. Trolling or deliberately
        disrupting the event may also result in sanctions affecting personal accounts. All cases are
        reviewed individually by the moderators, who reserve the right to make the final decision
        regarding penalties.
      </>,
    ],
  },

  de: {
    title: "Regeln",
    paragraphs: [
      <>
        Die Nutzung von <Highlight>Verbrauchsgegenständen</Highlight> (z. B. HP-/MP-Tränke,
        Gegengifte usw.) ist strengstens verboten.
      </>,
      <>Ein Verbindungsabbruch während eines Kampfes wird als Niederlage gewertet.</>,
      <>Pets und gezähmte Monster sind nicht erlaubt.</>,
      <>
        Es sind ausschließlich eigene <Highlight>Buffs</Highlight> erlaubt. Buffs von Pets, anderen
        Spielern oder der Lord-Buff sind nicht gestattet.
      </>,
      <>
        Das absichtliche Laufen in Zuschauergruppen, um den Gegner zum Verlust des Ziels zu bringen,
        ist verboten.
      </>,
      <>
        Die Verweigerung eines Kampfes oder absichtliches Trolling führt zur sofortigen{" "}
        <Highlight>Disqualifikation</Highlight> für die gesamte Saison.
      </>,
      <>
        Das Ausnutzen von Bugs (z. B. Rückwärtslaufen oder Nutzung der Shift-Taste während{" "}
        <Highlight>Thorn Trunk</Highlight> aktiv ist) ist strengstens verboten und führt zur
        automatischen Niederlage.
      </>,
      <>
        Das Tauschen von Ausrüstung ist technisch erlaubt; es wird jedoch ausdrücklich darum
        gebeten, mit eigener Ausrüstung zu spielen.
      </>,
      <>
        Kämpfe, die länger als <Highlight>5 Minuten</Highlight> dauern, werden als Unentschieden
        gewertet.
      </>,
      <>
        Erscheint ein Spieler nicht zum Match, wird der Kampf nach maximal 2 Minuten als Sieg für
        den anwesenden Spieler gewertet.
      </>,
      <>
        Verstöße gegen diese Regeln können zur Disqualifikation für den jeweiligen Tag, die gesamte
        Saison oder zum dauerhaften Ausschluss von zukünftigen Events führen. Trolling oder
        absichtliche Störung des Events kann sich ebenfalls auf persönliche Accounts auswirken. Die
        Moderatoren prüfen jeden Fall individuell und behalten sich das Recht vor, über
        entsprechende Strafen zu entscheiden.
      </>,
    ],
  },

  es: {
    title: "Reglas",
    paragraphs: [
      <>
        Está estrictamente prohibido el uso de <Highlight>objetos consumibles</Highlight> (por
        ejemplo, pociones de HP/MP, antídotos, etc.).
      </>,
      <>Desconectarse durante un combate se contará como derrota.</>,
      <>No se permiten mascotas ni monstruos domesticados.</>,
      <>
        Solo se permiten los <Highlight>buffs propios</Highlight>. No están permitidos buffs de
        mascotas, otros jugadores o asistencia del lord.
      </>,
      <>
        Está prohibido correr intencionadamente hacia el público para hacer que el oponente pierda
        el objetivo.
      </>,
      <>
        Negarse a luchar o hacer trolling deliberadamente resultará en{" "}
        <Highlight>descalificación inmediata</Highlight> para toda la temporada.
      </>,
      <>
        El abuso de bugs (por ejemplo, caminar hacia atrás o usar la tecla Shift mientras se está
        bajo el efecto de <Highlight>Thorn Trunk</Highlight>) está estrictamente prohibido y
        resultará en la pérdida automática del combate.
      </>,
      <>
        El intercambio de equipamiento está técnicamente permitido; sin embargo, se recomienda jugar
        con el propio equipamiento.
      </>,
      <>
        Los combates PvP que duren más de <Highlight>5 minutos</Highlight> se declararán empate.
      </>,
      <>
        Si un jugador no se presenta al combate, después de un máximo de 2 minutos se contará como
        victoria para el jugador presente.
      </>,
      <>
        El incumplimiento de estas reglas puede resultar en descalificación para el día, toda la
        temporada o exclusión permanente de futuros eventos. Hacer trolling o interrumpir
        deliberadamente el evento también puede acarrear sanciones a las cuentas personales. Todos
        los casos serán revisados individualmente por los moderadores, quienes se reservan el
        derecho de tomar la decisión final sobre las sanciones.
      </>,
    ],
  },
}

function RouteComponent() {
  const [lang, setLang] = useState<Language>("en")
  const current = content[lang]

  return (
    <PageLayout title="Rules">
      <LanguageSwitcher lang={lang} setLang={setLang} />

      <div className="max-w-2xl space-y-4">
        {current.paragraphs.map((text, index) => (
          <p key={index} className="text-muted-foreground leading-relaxed">
            {text}
          </p>
        ))}
      </div>
    </PageLayout>
  )
}
