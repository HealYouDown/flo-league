import { useCurrentUser, useLogout } from "@/api/hooks/auth"
import { createRootRoute, Link, Outlet } from "@tanstack/react-router"

import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu"

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { Toaster } from "@/components/ui/sonner"
import { Footer } from "@/components/footers"

const RootLayout = () => {
  const { data: currentUser } = useCurrentUser()
  const { mutate: logout } = useLogout()

  const isLoggedIn = currentUser?.id !== undefined

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b bg-background">
        <div className="container mx-auto flex h-14 items-center justify-between px-4">
          {/* Left side */}
          <div className="flex items-center gap-6">
            <Link to="/">
              <img src="/logo_medium.png" alt="Logo" className="h-12 w-auto object-contain" />{" "}
            </Link>

            <NavigationMenu>
              <NavigationMenuList>
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <Link to="/rules" className="[&.active]:font-semibold">
                      Rules
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>

                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <Link to="/guide" className="[&.active]:font-semibold">
                      Guide
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              </NavigationMenuList>
            </NavigationMenu>
          </div>

          {/* Right side */}
          <div className="flex items-center gap-4">
            {isLoggedIn && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm">
                    Manage
                  </Button>
                </DropdownMenuTrigger>

                <DropdownMenuContent align="end">
                  <DropdownMenuItem asChild>
                    <p className="text-xs text-muted-foreground">Account: {currentUser.username}</p>
                  </DropdownMenuItem>

                  <DropdownMenuSeparator />

                  <DropdownMenuItem asChild>
                    <Link to="/admin/seasons">Seasons</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link to="/admin/rounds">Rounds</Link>
                  </DropdownMenuItem>
                  {currentUser.is_admin && (
                    <DropdownMenuItem>
                      <Link to="/admin/update-players">Update Players</Link>
                    </DropdownMenuItem>
                  )}

                  <DropdownMenuSeparator />

                  <DropdownMenuItem onClick={() => logout({})} className="cursor-pointer">
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>
      <Toaster position="top-right" />

      <Footer />
    </div>
  )
}

export const Route = createRootRoute({ component: RootLayout })
