import axios from "axios";

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const response = error.response;

    if (!response) {
      return "Unable to connect to server";
    }

    if (response.data?.message) {
      return response.data.message;
    }

    if (
      response.data?.detail &&
      Array.isArray(response.data.detail)
    ) {
      return response.data.detail[0]?.msg ?? "Validation error";
    }

    switch (response.status) {
      case 401:
        return "Session expired";

      case 403:
        return "Access denied";

      case 404:
        return "Resource not found";

      case 500:
        return "Server error";

      default:
        return "Something went wrong";
    }
  }

  return "Unexpected error occurred";
}