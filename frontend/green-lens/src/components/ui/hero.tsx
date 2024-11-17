import background from '../../assets/imgs/Background.png';
import { LeftHill } from '../animations/left_hill.tsx';
import { RightHill } from '../animations/right_hill.tsx';
import { Mountains } from '../animations/mountains.tsx';
import { LeftForeground } from '../animations/left_foreground.tsx';
import { Sun } from '../animations/sun.tsx';
import { Cloud } from '../animations/cloud.tsx';
import { LogoText } from '../animations/logo_text.tsx';
import { Grass } from '../animations/grass.tsx';
import { Bird } from '../animations/bird.tsx';

import {motion} from 'framer-motion';

export default function Hero() {
    return (
        <div className="relative overflow-hidden">
            <img src={background} alt="Background" className="w-screen" />
            <motion.div
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.75, ease: "easeOut" }}
                className="absolute top-0 left-0 z-10"
            >
                <Mountains />
            </motion.div>

            <motion.div
                initial={{ x: -450 }}
                animate={{ x: 0}}
                transition={{ duration: 1.25, delay: 0.25 , ease: "easeOut"}}
                className="absolute top-0 left-0 z-20"
            >
                <LeftHill />
            </motion.div>

            <motion.div
                initial={{ x: 450, }}
                animate={{ x: 0,}}
                transition={{ duration: 1.25, delay: 0.25, ease: "easeOut" }}
                className="absolute  top-0 left-0 z-20"
            >
                <RightHill />
            </motion.div>

            <motion.div
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 1, delay: 1, ease: "easeOut" }}
                className="absolute top-0 left-0 z-30"
            >
                <LeftForeground />
            </motion.div>

            <motion.div
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.75, delay:1, ease: "easeOut" }}
                className="absolute top-0 left-0 z-40"
            >
                <Grass/>
            </motion.div>





            <motion.div
                initial={{ x: 100, y: 150, opacity: 0 }}
                animate={{ x: 0, y: 0, opacity: 1 }}
                transition={{ duration: 1.5, delay: 0.75, ease: "easeInOut" }}
                className="absolute top-10 right-0 z-9"
            >
                <motion.div
                    className="relative" style={{
                        display: "flex", // Ensure the image is centered
                        justifyContent: "center",
                    }}

                    animate={{
                        rotate: [0, 360], 
                    }}
                    transition={{
                        duration: 60, 
                        repeat: Infinity, 
                        ease: "linear", 
                    }}
                    
                >
                    <Sun />
                </motion.div>
            </motion.div>

            <motion.div
                animate={{
                    x: ["-17vw", "100vw"],
                }}
                transition={{
                    duration: 60, 
                    repeat: Infinity, 
                    ease: "linear", 
                }}
                className="absolute top-40 left-0 z-40"
            >
                <Cloud />
            </motion.div>
            <motion.div
                animate={{
                    x: ["100vw", "-20vw"],  // Start at the far right (100vw) and move to the far left (-20vw)
                    y: ["0vh", "-30vh"],    // Move up and down
                }}
                transition={{
                    duration: 25,
                    repeat: Infinity,  // Repeat the animation infinitely
                    ease: "linear",     // Continuous smooth movement
                }}
                className="absolute top-80 left-0 z-50"
            >
                <Bird />
            </motion.div>

            <motion.div
                className="absolute top-0 left-0 z-40 flex justify-center items-center w-full h-screen"
                initial={{ opacity: 0, y:-100 }} 
                animate={{ opacity: 1, y:-100 }}  
                transition={{
                    duration: 1.25,  
                    delay: 1,    
                    ease: "easeIn"
                }}
            >
                <LogoText />
            </motion.div>

            
        </div>
    )
}