import React, { type CSSProperties, type ElementType, type JSX } from 'react'
import { handleNumStats } from '../../util/StatConverter'
import { type ButtonType } from './PostTypeActionButtons';

type ActionButtonProps = {
  title: ButtonType['title']
  icon: ElementType | undefined
  data: ButtonType['data']
  color: ButtonType['color']
  fillColor?: ButtonType['fillColor']
  onClick?: (e: React.MouseEvent) => void
  isActive?: boolean
  className?: string 
}

export default function ButtonBase({
    title,
    icon: Icon,
    data,
    color,
    fillColor,
    onClick,
    isActive = false
}: ActionButtonProps): JSX.Element {
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