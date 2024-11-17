"use client"

import { TrendingUp } from "lucide-react"
import { CartesianGrid, Line, LineChart, XAxis } from "recharts"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

export default function Graphic() {
    const chartData = [
        { decade: "1960", waste: 88.1, recycle: 5.6},
        { decade: "1970", waste: 121.1, recycle: 8},
        { decade: "1980", waste: 151.6, recycle: 14.5},
        { decade: "1990", waste: 208.3, recycle: 33.2},
        { decade: "2000", waste: 243.5, recycle: 69.5},
        { decade: "2010", waste: 251.1, recycle: 85.4},
        { decade: "2018", waste: 292.4, recycle: 93.9},
    ]

    const chartConfig = {
        totalWaste: {
          label: "Waste",
          color: "#2563eb",
        },
        totalRecycle: {
            label: "Recycled",
            color: "#60a5fa",
        }
      } satisfies ChartConfig
      

    return (
        <div>
            <Card className="w-8/12 m-auto">
                <iframe id="iframe" title='Tonnes of waste dumped' src='https://www.theworldcounts.com/embeds/counters/104?background_color=white&color=black&font_family=%22Helvetica+Neue%22%2C+Arial%2C+sans-serif&font_size=14' className="border-none h-24 w-96 m-auto text-3xl"></iframe>
            </Card>
            <Card className="mt-8  mx-auto w-7/12">
                <CardHeader>
                    <CardTitle>MSW (Municipal Solid Waste) Generation vs. Recycling Rates</CardTitle>
                    <CardDescription>(million tons)</CardDescription>
                </CardHeader>
                <CardContent>
                    <ChartContainer config={chartConfig}>
                        <LineChart accessibilityLayer data={chartData} margin={{left: 12, right: 12,}}>
                            <CartesianGrid vertical={false} />
                            <XAxis dataKey="decade" axisLine={false}/>
                            <Line 
                                dataKey="waste" 
                                type="monotone"
                                stroke="red"
                                strokeWidth={2}
                                name="Waste: "
                            />
                            <Line 
                                dataKey="recycle"
                                type="monotone"
                                stroke="green"
                                strokeWidth={2}
                                name="Recycled: "
                            />
                            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
                        </LineChart>
                    </ChartContainer>
                </CardContent>
                <CardFooter>
                    <div className="flex w-full items-start gap-2 text-sm">
                        <div className="grid gap-2">
                            <div className="flex items-center gap-2 font-medium leading-none">
                                On average, MSW generation has increased by 22.75% per decade<TrendingUp className="h-4 w-4" />
                            </div>
                        </div>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}