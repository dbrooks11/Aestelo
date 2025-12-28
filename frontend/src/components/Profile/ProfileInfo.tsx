
import {type JSX} from 'react'
import { type ProfileDataType , type ProfileDataUseState } from '../../pages/ProfilePage'
import ProfileLinks from './ProfileLinks'
import ProfileBadges from './ProfileBadges'
import { UserPen } from 'lucide-react'


type BaseProfileInfoParams = Pick<ProfileDataType , 'username' | 'profile_photo_url' | 'bio' 
                                            | 'following_count' | 'follower_count'
                                            | 'post_count' | 'visit_count' | 'instagram'
                                            | 'tiktok' | 'twitter_x' | 'facebook'>

type ProfileInfoParams = BaseProfileInfoParams & {
    setProfileData: (profile: ProfileDataType  | null) => void
    profileData: ProfileDataUseState
    showModal: boolean
    setShowModal: (value:boolean) => void
}


const followsAndPostCountStyle = "font-normal text-[11px] sm:text-sm md:text-base"

export default function ProfileInfo(props: ProfileInfoParams):JSX.Element {

    const editProfileButtonClick = () => {
        props.setShowModal(!props.showModal)
    }

  return (
    <section className='z-10 relative justify-items-center mt-50 md:mt-60 w-full'>
        <div className='z-10 flex flex-col pb-8 border-b border-b-neutral-300 dark:border-b-neutral-800 w-5/6'>
            <section className='flex md:flex-row flex-col items-center gap-6 px-4 relative'>
                
                {/* Profile Picture */}
                <figure className='w-35 h-35 flex relative'>
                    <img 
                        className="rounded-full w-full h-full object-cover pointer-events-none" 
                        src={props.profile_photo_url} 
                        alt={`${props.username}'s profile picture`}
                    />
                    <button
                        className='lg:hidden flex absolute z-10 top-25 left-25 bg-accents-primary/5 dark:bg-white/10 backdrop-blur-sm p-2 rounded-full w-8 cursor-pointer dark:text-white text-accents-deep'
                        onClick={editProfileButtonClick}
                    >
                        <UserPen className='w-full h-full' aria-hidden strokeWidth={1.5}/>
                    </button>
                </figure>

                {/* User Details */}
                <section className='flex flex-col items-center md:items-start gap-4 font-semibold'>
                    
                    {/* Username */}
                    <h3 className="text-accents-primary text-base sm:text-lg md:text-xl">
                        @{props.username}
                    </h3>

                    {/* Stats Row */}
                    <div 
                        className='flex gap-5 text-black dark:text-white' 
                        role="group" 
                        aria-label="User Statistics"
                    >
                        {/* Followers / Following */}
                        <div className='flex gap-4'>
                            <span className={followsAndPostCountStyle} aria-label={`${props.follower_count} Followers`}>
                                Followers
                                <span className={followsAndPostCountStyle} aria-hidden="true">{` ${props.follower_count}`}</span>
                            </span>
                            
                            <span className={followsAndPostCountStyle} aria-label={`${props.following_count} Following`}>
                                Following
                                <span className={followsAndPostCountStyle} aria-hidden="true">{` ${props.following_count}`}</span>
                            </span>
                        </div>

                        {/* Posts / Visits */}
                        <div className='flex gap-4 pl-4 border-black dark:border-white border-l-2'>
                            <span className={followsAndPostCountStyle} aria-label={`${props.follower_count} Posts`}>
                                Posts
                                <span className={followsAndPostCountStyle} aria-hidden="true">{` ${props.follower_count}`}</span>
                            </span> 
                            
                            <span className={followsAndPostCountStyle} aria-label={`${props.following_count} Visits`}>
                                Visits
                                <span className={followsAndPostCountStyle} aria-hidden="true">{` ${props.following_count}`}</span>
                            </span>
                        </div>
                    </div>
                </section>
                <button 
                    className='right-1 z-10 absolute hover:bg-accents-primary/5 dark:hover:bg-white/10 hover:backdrop-blur-sm px-6 py-2 border border-accents-deep/30 dark:border-white/20 rounded-full font-bold text-accents-deep dark:text-white text-sm transition-colors hover:cursor-pointer hidden lg:flex' 
                    onClick={editProfileButtonClick}
                >
                    Edit Profile
                </button>
            </section>

            {/* Bio */}
            {props.bio ? (
                <div 
                    className='my-4 px-4 max-w-2xl text-[10px] text-slate dark:text-white md:text-xs break-all text-wrap'
                    aria-label="User Biography"
                >
                    <p>{props.bio}</p>
                </div>
            ) : null}

            {/* Social Links */}
            <ProfileLinks
                instagram={props.instagram}
                tiktok={props.tiktok}
                twitter_x={props.twitter_x}
                facebook={props.facebook}
            />
            
            {/* Badges */}
            <ProfileBadges/>
        </div>
    </section>
  )
}
