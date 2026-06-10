import { useState } from "react";
import { getErrorMessage } from "@/lib/utils/errorHandler";

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function execute<T>(
    callback: () => Promise<T>
  ): Promise<T | null> {
    try {
      setLoading(true);
      setError(null);

      return await callback();
    } catch (err) {
      const message = getErrorMessage(err);

      setError(message);

      return null;
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    error,
    execute,
  };
}