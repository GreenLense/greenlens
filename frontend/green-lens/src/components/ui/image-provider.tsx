import { Button } from "./button";
import { Card, CardContent, CardHeader, CardTitle } from "./card";

import exampleOutput from "../../assets/example-output.png"

import { forwardRef, useRef, useState } from "react"

const ImageProvider = forwardRef<HTMLDivElement, React.ComponentPropsWithoutRef<"div">>((props, ref) => {
    const fileInputRef = useRef<HTMLInputElement | null>(null)
    const [imageUrl, setImageUrl] = useState<string | null>(null);

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
                    if (file) {
                        const url = URL.createObjectURL(file);
                        setImageUrl(url); 
                    }
                }}
            />

            {imageUrl && (
                <div className="mt-4">
                    <img src={imageUrl} alt="Uploaded" className="max-w-full h-72 mb-6 mx-auto" />
                </div>
            )}

            <Card className="m-auto w-6/12">
                <CardHeader>
                    <CardTitle>Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                    The object in your image is plastic!
                </CardContent>
            </Card>
        </div>
    )
})

export default ImageProvider