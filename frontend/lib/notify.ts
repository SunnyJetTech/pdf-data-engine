import { toast } from "sonner"
import { getErrorMessage } from "@/lib/utils/errorHandler"

export const notify = {
  success: (msg: string) => toast.success(msg),
  error: (err: unknown) =>
    toast.error(getErrorMessage(err)),
  info: (msg: string) => toast.info(msg),
}