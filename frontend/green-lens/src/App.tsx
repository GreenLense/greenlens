import './App.css'

// ----- Custom Components -----
import Hero from "./components/ui/hero"
// ----- Imported Components -----
import { Button } from './components/ui/button'
import Graphic from './components/ui/graphic'
import Statement from './components/ui/statement'
import ImageProvider from './components/ui/image-provider'
import { useRef } from 'react'

function App() {
  const targetRef = useRef<HTMLDivElement | null>(null);

  const handleClick = () => {
    // Scroll to the target component
    if (targetRef.current) {
      targetRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div>
      <Hero />
      <Button onClick={handleClick} className='m-8 bg-white text-green-500 border border-green-500 hover:bg-green-200 focus:outline-none focus:ring-0 hover:border-green-500'>Get Started</Button>
      <Graphic />
      <Statement />
      <ImageProvider ref={targetRef}/>
    </div>
  )
}

export default App
