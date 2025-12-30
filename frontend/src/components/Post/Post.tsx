import { useEffect, useRef, type JSX } from "react";
import { Accessibility, Star, Ellipsis
    ,ExternalLink, Bookmark} from "lucide-react";
import VIconRounded from "../DynamicSvgs/VIconRounded";
import ScrollContainer from "react-indiana-drag-scroll";
import testImage from "../../assets/testImage.jpg"

// type PostProps = {
//     name: string
//     date_posted: string
//     description: string
//     total_num_of_photos: number
//     average_rating: number
//     total_num_of_ratings: string
//     save_count: number
//     share_count: string
//     hashtags: Array<string>
//     accessibility: boolean

// }

const testTags = ['#b', '#rickowens', '#b', '#ok', '#fishing', '#f', '#h', '#tr', '#r','#okay', '#robotics', '#iloverickowensnow', '#metoo', '#ro' , '#meow']

export default function Post(): JSX.Element{

    //TODO: move containerRef and useEffect to tags component 
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
            const topRowTags: Array<string> = tags.filter((_, index) => index % 2 === 0)
            const bottomRowTags: Array<string> = tags.filter((_, index) => index % 2 !== 0)

            return(
                <ScrollContainer 
                    className="flex flex-col w-full h-full overflow-x-scroll no-scrollbar gap-1"
                    innerRef={scrollRef}
                    >
                    <div className="flex items-center justify-start gap-4 h-1/2">
                        {topRowTags.map((tag)=> {
                            return(
                                <span key={tag} className="flex items-center px-1 py-0.5 rounded-md border">{tag}</span>
                            )
                        })}
                    </div>
                    <div className={'flex items-center gap-4 w-full px-4 h-1/2'}>
                        {bottomRowTags.map((tag) =>{
                            return(
                                <span className="flex justify-center items-center px-1 py-0.5 rounded-md border">{tag}</span>
                            )
                        })}
                    </div>
                </ScrollContainer>
            )
        }
    }

    const showPhotos = (photos: Array<object>): JSX.Element => {

        return(
            <></>
        )
    }

    return(
        
        <div className="flex flex-col mx-auto border border-white w-90 mb-200 bg-slate rounded-xs">
            
            {/* Images and Header container */}
            <div className="relative flex flex-1">
                
                {/* Header */}
                <div className="top-4 right-20 absolute flex flex-col justify-center items-center bg-white/10 backdrop-blur-lg px-2 py-1 border border-white text-xs">
                    <div className="flex items-center gap-2 px-1">
                        <span>Name placeholder</span>
                        <Accessibility/>
                    </div>
                    <div className="flex justify-center items-center gap-2">
                        <span className="flex items-center"><Star strokeWidth={1} className="w-full h-full"/>4.8</span>
                        <span>•</span>
                        <span>5.2k</span>
                        <span>•</span>
                        <span>2 mins ago</span>
                    </div>
                </div>

                {/* Description and Photo Counter */}
                    <div className="bottom-1 left-1 absolute flex text-white">
                        <span aria-hidden='true'>[</span>
                        <span aria-hidden='true' className="pt-0.5"><Ellipsis/></span>
                        <span aria-hidden='true'>]</span>
                    </div>

                    <div className="right-1 bottom-1 absolute flex justify-center items-center p-1 border border-white rounded-full w-8 h-8 text-[10px] text-white">
                        <span>3/10</span>
                    </div>
                
                {/* Photos */}
                {}
                <img 
                    src={testImage} 
                    className="h-full w-full"
                    alt='Post content'
                    ></img>
            </div>
            {/* Action button and tags container */}
            <div className="flex flex-col items-center justify-center border border-white w-full bg-black/20 backdrop-blur-md min-h-30 gap-2">

                {/* Hashtags */}
                {/* TODO: map over each tag to display it */}
                <div className="flex justify-center items-center h-1/2 w-full text-white px-8 text-[10px]">
                        {handleTags(testTags)}
                </div>   

                {/* Action Buttons */}
                <div className="flex justify-center items-center h-1/2 text-white w-full">
                    <div className="flex items-center justify-center text-sm gap-2">
                        <div className="flex justify-center items-center w-1/4">
                            <button><ExternalLink strokeWidth={1.5} className="w-full h-full"/></button>
                            <span>999.8m</span>
                        </div>
                        <div className="flex justify-center items-center w-1/4">
                            <button><Bookmark strokeWidth={1.5} className="w-full h-full"/></button>
                            <span>234.8m</span>
                        </div>
                        <div className="flex justify-center items-center w-1/4">
                            <button><Star strokeWidth={1.5} className="w-full h-full"/></button>
                            <span>234.8m</span>
                        </div>
                        <div className="flex justify-center items-center w-1/4">
                            <button><VIconRounded strokeWidth={1.5} className="w-full h-full"/></button>
                            <span>999.6m</span>
                        </div>
                    </div>
                    
                </div>          
            </div>
        </div>
    )
}