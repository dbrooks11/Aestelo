import { useMemo, type ComponentType, type JSX, 
    type SVGProps,type ReactNode, Fragment} from "react";
import SpotButtonBase from "./ButtonBase";
import type { LucideProps } from "lucide-react";


type IconComponent = ComponentType<LucideProps | SVGProps<SVGSVGElement>>;

export type ButtonType = {
    order: number
    title?: string
    position: 'left' | 'right'
    color?: string
    fillColor?: string
    icon?: IconComponent
    data?: number
    component?: ReactNode 
}


export default function PostTypeActionButtons({buttons}:{buttons: Array<ButtonType>}): JSX.Element{

    const {leftButtons, rightButtons} = useMemo(() => {
        const sortedButtons = [...buttons].sort((btn1, btn2) => btn1.order - btn2.order)
        return{
            leftButtons: sortedButtons.filter(btn => btn.position === 'left'),
            rightButtons: sortedButtons.filter(btn => btn.position === 'right')
        }
    }, [buttons])

    function renderSpotButtons(btnArray: Array<ButtonType>): JSX.Element {
        return(
            <>
                <div className="flex gap-2.5 text-neutral-600 dark:text-neutral-400 items-center">
                {btnArray.map((btn, index) => {
                    if (btn.component) {
                        return <Fragment key={index}>{btn.component}</Fragment>
                    }
                    return (
                        <SpotButtonBase
                            key={index}
                            title={btn.title!}
                            icon={btn.icon}
                            data={btn.data!}
                            fillColor={btn.fillColor}
                            color={btn.color!}
                        />
                    );
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