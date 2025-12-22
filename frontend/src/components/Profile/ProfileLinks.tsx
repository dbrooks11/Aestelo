import {type JSX} from 'react'

type ProfileLinksParams = {
    instagram: string | undefined,
    tiktok: string | undefined,
    twitter_x: string | undefined,
    facebook: string | undefined,
}

const profileLinksStyle = "hover:text-accents-deep dark:hover:text-accents-primary p-1 hover:shadow-sm rounded-full hover:bg-bg-light-secondary/50 dark:hover:dark:bg-accents-primary/10"

export default function ProfileLinks(props: ProfileLinksParams): JSX.Element {
  return (
    // Profile Links Section
    <section className='flex px-4 text-xs gap-4 text-accents-primary z-10 mb-4' aria-label='Social Media Links'>
        {/* Instagram */}
        {props.instagram ? <a className={profileLinksStyle} target='_blank' rel='noopener noreferrer' aria-label='instagram' href={props.instagram ? props.instagram : undefined}>{props.instagram.split('.').slice(1).join('.')}</a>: null}

        {/* Tiktok */}
        {props.tiktok ? <a className={profileLinksStyle} target='_blank' rel='noopener noreferrer' aria-label='tiktok' href={props.tiktok ? props.tiktok : undefined}>{props.tiktok.split('?')[0].split('.').slice(1).join('.')}</a> :null}

        {/* Twitter/X */}
        {props.twitter_x ? <a className={profileLinksStyle} target='_blank' rel='noopener noreferrer' aria-label='twitter or x' href={props.twitter_x ? props.twitter_x : undefined}>{props.twitter_x}</a>: null}

        {/* Facebook */}
        {props.facebook ? <a className={profileLinksStyle} target='_blank' rel='noopener noreferrer' aria-label='facebook' href={props.facebook ? props.facebook : undefined}>{props.facebook}</a>: null}
    </section>
  )
}
