import {type JSX} from 'react'
import { Link } from 'react-router-dom'

export default function ProfileTabs(): JSX.Element {
  return (
    <section className='mt-12 flex gap-12'>
        <section>
            <Link to={'/post/:id/profile-post/all'}>Posts</Link>
        </section>
        <section>
            <Link to={'/visit/:id/profile-visit/all'}>Visits</Link>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
            <div>hello</div>
        </section>
    </section>
  )
}
