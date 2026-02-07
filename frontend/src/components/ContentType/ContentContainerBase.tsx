import { ChevronLeft, ChevronRight } from "lucide-react";
import { type Dispatch, type JSX, type ReactNode, type SetStateAction } from "react";
import cn from "../../util/tailwind_merger";

type Props = {
    className?: string
    totalNumOfPhotos: number
    progress: number
    setProgress: Dispatch<SetStateAction<number>>
}

type ContentContainerProps = {
    props: Props
    children: Array<ReactNode>
}

export default function ContentContainerBase({props, children}: ContentContainerProps): JSX.Element{
    return(
         <div 
            className={`${cn('flex flex-col dark:bg-off-slate bg-white border dark:border-border-dark border-border-light rounded-sm w-80 text-sm sm:w-90 sm:text-base', props.className)}`}
        >
                    
            {/* Images and Header container */}
            <div 
                className="relative flex flex-1"
            >
                {children[0]}

                <div 
                className="absolute flex left-1 bottom-[50%]">
                <button 
                    className=" w-[1.75em] h-[1.75em] flex items-center justify-center rounded-full bg-black/10 backdrop-blur-[2px] text-white/70 border border-white/10  active:scale-90 cursor-pointer shadow-2xl z-20" 
                    onClick={() => props.setProgress(Math.max(1, props.progress - 1))}
                    aria-label="previous button"
                >
                    <ChevronLeft/>
                </button>
                </div>
                <div className="absolute flex right-1 bottom-[50%]">
                    <button 
                        className=" w-[1.75em] h-[1.75em] flex items-center justify-center rounded-full bg-black/10 backdrop-blur-[2px] text-white/70 border border-white/10  active:scale-90 cursor-pointer z-20" 
                        onClick={() => props.setProgress(Math.min(props.totalNumOfPhotos, props.progress + 1))}
                        aria-label="next button"
                    >
                        <ChevronRight/>
                    </button>
                </div>
            </div>
            <div className="flex flex-col dark:bg-off-slate w-full min-h-[6.5em]">
                {children[1]}  
            </div>
        </div>
    )
}