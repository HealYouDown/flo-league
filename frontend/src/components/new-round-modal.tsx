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
import { useState } from "react"
import { useCreateRound } from "@/api/hooks/rounds"
import { RoundMode, type SeasonRead } from "@/api/generated"
import { useForm } from "@tanstack/react-form"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { ROUND_MODE_OPTIONS } from "@/lib/enums"

interface NewRoundModalProps {
  season: SeasonRead
}

interface FormValues {
  name: string
  mode: RoundMode
}

const defaultFormValues: FormValues = {
  name: "",
  mode: RoundMode.ONE_VS_ONE,
}

export function NewRoundModal({ season }: NewRoundModalProps) {
  const [open, setOpen] = useState(false)
  const { mutate, isPending } = useCreateRound()

  const form = useForm({
    defaultValues: defaultFormValues,
    onSubmit: ({ value }) => {
      mutate(
        { body: { season_id: season.id, name: value.name, mode: value.mode } },
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
        <Button variant="outline" size="sm">
          <PlusIcon />
          New Round
        </Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>New Round for {season.name}</DialogTitle>
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
              name="mode"
              children={(field) => {
                return (
                  <Field>
                    <FieldLabel htmlFor={field.name}>Modus</FieldLabel>
                    <Select
                      name={field.name}
                      value={field.state.value.toString()}
                      onValueChange={(value) => field.handleChange(Number(value) as RoundMode)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {ROUND_MODE_OPTIONS.map(({ value, label }) => (
                          <SelectItem key={value} value={value.toString()}>
                            {label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
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
