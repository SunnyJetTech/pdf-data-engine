import Link from "next/link";

export default function AuthLinks({
  type,
}: {
  type: "login" | "register" | "forgot";
}) {
  return (
    <div className="flex justify-between text-sm mt-4">
      {type !== "login" && (
        <Link href="/login" className="text-blue-500">
          Login
        </Link>
      )}

      {type !== "register" && (
        <Link href="/register" className="text-blue-500">
          Register
        </Link>
      )}

      {type !== "forgot" && (
        <Link href="/forgot-password" className="text-blue-500">
          Forgot password?
        </Link>
      )}
    </div>
  );
}