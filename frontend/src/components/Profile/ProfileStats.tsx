import {type JSX} from 'react'
import { type ProfileDataType } from '../../pages/ProfilePage'

type ProfileStatsParams = {
    post_count: ProfileDataType['post_count'],
    visit_count: ProfileDataType['visit_count']
}

export default function ProfileStats({post_count, visit_count}: ProfileStatsParams): JSX.Element {
  return (
    <section className='z-10'>
        <div>
            <span>📍 Posts</span>
            <span>{post_count}</span>  
        </div>
        <div>
            <span>📸 Visits</span>
            <span>{visit_count}</span>  
        </div>
        <div>
            <span> </span>
            <span>47</span>  
        </div>

    </section>
  )
}
