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
    <div style={{ backgroundColor: '#19B84B', minHeight: '100vh' }} className="overflow-hidden">
      <Hero />
      <motion.div
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.75 , delay: 1.5, ease: "easeInOut" }}
      >
        <Button onClick={handleClick} className='m-8 bg-white text-green-500 border border-green-500 hover:bg-green-200 focus:outline-none focus:ring-0 hover:border-green-500'>Get Started</Button>
      </motion.div>

      <motion.div
        className="my-component"
        initial={{ opacity: 0, x: "-10vw" }} 
        whileInView={{ opacity: 1, x: 0 }} 
        viewport={{ once: true }}
        transition={{ duration: 0.75 , delay:0.25, ease: "circOut" }} 
      >
        <Graphic />

      </motion.div>

      <motion.div
        className="my-component"
        initial={{ opacity: 0, x: "10vw" }} // Start off-screen to the right
        whileInView={{ opacity: 1, x: 0 }} 
        viewport={{ once: true }}
        transition={{ duration: 0.75 , delay: 0.25, ease: "circOut" }} 
      >
        <Statement />
      </motion.div>

      <motion.div
        className="my-component"
        initial={{ opacity: 0, x: "-10vw" }} 
        whileInView={{ opacity: 1, x: 0 }} 
        viewport={{ once: true }}
        transition={{ duration: 0.75 , delay: 0.25, ease: "circOut" }} 
      >
        <ImageProvider ref={targetRef} />
      </motion.div>
      
    </div>
  )
}

export default App
