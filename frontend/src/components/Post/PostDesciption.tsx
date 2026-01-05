import { AnimatePresence, motion } from "framer-motion";
import { Ellipsis } from "lucide-react";
import { useState, type JSX } from "react";

export default function PostDescripton(): JSX.Element{

    const [showDescription, setShowDescription] = useState<boolean>(false)
    

    return(
        <div 
            className="bottom-1 left-2 absolute flex  text-white text-xs cursor-pointer "

        >
            <AnimatePresence mode="wait">
                {showDescription ? 
                <motion.div 
                    key='description'
                    id="post-description-content"
                    role="button"
                    tabIndex={0}
                    aria-expanded={true}
                    aria-label="Post description. Click to collapse."
                    initial={{opacity: 0}}
                    animate={{opacity: 1}}
                    exit={{opacity: 0}}
                    transition={{duration: 0.1}}
                    className= 'flex dark:bg-black/10 bg-white/10 backdrop-blur-[2px] p-1 borderborder-neutral-300/40 h-min overflow-y-scroll no-scrollbar  max-w-55 max-h-30 overscroll-contain'
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
                            <p className="text-shadow-2xs">
                                Breastfeeding is good for babies and moms. Infants that are breastfed get antibodies from their mothers against common illnesses. Breastfed babies have less chance of being obese as an adult. Breastfeeding a baby lets the infant-mother pair bond in a very unique way. Mother’s who breastfeed lower their chances of developing breast cancer. Usually, mothers who breastfeed lose their pregnancy weight more quickly and easily. The benefits of breastfeeding are numerous.
                            </p>
                </motion.div>: 
                <motion.button
                    key="button"
                    type="button"
                    role="button"
                    aria-label="Show full description"
                    aria-expanded={false}
                    aria-controls="post-description-content"
                    tabIndex={0}
                    initial={{ opacity: 0}}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{duration: 0.1}}
                    onClick={(e) => {
                        e.stopPropagation()
                        setShowDescription(true)}}
                    className= 'flex items-center dark:bg-black/10 bg-white/10 backdrop-blur-[2px] px-0.5 border-neutral-300/40 h-5 cursor-pointer'
                    >
                    <span aria-hidden='true' className="">[</span>
                    <span aria-hidden='true' className="mt-0.5"><Ellipsis/></span>
                    <span aria-hidden='true' className="">]</span>
                </motion.button>}
            </AnimatePresence>
        </div>
    )
}