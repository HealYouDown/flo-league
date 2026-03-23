import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { useUpdatePlayers } from "@/api/hooks/players"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { toast } from "sonner"
import { useDocumentTitle } from "@uidotdev/usehooks"

export const Route = createFileRoute("/admin/update-players")({
  component: RouteComponent,
})

function RouteComponent() {
  useDocumentTitle("Manage Players")
  const { mutate, isPending } = useUpdatePlayers()
  const [file, setFile] = useState<File | null>(null)

  const handleSubmit = (e: React.SubmitEvent) => {
    e.preventDefault()
    if (!file) return

    mutate(
      { body: { file } },
      {
        onSuccess: () => {
          setFile(null)
          toast.success("Players updated successfully!")
        },
        onError: () => {
          toast.error("Failed to update players. Check the CSV file.")
        },
      },
    )
  }

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Update Players</h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />

        {file && <p className="text-sm text-muted-foreground">Selected file: {file.name}</p>}

        <Button type="submit" disabled={!file || isPending}>
          {isPending ? "Uploading..." : "Upload CSV"}
        </Button>
      </form>
    </div>
  )
}
