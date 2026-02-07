import { type JSX, type ReactNode } from "react";
import cn from "../../util/tailwind_merger";


export default function ContentHeader({className, children}: {className?: string, children: ReactNode}):JSX.Element{
    return(
        <div className={`${cn("top-1/24 left-1/2 -translate-x-1/2 absolute flex flex-col justify-center items-center gap-[0.25em] border-neutral-300/30 bg-black/10 backdrop-blur-[2px] px-2 py-1 border text-[0.75em] text-white z-20 max-w-[94%] ", className)}`}>
            {children}
        </div>
    )
}