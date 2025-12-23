
import type {JSX} from 'react'

export default function ProfileBanner({myProfilePic}: {myProfilePic: string}): JSX.Element {
  return (
    <div className='absolute z-10 w-full pointer-events-none h-94 md:h-100 lg:h-98'>
      <img src={myProfilePic} className='mask-b-from-75% mask-b-to-99% md:mask-b-from-70% md:mask-b-to-95% object-cover w-full h-full'></img>
    </div>
  )
}
