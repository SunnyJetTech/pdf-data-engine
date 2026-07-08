import Hero from "@/components/landing/hero"
import Features from "@/components/landing/features"
import Pricing from "@/components/landing/pricing"
import Testimonials from "@/components/landing/testimonials"
import Faq from "@/components/landing/faq"
import Footer from "@/components/landing/footer"
import Navbar from "@/components/landing/navbar" 

export default function HomePage() {
  return (
    <>
      <Navbar />
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <Faq />
      <Footer />
    </>
  )
}