import { AnimatePresence, motion } from "framer-motion";
import cn from "../../util/tailwind_merger";
import { Ellipsis } from "lucide-react";
import { useState, type JSX } from "react";

type DesciptionProps = {
    description: string
    className?: string
}

export default function DescriptonOrCaption({description, className}: DesciptionProps): JSX.Element{

    const [showDescription, setShowDescription] = useState<boolean>(false)

    return(
        <div 
            className={`${cn('bottom-1 left-2 absolute flex text-white cursor-pointer z-20 max-w-3/4 text-[0.75em]', className)}`}

        >
            <AnimatePresence mode="wait">
                {showDescription ? 
                <motion.div 
                    key='description'
                    id="description-or-caption-content"
                    role="button"
                    tabIndex={0}
                    aria-expanded={true}
                    aria-label="Description/Caption. Click to collapse."
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
                    aria-label="Show full description/caption"
                    aria-expanded={false}
                    aria-controls="description-or-caption-content"
                    tabIndex={0}
                    initial={{ opacity: 0}}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{duration: 0.1}}
                    onClick={(e) => {
                        e.stopPropagation()
                        setShowDescription(true)}}
                    className= 'flex items-center dark:bg-black/10 bg-white/10 backdrop-blur-[2px] px-0.5 border-neutral-300/40 cursor-pointer h-[1.75em] select-none'
                    >
                    <span aria-hidden='true' className="text-[1.25em]">[</span>
                    <span aria-hidden='true' className="mt-[0.25em] flex shrink"><Ellipsis className="w-[1.75em] h-[1.75em]"/></span>
                    <span aria-hidden='true' className="text-[1.25em]">]</span>
                </motion.button>}
            </AnimatePresence>
        </div>
    )
}