import { useEffect, useRef, type JSX } from "react";
import ScrollContainer from "react-indiana-drag-scroll";



export default function SpotTags({tags}: {tags: Array<string>}): JSX.Element{

    const scrollRef = useRef<HTMLElement>(null)

    useEffect(() => {
    const element: HTMLElement | null = scrollRef.current
    if (!element) return

    const handleWheel = (e: WheelEvent): void => {
      if (e.deltaY !== 0) {
        e.preventDefault()
        
        element.scrollLeft += e.deltaY
      }
    };
    element.addEventListener('wheel', handleWheel, { passive: false })
    return () => element.removeEventListener('wheel', handleWheel)
    }, [])

    const handleTags = (tags: Array<string>): JSX.Element | undefined => {
        if(tags.length > 0){
            return(
                <ScrollContainer 
                    className="flex flex-col justify-center gap-1 mask-x-from-90% mask-x-to-100% w-full h-full overflow-x-scroll no-scrollbar mx-2"
                    innerRef={scrollRef}
                    >
                    <ul 
                        className="flex justify-start items-center gap-2 mx-2"
                        aria-label="Hashtags scrollable list"
                        tabIndex={0}
                        role="region"
                        >

                        {tags.map((tag)=> {
                            // TODO: make hashtags clickable
                            return(
                                <li 
                                    key={tag} 
                                    className='flex justify-center items-center dark:bg-neutral-700 px-1.5 py-0.5 border dark:border-white/5 rounded-md min-w-8 hover:text-accents-primary whitespace-nowrap hover:cursor-pointer shrink-0 drop-shadow-sm'
                                    aria-label={`Hashtag ${tag}`}
                                    >
                                        #{tag}
                                </li>
                            )
                        })}
                    </ul>
                </ScrollContainer>
            )
        }else{
            return (
                <span 
                    className="flex items-center ml-4 dark:text-neutral-600 text-black/40 italic gap-1 pointer-events-none"
                >
                    <span className="w-1.5 h-1.5 rounded-full dark:bg-neutral-700 bg-black/40"></span>
                    No hashtags
                </span>
                )
        }
    }
    
    return(
        <div className="flex w-full h-10 text-[10px] text-white dark:bg-slate/50 bg-stone-50 dark:border-white/5 border-border-light border-y">
            {handleTags(tags)} 
        </div>  
    )
}