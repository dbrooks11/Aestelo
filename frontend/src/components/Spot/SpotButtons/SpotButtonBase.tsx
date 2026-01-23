import React, { type CSSProperties, type ElementType, type JSX } from 'react'
import { handleNumStats } from '../../../util/StatConverter'
import { type SpotButtonType } from './SpotButtons';

type SpotActionButtonProps = {
  title: SpotButtonType['title']
  icon: ElementType | undefined
  data: SpotButtonType['data']
  color: SpotButtonType['color']
  fillColor?: SpotButtonType['fillColor']
  onClick?: (e: React.MouseEvent) => void
  isActive?: boolean
  className?: string 
}

export default function SpotButtonBase({
    title,
    icon: Icon,
    data,
    color,
    fillColor,
    onClick,
    isActive = false
}: SpotActionButtonProps): JSX.Element {
  return (
    <button
      title={title}
      onClick={onClick}
      style={{ '--btn-color': color, '--btn-fill-color': fillColor } as CSSProperties}
      className='group relative flex items-center gap-1 hover:dark:text-white hover:text-black transition-colors cursor-pointer select-none'
    >
      {Icon && <Icon
        strokeWidth={1}
        className={`group-hover:stroke-(--btn-color) transition-colors ${
          isActive && fillColor ? 'fill-(--btn-fill-color) stroke-(--btn-color)' : ''
        }`}
      />}
      {data && <span className="font-medium text-xs">{handleNumStats(data)}</span>}
    </button>
  );
};