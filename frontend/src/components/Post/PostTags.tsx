import { useEffect, useRef, type JSX } from "react";
import ScrollContainer from "react-indiana-drag-scroll";


const testTags = ["streetwear", "archive", "rickowens", "fashion", "ootd", "style", "vintage", "grailed", "y2k", "opium"]


export default function PostTags(): JSX.Element{

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
        if(tags){
            return(
                <ScrollContainer 
                    className="flex flex-col justify-center gap-1 mask-x-from-90% mask-x-to-100% w-full h-full overflow-x-scroll no-scrollbar mx-2"
                    innerRef={scrollRef}
                    >
                    <div className="flex justify-start items-center gap-2 mx-2">

                        {tags.map((tag)=> {

                            return(
                                <span 
                                    key={tag} 
                                    className='flex justify-center items-center bg-neutral-700 px-1.5 py-0.5 border dark:border-white/5 rounded-md min-w-8 hover:text-accents-primary whitespace-nowrap hover:cursor-pointer shrink-0 drop-shadow-sm'
                                    >
                                        #{tag}
                                </span>
                            )
                        })}
                    </div>
                </ScrollContainer>
            )
        }else{
            return <span>• No tags</span>
        }
    }
    
    return(
        <div className="flex w-full h-10 text-[10px] text-white dark:bg-slate/50 dark:border-white/5 border">
            {handleTags(testTags)} 
        </div>  
    )
}