import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { useUpdateSeason, useDeleteSeason } from "@/api/hooks/seasons"
import { type SeasonRead } from "@/api/generated/types.gen"
import { useForm } from "@tanstack/react-form"
import { FieldGroup, Field, FieldLabel } from "@/components/ui/field"
import { useCurrentUser } from "@/api/hooks/auth"
import { Edit2Icon } from "lucide-react"

interface EditSeasonModalProps {
  season: SeasonRead
}

export function EditSeasonModal({ season }: EditSeasonModalProps) {
  const { data: currentUser } = useCurrentUser()
  const [open, setOpen] = useState(false)
  const { mutate: updateMutate, isPending: isUpdating } = useUpdateSeason()
  const { mutate: deleteMutate, isPending: isDeleting } = useDeleteSeason()

  const form = useForm({
    defaultValues: {
      name: season.name,
      description: season.description,
      isRunning: season.is_running,
    },
    onSubmit: ({ value }) => {
      updateMutate(
        {
          path: { id: season.id },
          body: { name: value.name, description: value.description, is_running: value.isRunning },
        },
        {
          onSuccess: () => {
            form.reset()
            setOpen(false)
          },
        },
      )
    },
  })

  function handleDelete() {
    if (!confirm("Are you sure you want to delete this season?")) return
    if (!confirm("100% sure?")) return

    deleteMutate(
      { path: { id: season.id } },
      {
        onSuccess: () => setOpen(false),
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Edit2Icon />
          Edit
        </Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Season</DialogTitle>
        </DialogHeader>

        <form
          className="space-y-3"
          onSubmit={(e) => {
            e.preventDefault()
            form.handleSubmit()
          }}
        >
          <FieldGroup>
            <form.Field
              name="name"
              children={(field) => {
                return (
                  <Field>
                    <FieldLabel htmlFor={field.name}>Name</FieldLabel>
                    <Input
                      id={field.name}
                      name={field.name}
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      onChange={(e) => field.handleChange(e.target.value)}
                      autoComplete="off"
                    />
                  </Field>
                )
              }}
            />
          </FieldGroup>

          <FieldGroup>
            <form.Field
              name="description"
              children={(field) => {
                return (
                  <Field>
                    <FieldLabel htmlFor={field.name}>Description</FieldLabel>
                    <Input
                      id={field.name}
                      name={field.name}
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      onChange={(e) => field.handleChange(e.target.value)}
                      autoComplete="off"
                    />
                  </Field>
                )
              }}
            />
          </FieldGroup>

          <FieldGroup>
            <form.Field
              name="isRunning"
              children={(field) => {
                return (
                  <Field orientation="horizontal">
                    <Checkbox
                      id={field.name}
                      name={field.name}
                      checked={field.state.value}
                      onBlur={field.handleBlur}
                      onCheckedChange={(val) => field.handleChange(!!val)}
                    />
                    <FieldLabel htmlFor={field.name}>Active?</FieldLabel>
                  </Field>
                )
              }}
            />
          </FieldGroup>
          <DialogFooter>
            <Field orientation="horizontal">
              <Button type="submit" disabled={isUpdating}>
                {isUpdating ? "Saving..." : "Save"}
              </Button>
              {currentUser?.is_admin && (
                <Button
                  type="button"
                  variant="destructive"
                  onClick={handleDelete}
                  disabled={isDeleting || isUpdating}
                >
                  {isDeleting ? "Deleting..." : "Delete"}
                </Button>
              )}
            </Field>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
