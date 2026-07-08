export default function Pricing() {
  return (
    <section className="py-20">
      <h2 className="text-3xl font-bold text-center mb-10">
        Pricing
      </h2>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="border p-6 rounded">
          <h3>Free</h3>
          <p>20MB</p>
        </div>

        <div className="border-2 border-primary shadow-xl">
          <h3>Pro</h3>
          <p>500MB</p>
        </div>

        <div className="border p-6 rounded">
          <h3>Enterprise</h3>
          <p>Unlimited</p>
        </div>
      </div>
    </section>
  )
}