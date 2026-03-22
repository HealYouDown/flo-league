import {
  searchPlayersOptions,
  updatePlayersMutation,
} from "@/api/generated/@tanstack/react-query.gen"
import { useMutation, useQuery } from "@tanstack/react-query"

export function useSearchPlayers(name: string) {
  return useQuery({
    ...searchPlayersOptions({ query: { name } }),
    enabled: name.length >= 2,
  })
}

export function useUpdatePlayers() {
  return useMutation(updatePlayersMutation())
}
