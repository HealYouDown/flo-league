import { PageLayout } from "@/components/page-layout"
import { createFileRoute } from "@tanstack/react-router"
import { useDocumentTitle } from "@uidotdev/usehooks"

export const Route = createFileRoute("/imprint")({
  component: RouteComponent,
})

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <h2 className="text-lg font-semibold">{title}</h2>
      <div className="text-sm text-muted-foreground leading-relaxed">{children}</div>
    </div>
  )
}

function RouteComponent() {
  useDocumentTitle("Imprint")

  return (
    <PageLayout title="Imprint">
      <div className="max-w-3xl space-y-6">
        <Section title="Company">
          <p>
            <span className="font-medium">Giiku Games GmbH</span> is a company incorporated under
            German law.
          </p>
        </Section>

        <Section title="Address">
          <p>
            Giiku Games GmbH
            <br />
            Rehleitenweg 32b
            <br />
            83026 Rosenheim
            <br />
            Germany
          </p>
        </Section>

        <Section title="Corporate Information">
          <p>
            Managing Director: Achim Kaspers
            <br />
            Court of registry: District Court of Traunstein
            <br />
            Trade register number: HRB 27763
            <br />
            VAT-ID: DE323063583
            <br />
            Phone: +49 (0) 8031 / 22273 20
            <br />
            E-Mail:{" "}
            <a href="mailto:info@giikugames.com" className="text-primary underline">
              info@giikugames.com
            </a>
          </p>
        </Section>

        <Section title="Youth Protection">
          <p>
            Commissioner for Youth Protection: Maximilian Gramstat
            <br />
            E-Mail:{" "}
            <a href="mailto:datenschutz@giikugames.com" className="text-primary underline">
              datenschutz@giikugames.com
            </a>
          </p>
        </Section>

        <Section title="Disclaimer">
          <p>
            Although every effort is made to present current and accurate information, we cannot
            assume responsibility for information from external links. The author of each web page
            is solely responsible for the content of that page.
          </p>
        </Section>

        <Section title="Content">
          <p>
            The author reserves the right not to be responsible for the topicality, correctness,
            completeness or quality of the information provided. Liability claims regarding damage
            caused by the use of any information provided, including any kind of information which
            is incomplete or incorrect, will therefore be rejected.
          </p>
          <p>
            All offers are non-binding and without obligation. Parts of the pages or the complete
            publication including all offers and information might be extended, changed or partly or
            completely deleted by the author without separate announcement.
          </p>
        </Section>

        <Section title="Referrals and Links">
          <p>
            The author is not responsible for any contents linked or referred to from his pages
            unless he has full knowledge of illegal contents and would be able to prevent the
            visitors of his site from viewing those pages.
          </p>
        </Section>

        <Section title="Copyright">
          <p>
            The author intended not to use any copyrighted material for the publication or, if not
            possible, to indicate the copyright of the respective object.
          </p>
          <p>
            Any duplication or use of objects such as diagrams, sounds or texts in other electronic
            or printed publications is not permitted without the author's agreement.
          </p>
        </Section>

        <Section title="Privacy Policy">
          <p>
            If the opportunity for the input of personal or business data (email addresses, name,
            addresses) is given, the input of these data takes place voluntarily.
          </p>
        </Section>

        <Section title="Legal Validity">
          <p>
            This disclaimer is to be regarded as part of the internet publication which you were
            referred from. If sections or individual terms are not legal or correct, the content or
            validity of the other parts remain unaffected.
          </p>
        </Section>

        <div className="pt-4 border-t text-xs text-muted-foreground">
          © 2019–2026 Giiku Games GmbH — All rights reserved.
        </div>
      </div>
    </PageLayout>
  )
}
