import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-6">
      <h1 className="text-5xl font-bold">
        404
      </h1>

      <p>Page not found</p>

      <Link href="/">
        <Button>
          Go Home
        </Button>
      </Link>
    </div>
  );
}