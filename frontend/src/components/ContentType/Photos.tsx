import { ImageOff, Loader2 } from "lucide-react";
import { useMemo, useRef, useState, type JSX } from "react";



export default function Photos({media, progress, onClickFunctionality}): JSX.Element{

    const mediaList = useMemo(() => {
        return [...media].sort((a, b) => a.sort_order - b.sort_order);
    }, [media])
    const lastTapRef = useRef<number>(0)
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [onError, setOnError] = useState<boolean>(false)

    return(
        <div className="relative flex flex-1 justify-center items-center stroke-white object-cover aspect-4/5 text-accents-primary/80 select-none">
            {isLoading && <Loader2 className="animate-spin" size={34}/>}
            {onError && <ImageOff size={34}/>}
            {mediaList.map((item: {photo_path_url: string}, index: number) => {
                const shouldRender = Math.abs(index - (progress - 1)) <= 1
                
                if(!shouldRender) return null

                return (<img
                    key={index}
                    src={item.photo_path_url}
                    onTouchStart={() => {
                        const date = new Date()
                        const time = date.getTime()
                        const doubleTapDelay = 25
                        if (time - lastTapRef.current < doubleTapDelay) {
                            onClickFunctionality((prev: boolean) => !prev)
                        }
                        lastTapRef.current = time
                    }}
                    onDoubleClick={() => onClickFunctionality((prev: boolean) => !prev)}
                    loading={index === progress - 1 ? "eager" : "lazy"} 
                    onLoad={() => {
                        setOnError(false)
                        setIsLoading(false)
                    }}
                    onError={() => {
                        setIsLoading(false)
                        setOnError(true)
                    }}
                    className={`
                        absolute inset-0 w-full h-full object-cover
                        ${index === progress - 1 ? 'opacity-100 z-10' : 'opacity-0 z-0'}
                    `}
                    alt={`Spot content ${index + 1}`}
                ></img>)
            } )}
        </div>
    )
}