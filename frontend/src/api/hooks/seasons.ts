import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  createSeasonMutation,
  getSeasonOptions,
  getSeasonsOptions,
  getSeasonQueryKey,
  getSeasonsQueryKey,
  patchSeasonMutation,
  deleteSeasonMutation,
  getSeasonRoundsOptions,
  getSeasonLeaderboardOptions,
} from "@/api/generated/@tanstack/react-query.gen"

export function useCreateSeason() {
  const queryClient = useQueryClient()

  return useMutation({
    ...createSeasonMutation(),
    onSuccess: (data) => {
      queryClient.setQueryData(getSeasonQueryKey({ path: { id: data.id } }), data)
      queryClient.invalidateQueries({ queryKey: getSeasonsQueryKey() })
    },
  })
}

export function useDeleteSeason() {
  const queryClient = useQueryClient()

  return useMutation({
    ...deleteSeasonMutation(),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: getSeasonQueryKey({ path: { id: variables.path.id } }),
      })
      queryClient.invalidateQueries({ queryKey: getSeasonsQueryKey() })
    },
  })
}

export function useUpdateSeason() {
  const queryClient = useQueryClient()

  return useMutation({
    ...patchSeasonMutation(),
    onSuccess: (data) => {
      queryClient.setQueryData(getSeasonQueryKey({ path: { id: data.id } }), data)
      queryClient.invalidateQueries({ queryKey: getSeasonsQueryKey() })
    },
  })
}

export function useGetSeasons() {
  return useQuery(getSeasonsOptions())
}

export function useGetSeason(id: number) {
  return useQuery(
    getSeasonOptions({
      path: { id },
    }),
  )
}

export function useGetSeasonRounds(id: number) {
  return useQuery(
    getSeasonRoundsOptions({
      path: { id },
    }),
  )
}

export function useGetLeaderboard(id: number) {
  return useQuery(
    getSeasonLeaderboardOptions({
      path: { id },
    }),
  )
}
