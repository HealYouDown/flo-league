import { Link } from "@tanstack/react-router"

export function Footer() {
  return (
    <footer className="border-t mt-10">
      <div className="container mx-auto flex flex-col md:flex-row items-center justify-between py-4 text-sm text-muted-foreground">
        <div className="flex gap-4 mt-2 md:mt-0">
          <Link to="/imprint" className="hover:text-foreground transition">
            Imprint
          </Link>
          <Link to="/privacy" className="hover:text-foreground transition">
            Privacy Policy
          </Link>
        </div>
      </div>
    </footer>
  )
}
