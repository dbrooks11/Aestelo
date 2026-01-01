import { useMemo, type ComponentType, type JSX, type SVGProps } from "react";
import { Star,ExternalLink, Bookmark, type LucideProps} from "lucide-react"
import VIconRounded from "../DynamicSvgs/VIconRounded"
import { handleNumStats } from "../../util/StatConverter";


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
                <div className="flex gap-2.5 dark:text-neutral-400 text-neutral-600">
                    {btnArray.map((btn: PostButtonType) => {
                            return(
                                <button
                                    key={btn.title}
                                    title={btn.title}
                                    style={{'--btn-color': btn.color, '--btn-fill-color': btn.fillColor} as React.CSSProperties}
                                    className="group flex items-center gap-1 hover:dark:text-white hover:text-black transition-colors cursor-pointer"
                                >
                                    {/* TODO: change stroke and fill to be on when user completes action */}
                                    <btn.icon
                                        strokeWidth={1}
                                        className={`group-hover:stroke-(--btn-color) ${btn.fillColor && 'fill-(--btn-fill-color)'} transition-colors`}
                                    >
                                    </btn.icon>
                                    {/* TODO: replace hardcoded stat with real data */}
                                    <span className="font-medium text-xs">{handleNumStats(1219994)}</span>
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