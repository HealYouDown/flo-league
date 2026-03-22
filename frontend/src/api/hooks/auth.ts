import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  loginMutation,
  logoutMutation,
  getMeOptions,
  getMeQueryKey,
} from "../generated/@tanstack/react-query.gen"

export function useLogin(options?: { onSuccess?: () => void }) {
  const queryClient = useQueryClient()

  return useMutation({
    ...loginMutation(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: getMeQueryKey() })
      options?.onSuccess?.()
    },
  })
}

export function useLogout() {
  const queryClient = useQueryClient()

  return useMutation({
    ...logoutMutation(),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: getMeQueryKey(),
      })
    },
  })
}

export function useCurrentUser() {
  return useQuery({
    ...getMeOptions(),
    retry: false, // don't spam retries on 401
    retryOnMount: false,
    refetchOnWindowFocus: false,
  })
}
