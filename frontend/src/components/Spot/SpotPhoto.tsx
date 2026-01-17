import { type JSX } from "react";



export default function SpotPhoto({spot, progress}): JSX.Element{
    const mediaList = spot.spot_media.sort((a:{sort_order: number}, b:{sort_order: number}) => a.sort_order - b.sort_order)


    return(
        <div className="relative aspect-4/5 object-cover flex flex-1">
            {mediaList.map((item: {photo_path_url: string}, index: number) => {
                const shouldRender = Math.abs(index - (progress - 1)) <= 1
                
                if(!shouldRender) return null

                return (<img
                    key={index}
                    src={item.photo_path_url}
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