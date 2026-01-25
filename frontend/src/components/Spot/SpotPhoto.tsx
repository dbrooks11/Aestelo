import { useRef, type JSX } from "react";



export default function SpotPhoto({spot, progress, setOpenRateSelector}): JSX.Element{

    const mediaList = [...spot.media].sort((a:{sort_order: number}, b:{sort_order: number}) => a.sort_order - b.sort_order)
    const lastTapRef = useRef<number>(0)

    return(
        <div className="relative aspect-4/5 object-cover flex flex-1 select-none">
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
                            setOpenRateSelector((prev: boolean) => !prev)
                        }
                        lastTapRef.current = time
                    }}
                    onDoubleClick={() => setOpenRateSelector((prev: boolean) => !prev)}
                    loading={index === progress - 1 ? "eager" : "lazy"} 
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