import { type JSX } from "react";
import type { ProfileDataType } from "../../../pages/ProfilePage";
import cn from "../../../util/tailwind_merger";

type ProfilePhotoPlaceholderType = {
    username: ProfileDataType['username']
    className?: string
}

export default function ProfilePhotoPlaceholder({username, className}: ProfilePhotoPlaceholderType): JSX.Element{
    return(
        <div 
            className={cn(className, 'dark:text-white text-black font-bold rounded-full w-full h-full flex items-center justify-center pointer-events-none')}
            role="img"
            aria-label={`Avatar for ${username}`}
        >
        <span aria-hidden="true">
            {username.charAt(0) + username.charAt(username.length - 1)}
        </span>
        </div>
    )
}