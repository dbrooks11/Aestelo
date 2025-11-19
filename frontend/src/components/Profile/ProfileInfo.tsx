
import type {JSX} from 'react'
import ProfileLinks from './ProfileLinks'


type ProfileInfoParams = {
    username: string | undefined,
    profile_pic_url: string | undefined,
    bio: string | undefined,
    following_count: number | undefined,
    follower_count: number | undefined,
    post_count: number,
    visit_count: number,
    instagram: string | undefined,
    tiktok: string | undefined,
    twitter_x: string | undefined,
    facebook: string | undefined,
    
}

export default function ProfileInfo(props: ProfileInfoParams):JSX.Element {
  return (
    <section className='flex flex-col items-center justify-center mt-10'>
        <div className='flex flex-col max-w-full'>
            <div className='' aria-hidden>Profile Banner</div>
            <section className='flex items-center gap-6 px-4'>
                <div className='profile_image_wrapper'>
                    <img className="profile_image" src={props.profile_pic_url} alt="User's Profile Picture"></img>
                </div>
                <section className='flex flex-col gap-4'>
                    <h3 className="text-accents-primary" role = 'username' aria-label="username">@{props.username}</h3>
                    <div className='flex gap-5 dark:text-white text-black'>
                        <section className='flex gap-4'>
                            <span className='profile_stats_label'>Followers<span className='profile_stats_info'>{` ${props.follower_count}`}</span></span>
                            <span className='profile_stats_label'>Following<span className='profile_stats_info'>{` ${props.following_count}`}</span></span>
                        </section>
                        <section className='flex gap-4 border-l-2 border-black dark:border-white pl-4'>
                            <span className='profile_stats_label'>Posts<span className='profile_stats_info'>{` ${props.follower_count}`}</span></span> 
                            <span className='profile_stats_label'>Visits<span className='profile_stats_info'>{` ${props.following_count}`}</span></span>
                        </section>
                    </div>
                </section>
            </section>
            {props.bio ? <div aria-label='Bio' className='px-4 my-4 text-wrap break-all text-slate dark:text-white text-xs max-w-2xl'>
            <p role='bio' >
                {props.bio}</p>
            </div>:null}
            <ProfileLinks
                instagram={props.instagram}
                tiktok = {props.tiktok}
                twitter_x={props.twitter_x}
                facebook={props.facebook}
            />
        </div>
    </section>
  )
}
