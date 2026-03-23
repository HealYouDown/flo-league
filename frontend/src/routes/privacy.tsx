import { PageLayout } from "@/components/page-layout"
import { createFileRoute } from "@tanstack/react-router"
import { useDocumentTitle } from "@uidotdev/usehooks"

export const Route = createFileRoute("/privacy")({
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

function SubSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1">
      <h3 className="font-medium">{title}</h3>
      <div>{children}</div>
    </div>
  )
}

function RouteComponent() {
  useDocumentTitle("Privacy Policy")

  return (
    <PageLayout title="Privacy Policy">
      <div className="max-w-3xl space-y-8">
        {/* I. General */}
        <div className="space-y-4">
          <h1 className="text-xl font-bold">I. General Information</h1>

          <Section title="1. Responsible Body & Data Protection Officer">
            <p>
              Below we explain which personal data is collected and processed when using our
              services.
            </p>
            <p className="mt-2">
              <span className="font-medium">GIIKU GAMES GmbH</span>
              <br />
              Rehleitenweg 32b
              <br />
              83026 Rosenheim
              <br />
              Germany
              <br />
              Tel: +49 8031 210 205 70
              <br />
              E-Mail:{" "}
              <a href="mailto:datenschutz@giikugames.com" className="text-primary underline">
                datenschutz@giikugames.com
              </a>
            </p>
          </Section>

          <Section title="2. Legal Basis">
            <p>
              Processing is based on the General Data Protection Regulation (GDPR), effective May
              25, 2018.
            </p>

            <ul className="list-disc ml-5 mt-2 space-y-1">
              <li>
                <strong>Consent (Art. 6(1)(a) GDPR):</strong> Voluntary and informed consent to data
                processing.
              </li>
              <li>
                <strong>Contract (Art. 6(1)(b) GDPR):</strong> Necessary for fulfilling contractual
                obligations.
              </li>
              <li>
                <strong>Legal obligation (Art. 6(1)(c) GDPR):</strong> Required by law.
              </li>
              <li>
                <strong>Legitimate interest (Art. 6(1)(f) GDPR):</strong> Required for our
                legitimate interests unless overridden.
              </li>
            </ul>
          </Section>

          <Section title="3. Rights of the Data Subject">
            <ul className="list-disc ml-5 space-y-1">
              <li>Right of access (Art. 15 GDPR)</li>
              <li>Right to rectification (Art. 16 GDPR)</li>
              <li>Right to erasure (Art. 17 GDPR)</li>
              <li>Right to restriction (Art. 18 GDPR)</li>
              <li>Right to data portability (Art. 20 GDPR)</li>
              <li>Right to object (Art. 21 GDPR)</li>
            </ul>

            <p className="mt-2">
              You also have the right to lodge a complaint with a supervisory authority.
            </p>
          </Section>

          <Section title="4. Data Erasure and Storage Duration">
            <p>
              Personal data is deleted or blocked as soon as the purpose of storage ceases to apply.
              Storage may continue if required by EU or national regulations.
            </p>
          </Section>
        </div>

        {/* II. Data Processing */}
        <div className="space-y-4">
          <h1 className="text-xl font-bold">II. Concrete Data Processing</h1>

          <Section title="1. Data Collection When Visiting the Website">
            <SubSection title="a) Scope of Processing">
              <ul className="list-disc ml-5 space-y-1">
                <li>Browser type and version</li>
                <li>Operating system</li>
                <li>Internet service provider</li>
                <li>IP address</li>
                <li>Date and time of access</li>
                <li>Referrer websites</li>
                <li>Visited pages</li>
              </ul>

              <p className="mt-2">
                This data is stored in log files and processed by our hosting provider within the
                EU.
              </p>
            </SubSection>

            <SubSection title="b) Legal Basis">
              <p>Processing is based on Art. 6(1)(f) GDPR (legitimate interest).</p>
            </SubSection>

            <SubSection title="c) Purpose">
              <p>
                Data processing ensures website functionality, security, and optimization. No
                marketing evaluation takes place.
              </p>
            </SubSection>

            <SubSection title="d) Storage Duration">
              <p>
                Log files are deleted after 30 days unless required for specific purposes. IPs may
                be anonymized.
              </p>
            </SubSection>

            <SubSection title="e) Objection">
              <p>
                Collection and storage are essential for operation, therefore no objection is
                possible.
              </p>
            </SubSection>
          </Section>
        </div>
      </div>
    </PageLayout>
  )
}
