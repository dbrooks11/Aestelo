import { AnimatePresence, motion } from "framer-motion";
import cn from "../../util/tailwind_merger";
import { Ellipsis } from "lucide-react";
import { useState, type JSX } from "react";

type SpotDesciptionProps = {
    description: string
    className?: string
}

export default function SpotDescripton({description, className}: SpotDesciptionProps): JSX.Element{

    const [showDescription, setShowDescription] = useState<boolean>(false)

    return(
        <div 
            className={`${cn('bottom-1 left-2 absolute flex text-white text-xs cursor-pointer z-20 max-w-3/4', className)}`}

        >
            <AnimatePresence mode="wait">
                {showDescription ? 
                <motion.div 
                    key='description'
                    id="spot-description-content"
                    role="button"
                    tabIndex={0}
                    aria-expanded={true}
                    aria-label="Spot description. Click to collapse."
                    initial={{opacity: 0}}
                    animate={{opacity: 1}}
                    exit={{opacity: 0}}
                    transition={{duration: 0.1}}
                    className= 'flex dark:bg-black/10 bg-white/10 backdrop-blur-[2px] p-1 border border-neutral-300/40 overflow-y-auto no-scrollbar overscroll-contain max-h-25'
                    onClick={(e) => {
                        e.stopPropagation()
                        setShowDescription(false)}}
                    onKeyDown={(e) => {
                        if(e.key === 'Enter' || e.key === ' '){
                            e.stopPropagation()
                            setShowDescription(false)
                        }
                    }}
                    >
                            <p className="text-shadow-2xs max-w-full wrap-break-word">
                                {description}
                            </p>
                </motion.div>: 
                <motion.button
                    key="button"
                    type="button"
                    role="button"
                    aria-label="Show full description"
                    aria-expanded={false}
                    aria-controls="spot-description-content"
                    tabIndex={0}
                    initial={{ opacity: 0}}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{duration: 0.1}}
                    onClick={(e) => {
                        e.stopPropagation()
                        setShowDescription(true)}}
                    className= 'flex items-center dark:bg-black/10 bg-white/10 backdrop-blur-[2px] px-0.5 border-neutral-300/40 cursor-pointer h-5'
                    >
                    <span aria-hidden='true' className="">[</span>
                    <span aria-hidden='true' className="mt-0.5 flex shrink"><Ellipsis className="w-full h-full"/></span>
                    <span aria-hidden='true' className="">]</span>
                </motion.button>}
            </AnimatePresence>
        </div>
    )
}