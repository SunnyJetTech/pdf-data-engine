"use client"

import { useEffect } from "react"
import { AxiosError } from "axios"

export function useApiError(
  error: unknown
) {
  useEffect(() => {
    if (!error) return

    const err =
      error as AxiosError<any>

    const message =
      err?.response?.data?.message ||
      "Unexpected error"

    console.error("API ERROR:", message)

  }, [error])
}