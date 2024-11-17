import { Button } from "./button";
import { Card, CardContent, CardHeader, CardTitle } from "./card";

import exampleOutput from "../../assets/example-output.png"

import { forwardRef, useRef } from "react"

const ImageProvider = forwardRef<HTMLDivElement, React.ComponentPropsWithoutRef<"div">>((props, ref) => {
    const fileInputRef = useRef<HTMLInputElement | null>(null)

    const handleClick = () => {
        fileInputRef.current?.click()
    }

    return (
        <div ref={ref} {...props} className="mb-4">
            <Button onClick={handleClick} className='m-8 bg-white text-green-500 border border-green-500 hover:bg-green-200 focus:outline-none focus:ring-0 hover:border-green-500'>Upload</Button>
            <input 
                ref={fileInputRef} 
                type="file" 
                className="hidden" 
                onChange={(e) => {
                    const file = e.target.files?.[0];
                    console.log(file); // Handle the file selection here
                }}
            />

            <Card className="m-auto w-6/12">
                <CardHeader>
                    <CardTitle>Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                    <img src={exampleOutput} alt="Example of computer vision recognizing material classification" />
                </CardContent>
            </Card>
        </div>
    )
})

export default ImageProvider