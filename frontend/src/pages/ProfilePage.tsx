
import {useEffect, type JSX, useState} from 'react'
import { protectedInstance } from '../util/axios_api_helpers'
import ProfileHeader from '../components/Profile/ProfileHeader'
import ProfileBanner from '../components/Profile/ProfileBanner'
import ProfileInfo from '../components/Profile/ProfileInfo'
import ProfileTabs from '../components/Profile/ProfileTabs'
import myProfilePic from '../assets/my_profile_pic.jpg'
import defaultProfilePic from "../assets/default_profile_pic.png"
import type { AxiosResponse } from 'axios'

export type ProfileData = {
  id: string,
  profile_photo: string,
  username: string,
  banner_theme: string,
  bio: string,
  instagram: string | undefined,
  tiktok: string | undefined,
  twitter_x: string | undefined,
  facebook: string | undefined,

  is_verified_instagram: boolean,
  is_verified_tiktok: boolean,
  is_verified_twitter_x: boolean,
  is_verified_facebook: boolean,
  
  is_business_account: boolean,
  is_prem_account: boolean,
  show_online_status: boolean,
  is_private: boolean,

  follower_count: number,
  following_count: number,
  post_count: number,
  visit_count: number,

  profile_created_at: Date
  
}

export type ProfileDataUseState = ProfileData | null

export default function ProfilePage(): JSX.Element {

  const [profileData, setProfileData] = useState<ProfileDataUseState>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>("")
  const [showForm, setShowForm] = useState<boolean>(false)

  const editProfileButtonClick = () => {
    setShowForm(!showForm)
  }

  useEffect(() => {
    const profile = async () => {
      try{
        const response: AxiosResponse = await protectedInstance.get('/profile/me')
        const data = response.data

        if(response.status === 200){
          setProfileData(data.my_profile)
          setIsLoading(false)
        }

      }catch(error){
        console.log('failed to fetch profile')
        // AxisErrorHelper(error, setError, "Profile")
        
      }
    }

    profile()
  }, []);
    
 

  return (
    <>
      {!isLoading ? <main className='flex flex-col items-center h-full relative'>
        {error ? error : null}
        <ProfileHeader username = {profileData?.username} follower_count={profileData?.follower_count}/>
        <ProfileBanner myProfilePic={myProfilePic}/>
        <ProfileInfo 
          profile_photo={profileData?.profile_photo ? profileData.profile_photo : myProfilePic} //todo: default icon is temporary (remove it since it has liscense)
          follower_count={profileData?.follower_count ? profileData.follower_count : 0}
          following_count={profileData?.following_count ? profileData.following_count : 0}
          username= {profileData?.username ? profileData.username : ''}
          bio = {profileData?.bio ? profileData.bio : "HELLO I AM A FIAMOUS TIKTOKERhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"}
          post_count={profileData?.post_count ? profileData.post_count : 0}
          visit_count={profileData?.visit_count ? profileData.visit_count : 0}
          instagram = {profileData?.instagram ? profileData.instagram : undefined}
          tiktok = {profileData?.tiktok ? profileData.tiktok : undefined}
          twitter_x = {profileData?.twitter_x ? profileData.twitter_x : undefined}
          facebook = {profileData?.facebook ? profileData.facebook : undefined}
          setProfileData = {setProfileData}
          profileData = {profileData}
        />
        <button 
            className='absolute z-10 top-88 right-32 border dark:border-white/20 rounded-full px-6 py-2 hover:cursor-pointer dark:text-white font-bold dark:hover:bg-white/10 hover:bg-accents-primary/5 hover:backdrop-blur-sm text-accents-deep border-accents-deep/30 text-sm transition-colors' 
            onClick={editProfileButtonClick}
            >
              Edit Profile
        </button>
        {showForm ? <form className='absolute z-10 bg-black text-white top-100 right-32'>
          <label htmlFor='username'></label>
          <input type='text' name='username' id='username'></input>
        </form>: null}
        <ProfileTabs/>
      </main>: "Loading Profile..."}
    </>
  )
}
