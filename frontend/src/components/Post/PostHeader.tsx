import { Accessibility, Star } from "lucide-react";
import { type JSX } from "react";

export default function PostHeader(): JSX.Element{
    return(
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
    )
}