
import {useState, type JSX} from 'react'
import { type ProfileData, type ProfileDataUseState } from '../../pages/ProfilePage'
import ProfileLinks from './ProfileLinks'
import ProfileBadges from './ProfileBadges'


type BaseProfileInfoParams = Pick<ProfileData, 'username' | 'profile_photo' | 'bio' 
                                            | 'following_count' | 'follower_count'
                                            | 'post_count' | 'visit_count' | 'instagram'
                                            | 'tiktok' | 'twitter_x' | 'facebook'>

type ProfileInfoParams = BaseProfileInfoParams & {
    setProfileData: (profile: ProfileData | null) => void
    profileData: ProfileDataUseState
}


const followsAndPostCountStyle = "font-normal text-[11px] sm:text-sm md:text-base"

export default function ProfileInfo(props: ProfileInfoParams):JSX.Element {

  return (
    <section className='relative mt-50 md:mt-60 w-full z-10  justify-items-center'>
        <div className='flex flex-col z-10 pb-8 border-b border-b-neutral-300 dark:border-b-neutral-800 w-5/6'>
            <section className='flex flex-col md:flex-row items-center gap-6 px-4'>
                <div className='min-w-35 min-h-35'>
                    <img className="w-35 h-35 rounded-full object-cover pointer-events-none" src={props.profile_photo} alt="User's Profile Picture"></img>
                </div>
                <section className='flex flex-col gap-4 items-center md:items-start font-semibold'>
                    <h3 className="text-accents-primary text-sm sm:text-lg md:text-xl" role = 'username' aria-label="username">@{props.username}</h3>
                    <div className='flex gap-5 dark:text-white text-black'>
                        <section className='flex gap-4'>
                            <span className={followsAndPostCountStyle}>Followers<span className={followsAndPostCountStyle}>{` ${props.follower_count}`}</span></span>
                            <span className={followsAndPostCountStyle}>Following<span className={followsAndPostCountStyle}>{` ${props.following_count}`}</span></span>
                        </section>
                        <section className='flex gap-4 border-l-2 border-black dark:border-white pl-4'>
                            <span className={followsAndPostCountStyle}>Posts<span className={followsAndPostCountStyle}>{` ${props.follower_count}`}</span></span> 
                            <span className={followsAndPostCountStyle}>Visits<span className={followsAndPostCountStyle}>{` ${props.following_count}`}</span></span>
                        </section>
                    </div>
                </section>
            </section>
            {props.bio ? <div aria-label='Bio' className='px-4 my-4 text-wrap break-all text-slate dark:text-white max-w-2xl text-[10px] md:text-xs'>
                <p role='bio' >
                    {props.bio}
                </p>
            </div>:null}
            <ProfileLinks
                instagram={props.instagram}
                tiktok = {props.tiktok}
                twitter_x={props.twitter_x}
                facebook={props.facebook}
            />
            <ProfileBadges/>
        </div>
    </section>
  )
}
