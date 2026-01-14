import { useMemo, type CSSProperties, type ComponentType, type JSX, type SVGProps } from "react";
import { Star,ExternalLink, Bookmark, type LucideProps} from "lucide-react"
import VIconRounded from "../DynamicSvgs/VIconRounded"
import { handleNumStats } from "../../util/StatConverter";


type IconComponent = ComponentType<LucideProps | SVGProps<SVGSVGElement>>;

type SpotButtonType = {
    order: number
    title: string
    position: 'left' | 'right'
    color: string
    fillColor?: string
    icon: IconComponent
    data: number
}

type SpotButtonProps = {
    shareCount: number,
    saveCount: number,
    totalNumOfRatings: number
    visitCount: number
}

export default function SpotButtons({shareCount, saveCount, 
    totalNumOfRatings, visitCount
}: SpotButtonProps): JSX.Element{

    const spotButtons: Array<SpotButtonType> = [
        {
            order: 1,
            title: 'Share',
            position: 'left',
            icon: ExternalLink,
            color: '#c084fc',
            data: shareCount
        },
        {
            order: 2,
            title: 'Save',
            position: 'left',
            color: '#60a5fa',
            // fillColor: '#60a5fa',
            icon: Bookmark,
            data: saveCount
        },
        {
            order: 3,
            title: 'Rate',
            color: '#fbbf24',
            // fillColor: '#facc15',
            position: 'left',
            icon: Star,
            data: totalNumOfRatings
        },
        {
            order: 4,
            title: 'Visit',
            color: '#22c55e',
            // fillColor: '#22c55e',
            position: 'right',
            icon: VIconRounded,
            data: visitCount
        },
    ]   

    

    const {leftButtons, rightButtons} = useMemo(() => {
        const sortedButtons = spotButtons.sort((btn1, btn2) => btn1.order - btn2.order)
        return{
            leftButtons: sortedButtons.filter(btn => btn.position === 'left'),
            rightButtons: sortedButtons.filter(btn => btn.position === 'right')
        }
    }, [])

    function renderSpotButtons(btnArray: Array<SpotButtonType>): JSX.Element {
        return(
            <>
                <div className="flex gap-2.5 dark:text-neutral-400 text-neutral-600">
                    {btnArray.map((btn: SpotButtonType) => {
                            return(
                                <button
                                    key={btn.title}
                                    title={btn.title}
                                    style={{'--btn-color': btn.color, '--btn-fill-color': btn.fillColor} as CSSProperties}
                                    className="group flex items-center gap-1 hover:dark:text-white hover:text-black transition-colors cursor-pointer"
                                >
                                    {/* TODO: change stroke and fill to be on when user completes action */}
                                    <btn.icon
                                        strokeWidth={1}
                                        className={`group-hover:stroke-(--btn-color) ${btn.fillColor && 'fill-(--btn-fill-color)'} transition-colors`}
                                    >
                                    </btn.icon>
                                    <span className="font-medium text-xs">{handleNumStats(btn.data)}</span>
                                </button>
                            )
                    })}
                </div>
            </>
        )
    }

    return(
        <div className="flex flex-1 justify-between items-center gap-4 px-4 w-full text-xs">
            {renderSpotButtons(leftButtons)}
            {renderSpotButtons(rightButtons)}
        </div>
    )
}