import Container from "@/components/layout/container"

const features = [
  {
    title: "PDF Extraction",
    description:
      "Extract structured data from PDFs instantly.",
  },
  {
    title: "Smart Search",
    description:
      "Search documents like a database.",
  },
  {
    title: "CSV Export",
    description:
      "Export filtered results anytime.",
  },
  {
    title: "AI Analysis",
    description:
      "Generate insights automatically.",
  },
  {
    title: "Fast Processing",
    description:
      "Optimized for large documents.",
  },
  {
    title: "Role Management",
    description:
      "Admin and user permissions.",
  },
]

export default function Features() {
  return (
    <section className="py-24">
      <Container>
        <h2 className="text-4xl font-bold text-center mb-16">
          Features
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="border rounded-xl p-6 hover:shadow-lg transition"
            >
              <h3 className="font-semibold text-xl mb-2">
                {feature.title}
              </h3>

              <p className="text-muted-foreground">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  )
}