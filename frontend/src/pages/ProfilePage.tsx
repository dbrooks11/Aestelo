
import {useEffect, type JSX, useState} from 'react'
import { AxiosErrorHelper, protectedInstance } from '../util/axios_api_helpers'
import DefaultBannerDark from "../assets/default_banner_dark.svg"
import DefaultBannerLight from "../assets/default_banner_light.svg"
import DefaultPhoto from "../assets/default_photo.svg"
import ProfileHeader from '../components/Profile/ProfileHeader'
import ProfileBanner from '../components/Profile/ProfileBanner'
import ProfileInfo from '../components/Profile/ProfileInfo'
import ProfileTabs from '../components/Profile/ProfileTabs'
import EditProfileForm from '../components/Profile/ProfileEditForm'
import type { AxiosResponse } from 'axios'
import Modal from '../components/Modal'
import ToasterCustom from '../components/Toast'
import toast from 'react-hot-toast'
import { useTheme } from '../context/ThemeContext'
import ProfileLoadingSkeleton from '../components/Skeletons/ProfileSkeleton'

export type ProfileDataType = {
  id: string,
  profile_photo_url: string | undefined
  profile_banner_url: string | undefined,
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

export type ProfileDataUseState = ProfileDataType | null


export default function ProfilePage(): JSX.Element {

  const {theme} = useTheme()
  const [profileData, setProfileData] = useState<ProfileDataUseState>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [showModal, setShowModal] = useState<boolean>(false)
  const banner = `${theme === 'light' ? DefaultBannerLight : DefaultBannerDark}`

  

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
        const newError = AxiosErrorHelper(error)
        toast.error(newError, {
          toasterId: 'profile'
        })
        
      }
    }

    profile()
  }, []);

  
  return (
    <>
      {!isLoading ? <main className='relative flex flex-col items-center h-full'>
        <ProfileHeader 
          username = {profileData?.username ? profileData.username : ''} 
          follower_count={profileData?.follower_count ? profileData.follower_count : 0}/>
          
        <ProfileBanner profileBanner={profileData?.profile_banner_url ? profileData.profile_banner_url: banner}/> 
        <ProfileInfo 
          profile_photo_url={profileData?.profile_photo_url ? profileData.profile_photo_url : DefaultPhoto} 
          follower_count={profileData?.follower_count ? profileData.follower_count : 0}
          following_count={profileData?.following_count ? profileData.following_count : 0}
          username= {profileData?.username ? profileData.username : ''}
          bio = {profileData?.bio ? profileData.bio : ""}
          post_count={profileData?.post_count ? profileData.post_count : 0}
          visit_count={profileData?.visit_count ? profileData.visit_count : 0}
          instagram = {profileData?.instagram ? profileData.instagram : undefined}
          tiktok = {profileData?.tiktok ? profileData.tiktok : undefined}
          twitter_x = {profileData?.twitter_x ? profileData.twitter_x : undefined}
          facebook = {profileData?.facebook ? profileData.facebook : undefined}
          setProfileData = {setProfileData}
          profileData = {profileData}
          setShowModal = {setShowModal}
          showModal = {showModal}
        />
        
        <ProfileTabs/>
        <Modal showModal={showModal} closeModal={closeModal} title='Edit Profile'>
          <EditProfileForm
            profile_banner_url={profileData?.profile_banner_url ? profileData.profile_banner_url : banner}
            profile_photo_url={profileData?.profile_photo_url ? profileData.profile_photo_url : DefaultPhoto}  
            username = {profileData?.username ? profileData.username : ""} 
            bio = {profileData?.bio ? profileData.bio : ""}
            setProfileData={setProfileData}
            setShowModal={setShowModal}
          />
        </Modal>
        <ToasterCustom toasterId='profile'/>
      </main>: <ProfileLoadingSkeleton/>}
    </>
  )
}
