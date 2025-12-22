import { useState, type JSX, type ReactElement, type ReactNode } from "react";

const Tabs = ({children}: {children: Array<JSX.Element>}) => {

    const [activeTab, setActiveTab] = useState(children[0].props.label)

    const handleTabClick = (e, newActiveTab: TabProps) =>{
        e.preventDefault()
        setActiveTab(newActiveTab)
    }

    return (
        <div className="mt-12 flex flex-col w-full">
            <div className="flex z-10 justify-center items-center" role='tablist'>
                {children.map((child)=> {

                    return(
                    <button
                        key = {child.props.label}
                        className={`${activeTab === child.props.label ? 'dark:text-white text-accents-deep border-b-2 border-b-accents-primary' : ''}  ${child.props.icon && child.props.label ? 'gap-4' : ''} w-1/4 p-4 dark:text-neutral-500 font-bold cursor-pointer hover:dark:text-white hover:text-accents-deep flex items-center justify-center`}
                        onClick={(e) => handleTabClick(e, child.props.label)}
                    >
                        {child.props.icon ? child.props.icon : null}
                        {child.props.label}
                    </button>
                    )
                })}
            </div>
            <section>
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