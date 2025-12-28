import { type JSX } from "react";

export default function ProfileLoadingSkeleton(): JSX.Element{
    return(
        <div 
            className="flex flex-col items-center p-6 w-full min-h-screen"
            aria-hidden="true"
            role="profile loader"
            >
            {/* Banner loader*/}
            <div className="bg-gray-300/60 dark:bg-white/10 rounded-sm w-full h-70 md:h-80 animate-pulse"></div>
            
            {/* Wrapper for Photo + Info */}
            <div className="flex flex-col items-center gap-6 -mt-15 md:px-15 w-full"> 
                
                
                <div className="z-10 flex md:flex-row flex-col items-center gap-4 w-full">

                    {/* Photo loader */}
                    <div className="bg-bg-light-secondary dark:bg-charcoal border-8 border-bg-light-secondary dark:border-charcoal rounded-full shrink-0">
                        <div className="bg-gray-300/60 dark:bg-white/10 rounded-full min-w-35 min-h-35 animate-pulse shrink-0"></div>
                    </div>
                    

                    {/* Info loader */}
                    <div className="flex flex-col items-center md:items-start gap-4 w-full">
                        <div className="flex justify-center md:justify-between w-full">
                            {/* Username loader */}
                            <div className="flex bg-bg-light-secondary dark:bg-charcoal border-8 border-bg-light-secondary dark:border-charcoal rounded-full w-1/2 md:w-1/3">
                                <div className="bg-gray-300/60 dark:bg-white/10 rounded-full w-full h-6 animate-pulse"></div>
                            </div>
                            {/* edit button loader */}
                            <div className="hidden md:flex bg-bg-light-secondary dark:bg-charcoal border-0 border-bg-light-secondary md:border-8 dark:border-charcoal rounded-full w-1/2 md:w-1/8">
                                <div className="bg-gray-300/60 dark:bg-white/10 rounded-full w-full h-8 animate-pulse"></div>
                            </div>
                        </div>
                        
                        
                        <div className="flex gap-2 w-3/4 md:w-1/2">
                            {[1,2,3,4].map((i)=>(
                                <div key={i} className="bg-gray-300/60 dark:bg-white/10 rounded-full w-1/4 h-6 animate-pulse"></div>
                            ))}
                        </div> 
                        
                    </div>
                </div>
                
                {/* Bio loader */}
                <div className="flex justify-center md:justify-start w-full">
                    <div className="bg-gray-300/60 dark:bg-white/10 rounded-xl w-4/5 h-6 animate-pulse"></div>
                </div>
                

                {/* Links */}
                <div className="flex gap-4 w-full">
                    {[1,2,3,4].map((i)=>(
                                <div key={i} className="bg-gray-300/60 dark:bg-white/10 rounded-full w-1/3 h-4 animate-pulse"></div>
                    ))}
                </div>

                
            </div>
            <div className="flex-1 bg-gray-300/60 dark:bg-white/10 mt-6 rounded-sm w-full animate-pulse"></div>
        </div>
    )
}