import { defineConfig } from "@hey-api/openapi-ts"

export default defineConfig({
  input: "http://localhost:8080/openapi.json",
  output: "src/api/generated",
  plugins: ["@tanstack/react-query", { enums: "javascript", name: "@hey-api/typescript" }],
})
