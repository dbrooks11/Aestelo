import { useState, useRef, type JSX, type ReactElement, type ReactNode } from "react";
import cn from "../util/tailwind_merger";

type TabsProps = {
    children: Array<JSX.Element>
    tabsAndContentContainerStyle?: string 
    tabsContainerStyle?: string 
    tabContentStyle?: string
    tabsStyle?: string
    activeTabStyle?: string
    tabsIconStyle?: string
    tabsLabelStyle?: string 
}

const Tabs = ({children, tabsAndContentContainerStyle, tabsContainerStyle, tabsStyle, activeTabStyle, 
    tabsIconStyle, tabsLabelStyle, tabContentStyle}: TabsProps) => {

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
    
            {/*  Tab Header */}
            <div 
                className={cn("flex justify-center items-center", tabsContainerStyle)} 
                id="tabs_container" 
                role="tablist" 
                aria-label="Profile Sections" 
            >
                {children.map((child, index) => {
                    const isActive = activeTab === child.props.label;
                    const tabId = `tab-${index}`;
                    const panelId = `panel-${index}`;

                    return (
                        <button
                            key={child.props.label}
                            role="tab" 
                            id={tabId}
                            aria-selected={isActive} 
                            aria-controls={panelId} 
                            tabIndex={isActive ? 0 : -1} 
                            
                            className={`${isActive ? `${cn('', activeTabStyle)}` : ''}  ${child.props.icon && child.props.label ? 'gap-4' : ''} ${cn('flex justify-center items-center p-3 w-1/4 cursor-pointer', tabsStyle)}`}
                            
                            onClick={(e) => {
                                e.stopPropagation()
                                handleTabClick(e, child.props.label)
                            }}
                        >
                            {/* Icon - Hidden on desktop, visible on mobile */}
                            <span 
                                className={cn("md:hidden", tabsIconStyle)} 
                                title={child.props.label}
                                aria-hidden="true" 
                            >
                                {child.props.icon ? child.props.icon : null}
                            </span>

                            {/* Label - Visible on desktop */}
                            <span className={cn("hidden md:inline", tabsLabelStyle)}>
                                {child.props.label}
                            </span>
                        </button>
                    )
                })}
            </div>

            {/* Tab Content */}
            <section ref={tabsContentRef} className={tabContentStyle}>
                {children.map((child, index) => {
                    const isActive = child.props.label === activeTab;
                    const panelId = `panel-${index}`;
                    const tabId = `tab-${index}`;

                    if (isActive) {
                        return (
                            <div 
                                key={child.props.label}
                                role="tabpanel" 
                                id={panelId}
                                aria-labelledby={tabId} 
                                tabIndex={0} 
                            >
                                {child.props.children}
                            </div>
                        )
                    }
                    return null;
                })}
            </section>
        </div>
    )
}

type TabProps= {
    icon?: ReactElement
    label?: string
    children: ReactNode
    className?: string
}


const Tab = ({ icon, label, children }: TabProps) => {
    return (
        <div icon={icon} label={label} className="hidden">
            {children}
        </div>
    )
}

export {Tabs, Tab}