import { useMemo, type ComponentType, type JSX, type SVGProps } from "react";
import { Star,ExternalLink, Bookmark, type LucideProps} from "lucide-react"
import VIconRounded from "../DynamicSvgs/VIconRounded"


type IconComponent = ComponentType<LucideProps | SVGProps<SVGSVGElement>>;

type PostButtonType = {
    order: number
    title: string
    position: 'left' | 'right'
    color: string
    fillColor?: string
    icon: IconComponent
    data: number
}

const postButtons: Array<PostButtonType> = [
    {
        order: 1,
        title: 'Share',
        position: 'left',
        icon: ExternalLink,
        color: '#c084fc',
        data: 999999999
    },
    {
        order: 2,
        title: 'Save',
        position: 'left',
        color: '#60a5fa',
        // fillColor: '#60a5fa',
        icon: Bookmark,
        data: 96000
    },
    {
        order: 3,
        title: 'Rate',
        color: '#fbbf24',
        // fillColor: '#facc15',
        position: 'left',
        icon: Star,
        data: 9876
    },
    {
        order: 4,
        title: 'Visits',
        color: '#22c55e',
        // fillColor: '#22c55e',
        position: 'right',
        icon: VIconRounded,
        data: 318099
    },
    
]


export default function PostButtons(): JSX.Element{

    const handlePostStats = (stat: number): string => {
    if (stat === 0) return "0"

    const thousand = 1000
    const tenThousand = 10000
    const million = 1000000
    const billion = 1000000000
    const trillion = 1000000000000

    const floorStat = (value: number) => {
        return Math.floor(value * 10) / 10;
    };

        if (stat >= trillion) {
            return floorStat(stat / trillion) + 't'
        } 
        if (stat >= billion) {
            return floorStat(stat / billion) + 'b'
        } 
        if (stat >= million) {
            return floorStat(stat / million) + 'm'
        }
        if(stat >= tenThousand){
            return floorStat(stat / thousand) + 'k'
        }
        
    return stat.toString();
    }

    const {leftButtons, rightButtons} = useMemo(() => {
        const sortedButtons = postButtons.sort((btn1, btn2) => btn1.order - btn2.order)
        return{
            leftButtons: sortedButtons.filter(btn => btn.position === 'left'),
            rightButtons: sortedButtons.filter(btn => btn.position === 'right')
        }
    }, [])

    function renderPostButtons(btnArray: Array<PostButtonType>): JSX.Element {
        return(
            <>
                <div className="flex gap-2 text-neutral-400">
                    {btnArray.map((btn: PostButtonType) => {
                            return(
                                <button
                                    key={btn.title}
                                    title={btn.title}
                                    style={{'--btn-color': btn.color, '--btn-fill-color': btn.fillColor} as React.CSSProperties}
                                    className="group flex items-center gap-1 hover:text-white transition-colors cursor-pointer"
                                >
                                    {/* TODO: change stroke and fill to be on when user completes action */}
                                    <btn.icon
                                        strokeWidth={1}
                                        className={`stroke-(--btn-color) ${btn.fillColor && 'fill-(--btn-fill-color)'} transition-colors`}
                                    >
                                    </btn.icon>
                                    {/* TODO: replace hardcoded stat with real data */}
                                    <span className="font-medium text-xs">{handlePostStats(1219994)}</span>
                                </button>
                            )
                    })}
                </div>
            </>
        )
    }

    return(
        <div className="flex flex-1 justify-between items-center gap-4 px-4 w-full text-xs">
            {renderPostButtons(leftButtons)}
            {renderPostButtons(rightButtons)}
        </div>
    )
}