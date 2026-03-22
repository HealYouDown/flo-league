import { StrictMode } from "react"
import { createRoot } from "react-dom/client"

import "./index.css"
import { MutationCache, QueryCache, QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { client } from "@/api/generated/client.gen.ts"
import { routeTree } from "./routeTree.gen"
import { RouterProvider, createRouter } from "@tanstack/react-router"
import { toast } from "sonner"
import { TooltipProvider } from "@/components/ui/tooltip"
const router = createRouter({ routeTree })

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60000,
    },
  },
  queryCache: new QueryCache({
    onError: (error, query) => {
      console.error(error)

      // @ts-expect-error queryKey is typed as unknown[] but we know the shape
      const queryId = query.queryKey?.[0]?._id
      // Ignores errors on the "getMe" API calls
      if (queryId === "getMe") return

      // Force invalidates all queries, which will update the UI with the latest data
      queryClient.invalidateQueries()

      toast.error("Something went wrong: " + error)
    },
  }),
  mutationCache: new MutationCache({
    onError: (error) => {
      console.error(error)

      // Force invalidates all queries, which will update the UI with the latest data
      queryClient.invalidateQueries()

      toast.error("Something went wrong: " + error)
    },
  }),
})

client.setConfig({
  baseUrl: import.meta.env.VITE_API_URL,
  credentials: "include",
})

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <RouterProvider router={router} />
      </TooltipProvider>
    </QueryClientProvider>
  </StrictMode>,
)
