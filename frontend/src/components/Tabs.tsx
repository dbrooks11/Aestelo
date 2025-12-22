import { useState, useRef, type JSX, type ReactElement, type ReactNode } from "react";
import cn from "../util/tailwind_merger";

type TabsProps = {
    children: Array<JSX.Element>
    tabsAndContentContainerStyle?: string 
    tabsContainerStyle?: string 
    tabsStyle?: string
    activeTabStyle?: string
    tabsIconStyle?: string
    tabsLabelStyle?: string 
}

const Tabs = ({children, tabsAndContentContainerStyle, tabsContainerStyle, tabsStyle, activeTabStyle, tabsIconStyle, tabsLabelStyle}: TabsProps) => {

    const [activeTab, setActiveTab] = useState(children[0].props.label)
    const tabsContentRef = useRef<HTMLElement | null>(null)


    const handleTabClick = (e, newActiveTab: string) =>{
        e.preventDefault()
        setActiveTab(newActiveTab)

        const offset = 115
        
        if(tabsContentRef.current){
            const contentPosition = tabsContentRef.current.getBoundingClientRect().top
            const offsetPosition = contentPosition + window.scrollY - offset

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            })
        }
    }

    return (
        <div className={cn("flex flex-col", tabsAndContentContainerStyle)} id="tabs_and_content_container">
            <div 
            className={cn("flex justify-center items-center", tabsContainerStyle)} 
            id="tabs_container" aria-roledescription='tablist'
            >
                {children.map((child)=> {

                    return(
                    <button
                        key = {child.props.label}
                        className={`${activeTab === child.props.label ? `${cn('', activeTabStyle)}` : ''}  ${child.props.icon && child.props.label ? 'gap-4' : ''} ${cn('flex justify-center items-center p-4 w-1/4 cursor-pointer', tabsStyle)}`}
                        onClick={(e) => handleTabClick(e, child.props.label)}
                        aria-roledescription="tab"
                        id="tab"
                    >
                        <span className={cn("md:hidden", tabsIconStyle)} title={child.props.label}>{child.props.icon ? child.props.icon : null}</span>
                        <span className={cn("hidden md:inline", tabsLabelStyle)}>{child.props.label}</span>
                    </button>
                    )
                })}
            </div>
            <section ref={tabsContentRef}>
                {children.map((child)=> {
                    if(child.props.label === activeTab){
                        return <div key={child.props.label}>{child.props.children}</div>
                    }
                    return null
                })}
            </section>
        </div>
    )
}

type TabProps= {
    icon?: ReactElement
    label?: string
    children: ReactNode
}


const Tab = ({ icon, label, children }: TabProps) => {
    return (
        <div icon={icon} label={label} className="hidden">
            {children}
        </div>
    )
}

export {Tabs, Tab}