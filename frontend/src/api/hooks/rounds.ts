import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  createRoundMutation,
  getRoundsQueryKey,
  getRoundsOptions,
  getRoundOptions,
  getRoundParticipantsOptions,
  addParticipantMutation,
  getRoundParticipantsQueryKey,
  removeParticipantMutation,
  getRoundQueryKey,
  updateRoundMutation,
  getRoundMatchesOptions,
  updateRoundMatchMutation,
  getRoundMatchesQueryKey,
} from "@/api/generated/@tanstack/react-query.gen"
import { RoundStatus } from "@/api/generated"

export function useCreateRound() {
  const queryClient = useQueryClient()

  return useMutation({
    ...createRoundMutation(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: getRoundsQueryKey() })
    },
  })
}

export function useGetRounds() {
  return useQuery(getRoundsOptions())
}

export function useGetActiveRounds() {
  return useQuery(
    getRoundsOptions({
      query: {
        status: [RoundStatus.DRAFT, RoundStatus.RUNNING],
      },
    }),
  )
}

export function useGetRound(round_id: number) {
  return useQuery({
    ...getRoundOptions({ path: { round_id } }),
    refetchInterval: 15_000,
  })
}

export function useGetRoundParticipants(round_id: number) {
  return useQuery({
    ...getRoundParticipantsOptions({ path: { round_id } }),
    refetchInterval: 10_000,
  })
}

export function useAddParticipant() {
  const queryClient = useQueryClient()

  return useMutation({
    ...addParticipantMutation(),
    onSuccess: (data, variables) => {
      const roundId = variables.path.round_id
      const key = getRoundParticipantsQueryKey({ path: { round_id: roundId } })
      queryClient.setQueryData(key, data)
    },
  })
}

export function useRemoveParticipant() {
  const queryClient = useQueryClient()

  return useMutation({
    ...removeParticipantMutation(),
    onSuccess: (data, variables) => {
      const roundId = variables.path.round_id
      const key = getRoundParticipantsQueryKey({ path: { round_id: roundId } })
      queryClient.setQueryData(key, data)
    },
  })
}

function useChangeRoundStatus(status: RoundStatus) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (variables: { round_id: number }, context) => {
      const mutationOptions = updateRoundMutation()
      if (!mutationOptions?.mutationFn) {
        throw new Error("mutationFn is undefined")
      }
      return mutationOptions.mutationFn!(
        {
          path: { round_id: variables.round_id },
          body: { status },
        },
        context,
      )
    },
    onSuccess: (_, variables) => {
      const roundId = variables.round_id
      queryClient.invalidateQueries({
        queryKey: getRoundQueryKey({ path: { round_id: roundId } }),
      })
    },
  })
}

export const useStartRound = () => useChangeRoundStatus(RoundStatus.RUNNING)
export const useFinishRound = () => useChangeRoundStatus(RoundStatus.COMPLETED)

export function useGetRoundMatches(round_id: number) {
  return useQuery({
    ...getRoundMatchesOptions({ path: { round_id } }),
    refetchInterval: 10_000,
  })
}

export function useUpdateRoundMatch() {
  const queryClient = useQueryClient()

  return useMutation({
    ...updateRoundMatchMutation(),
    onSuccess: (_, variables) => {
      const roundId = variables.path.round_id
      const key = getRoundMatchesQueryKey({ path: { round_id: roundId } })
      queryClient.invalidateQueries({ queryKey: key })
    },
  })
}
