import Container from "@/components/layout/container"

export default function Footer() {
  return (
    <footer className="border-t py-12">
      <Container>
        <div className="flex flex-col md:flex-row justify-between">
          <div>
            <h3 className="font-bold text-xl">
              Tablify
            </h3>

            <p className="text-muted-foreground mt-2">
              Convert documents into searchable data.
            </p>
          </div>

          <div className="text-muted-foreground">
            &copy; 2025 - {new Date().getFullYear()} Tablify. All rights reserved.
          </div>
        </div>
      </Container>
    </footer>
  )
}