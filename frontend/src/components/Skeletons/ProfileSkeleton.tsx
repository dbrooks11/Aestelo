import { type JSX } from "react";

//TODO: finish skeleton loader
export default function ProfileLoadingSkeleton(): JSX.Element{
    return(
        <div 
            className="min-h-screen w-full flex flex-col items-center p-6"
            aria-hidden="true"
            role="profile loader"
            >
            {/* Banner loader*/}
            <div className="w-full h-70 md:h-80 bg-gray-300/60 dark:bg-white/10 animate-pulse rounded-sm"></div>
            
            {/* Wrapper for Photo + Info */}
            <div className="flex flex-col w-full items-center gap-6 md:px-15 -mt-15"> 
                
                
                <div className="flex flex-col md:flex-row w-full items-center gap-4 z-10">

                    {/* Photo loader */}
                    <div className="rounded-full bg-bg-light-secondary border-bg-light-secondary dark:bg-charcoal border-8 dark:border-charcoal shrink-0">
                        <div className="rounded-full min-h-35 min-w-35 bg-gray-300/60 dark:bg-white/10 animate-pulse shrink-0"></div>
                    </div>
                    

                    {/* Info loader */}
                    <div className="flex flex-col w-full gap-4 items-center md:items-start">
                        <div className="w-full flex md:justify-between justify-center">
                            {/* Username loader */}
                            <div className=" flex w-1/2 md:w-1/3 bg-bg-light-secondary border-bg-light-secondary dark:bg-charcoal border-8 dark:border-charcoal rounded-full">
                                <div className="w-full bg-gray-300/60 dark:bg-white/10 h-6 animate-pulse rounded-full"></div>
                            </div>
                            {/* edit button loader */}
                            <div className=" md:flex w-1/2 md:w-1/8 bg-bg-light-secondary border-bg-light-secondary dark:bg-charcoal border-0 md:border-8 dark:border-charcoal rounded-full hidden">
                                <div className="w-full bg-gray-300/60 dark:bg-white/10 h-8 animate-pulse rounded-full"></div>
                            </div>
                        </div>
                        
                        
                        <div className="w-3/4 md:w-1/2 flex gap-2">
                            {[1,2,3,4].map((i)=>(
                                <div key={i} className="w-1/4 bg-gray-300/60 dark:bg-white/10 h-6 animate-pulse rounded-full"></div>
                            ))}
                        </div> 
                        
                    </div>
                </div>
                
                {/* Bio loader */}
                <div className="w-full flex justify-center md:justify-start">
                    <div className="w-4/5 h-6 bg-gray-300/60 dark:bg-white/10 animate-pulse rounded-xl"></div>
                </div>
                

                {/* Links */}
                <div className="flex w-full gap-4">
                    {[1,2,3,4].map((i)=>(
                                <div key={i} className="w-1/3 bg-gray-300/60 dark:bg-white/10 animate-pulse h-4 rounded-full"></div>
                    ))}
                </div>

                
            </div>
            <div className="rounded-sm bg-gray-300/60 dark:bg-white/10 animate-pulse w-full flex-1 mt-6"></div>
        </div>
    )
}