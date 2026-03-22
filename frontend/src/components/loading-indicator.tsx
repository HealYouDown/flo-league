import { Spinner } from "@/components/ui/spinner"

export function LoadingIndicator() {
  return (
    <div className="flex items-center gap-2">
      <Spinner />
    </div>
  )
}
