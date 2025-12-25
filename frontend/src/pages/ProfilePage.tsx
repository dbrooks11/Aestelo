
import {useEffect, type JSX, useState} from 'react'
import { protectedInstance } from '../util/axios_api_helpers'
import cn from '../util/tailwind_merger'
import ProfileHeader from '../components/Profile/ProfileHeader'
import ProfileBanner from '../components/Profile/ProfileBanner'
import ProfileInfo from '../components/Profile/ProfileInfo'
import ProfileTabs from '../components/Profile/ProfileTabs'
import EditProfileForm from '../components/Profile/ProfileEditForm'
import myProfilePic from '../assets/my_profile_pic.jpg'
import defaultProfilePic from "../assets/default_profile_pic.png"
import type { AxiosResponse } from 'axios'
import Modal from '../components/Modal'

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

const editProfileFormDivStyle = ""
const editProfileFormLabelStyle = ""

export default function ProfilePage(): JSX.Element {

  const [profileData, setProfileData] = useState<ProfileDataUseState>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>("")
  const [showModal, setShowModal] = useState<boolean>(false)

  const editProfileButtonClick = () => {
    setShowModal(!showModal)
  }

  const closeModal = () =>{
        setShowModal(false)
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
      {!isLoading ? <main className='relative flex flex-col items-center h-full'>
        {error ? error : null}
        <ProfileHeader username = {profileData?.username} follower_count={profileData?.follower_count}/>
        <ProfileBanner profileBanner={myProfilePic}/>
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
            className='top-88 right-32 z-10 absolute hover:bg-accents-primary/5 dark:hover:bg-white/10 hover:backdrop-blur-sm px-6 py-2 border border-accents-deep/30 dark:border-white/20 rounded-full font-bold text-accents-deep dark:text-white text-sm transition-colors hover:cursor-pointer' 
            onClick={editProfileButtonClick}
            >
              Edit Profile
        </button>
        <ProfileTabs/>
        <Modal showModal={showModal} closeModal={closeModal} title='Edit Profile'>
          <EditProfileForm/>
        </Modal>
        
      </main>: "Loading Profile..."}
    </>
  )
}
