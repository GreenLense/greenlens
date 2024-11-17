import './App.css'

// ----- Custom Components -----
import Hero from "./components/ui/hero"
// ----- Imported Components -----
import { Button } from './components/ui/button'
import Graphic from './components/ui/graphic'
import Statement from './components/ui/statement'
import ImageProvider from './components/ui/image-provider'
import { useRef } from 'react'
import {motion } from 'framer-motion'

function App() {
  const targetRef = useRef<HTMLDivElement | null>(null);

  const handleClick = () => {
    // Scroll to the target component
    if (targetRef.current) {
      targetRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div style={{ backgroundColor: '#19B84B', minHeight: '100vh' }}>
      <Hero />
      <motion.div
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1.15, delay: 1.75, ease: "easeInOut" }}
      >
        <Button onClick={handleClick} className='m-8 bg-white text-green-500 border border-green-500 hover:bg-green-200 focus:outline-none focus:ring-0 hover:border-green-500'>Get Started</Button>
        <Graphic />
        <Statement />
        <ImageProvider ref={targetRef} />

      </motion.div>
      
    </div>
  )
}

export default App
