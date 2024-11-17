import { Button } from "./button";
import { Card, CardContent, CardHeader, CardTitle } from "./card";

import { forwardRef, useRef, useState } from "react"

const ImageProvider = forwardRef<HTMLDivElement, React.ComponentPropsWithoutRef<"div">>((props, ref) => {
    const fileInputRef = useRef<HTMLInputElement | null>(null)
    const [imageUrl, setImageUrl] = useState<string | null>(null);
    const [result, setResult] = useState<string | null>(null);

    const handleClick = () => {
        fileInputRef.current?.click()
    }

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
          const url = URL.createObjectURL(file);
          setImageUrl(url); // Display the image preview

          console.log(file)
    
          // Create a FormData instance to send the file
          const formData = new FormData();
          formData.append('file', file);

          console.log(formData)
    
          try {
            const response = await fetch('http://localhost:5001/upload', { // Ensure the URL points to the correct backend
              method: 'POST',
              body: formData,
            });
    
            if (!response.ok) {
              throw new Error('File upload failed');
            }
    
            const data = await response.json();
            console.log('File uploaded successfully:', data);
            console.log("Response from backend: ", data.message)
            setResult(data.message)
          } catch (error) {
            console.error('Error uploading file:', error);
          }
        }
      };

    return (
        <div ref={ref} {...props} className="mb-4">
            <Button onClick={handleClick} className='m-8 bg-white text-green-500 border border-green-500 hover:bg-green-200 focus:outline-none focus:ring-0 hover:border-green-500'>Upload</Button>
            <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileUpload}
            />

            {imageUrl && (
                <Card className="mx-auto w-4/12 mb-4">
                    <div className="mt-4">
                        <img src={imageUrl} alt="Uploaded" className="max-w-full h-72 mb-6 mx-auto" />
                    </div>      
                </Card>
            )}

            <Card className="mx-auto w-6/12">
                <CardHeader>
                    <CardTitle>Analysis</CardTitle>
                </CardHeader>
                {
                    result && <CardContent>
                        The object in your image is {result}!
                    </CardContent>
 
                }
                {
                    !result && <CardContent>
                        Waiting...
                    </CardContent>
                }
            </Card>
        </div>
    )
})

export default ImageProvider