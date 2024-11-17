import './App.css'

// ----- Custom Components -----
import Hero from "./components/ui/hero"
// ----- Imported Components -----
import { Button } from './components/ui/button'
import Graphic from './components/ui/graphic'
import Statement from './components/ui/statement'
import ImageProvider from './components/ui/image-provider'
import Footer from './components/ui/footer'

function App() {
  return (
    <div>
      <Hero />
      <Button className='m-4'>Get Started</Button>
      <Graphic />
      <Statement />
      <ImageProvider />
      <Footer />
    </div>
  )
}

export default App
