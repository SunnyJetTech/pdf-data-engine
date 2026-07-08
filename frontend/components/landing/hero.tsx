import Link from "next/link"
import { Button } from "@/components/ui/button"
import Container from "@/components/layout/container"

export default function Hero() {
  return (
    <section className="py-28">
      <Container>
        <div className="max-w-4xl mx-auto text-center">
          <span className="inline-block px-4 py-2 rounded-full bg-primary/10 text-primary mb-6">
            AI-Powered Data Extraction
          </span>

          <h1 className="text-5xl md:text-7xl font-bold leading-tight">
            Turn Documents Into
            <span className="text-primary">
              {" "}Searchable Data
            </span>
          </h1>

          <p className="mt-8 text-xl text-muted-foreground">
            Upload PDFs, Excel sheets and CSV files.
            Search, filter, export and manage your data
            instantly from one dashboard.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <Link href="/register">
              <Button size="lg">
                Start Free
              </Button>
            </Link>

            <Link href="/pricing">
              <Button
                variant="outline"
                size="lg"
              >
                View Pricing
              </Button>
            </Link>
          </div>
        </div>
      </Container>
    </section>
  )
}