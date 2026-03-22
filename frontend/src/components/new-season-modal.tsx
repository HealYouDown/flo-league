import { Button } from "@/components/ui/button"
import { PlusIcon } from "lucide-react"

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { FieldGroup, Field, FieldLabel } from "@/components/ui/field"
import { useState } from "react"
import { useCreateSeason } from "@/api/hooks/seasons"
import { useForm } from "@tanstack/react-form"

export function NewSeasonModal() {
  const [open, setOpen] = useState(false)
  const { mutate, isPending } = useCreateSeason()

  const form = useForm({
    defaultValues: {
      name: "",
      description: "",
    },
    onSubmit: ({ value }) => {
      mutate(
        {
          body: { name: value.name, description: value.description },
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

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">
          <PlusIcon />
          New Season
        </Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>New Season</DialogTitle>
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

          <DialogFooter>
            <Field orientation="horizontal">
              <Button type="submit" disabled={isPending}>
                {isPending ? "Creating..." : "Create"}
              </Button>
            </Field>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
