import { type JSX } from "react";
import { Lock } from "lucide-react";


export default function CollectionCard({collection, setViewCollection, viewCollection}): JSX.Element{

    const count: number = collection.preview_thumbnails && collection.preview_thumbnails.length

    const sizePhotosToGrid = (index: number) =>{
        if (count === 1) return "col-span-2 row-span-2"
        if (count === 2) return "row-span-2"
        if (count === 3 && index === 0) return "row-span-2"
        return "col-span-1 row-span-1"
    }

    return(
        <>
            <div 
                className={`${(!count || count === 0) && 'bg-accents-deep/90 dark:bg-accents-deep/80'} rounded-xs grid grid-cols-2 grid-rows-2 relative overflow-hidden aspect-square shrink-0 hover:scale-101 transition-all cursor-pointer`}
                onClick={() => setViewCollection(collection.id)}
            >
                {collection.preview_thumbnails && collection.preview_thumbnails.map((photo: string, index: number) => {
                    return (
                        <img
                            key={index}
                            src={photo}
                            className={`w-full h-full object-cover pointer-events-none select-none ${sizePhotosToGrid(index)}`}
                        >
                        </img>
                    )
                })}
                <div className="bottom-0 absolute flex flex-col gap-2 bg-linear-to-t from-black/80 to-transparent p-4 pt-20 w-full text-white text-xs md:text-base">
                    <div className="flex justify-between items-center">
                        <span
                            className="font-bold text-[1em] truncate"
                        >
                            {collection.name}
                        </span>
                        {!collection.is_public && 
                        <Lock 
                            size={14}
                            className="shrink-0"
                        />}
                    </div>
                    <p className="text-neutral-200 dark:text-neutral-300 text-[0.75em] line-clamp-2">{collection.description}</p>
                </div>
            </div>
        </>
    )
}