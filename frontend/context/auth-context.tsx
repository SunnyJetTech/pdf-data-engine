"use client"

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from "react"
import { CurrentUser } from "@/types/api.types"
import { getCurrentUser } from "@/api/auth.api"

interface AuthContextType {
  user: CurrentUser | null
  loading: boolean
  refreshUser: () => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext =
  createContext<AuthContextType | null>(null)

export function AuthProvider({
  children,
}: {
  children: React.ReactNode
}) {
  const [user, setUser] =
    useState<CurrentUser | null>(null)

  const [loading, setLoading] =
    useState(true)

  const refreshUser = useCallback(async () => {
    try {
      const response =
        await getCurrentUser()

      setUser(response.data)
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  function logout() {
    setUser(null)
  }

  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        refreshUser,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error(
      "useAuth must be used within AuthProvider"
    )
  }

  return context
}