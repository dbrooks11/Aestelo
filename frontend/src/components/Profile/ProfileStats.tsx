import {type JSX} from 'react'

type ProfileStatsParams = {
    post_count: number | undefined,
    visit_count: number | undefined
}

export default function ProfileStats({post_count, visit_count}: ProfileStatsParams): JSX.Element {
  return (
    <section>
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
