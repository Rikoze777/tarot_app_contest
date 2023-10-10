import React from 'react';
import './modules/tarot.css'
import backImage from '../assets/ic_card_back.png'

function TarotCard({image}) {
  const [isRotated, setIsRotated] = React.useState(false);
  const mediaUrl = import.meta.env.VITE_API_BASE_URL

  const onRotate = () => setIsRotated((rotated) => !rotated);
  return (
    <div className={`card ${isRotated ? 'rotated' : ''} mx-auto w-48 h-[19.68rem] mt-8`} onClick={onRotate}>
        <img src={backImage} className="front w-48 h-[19.68rem] shadow-lg object-cover rounded-3xl" />
        <img src={mediaUrl + image} className="back w-48 h-[19.68rem] shadow-lg object-cover rounded-3xl" />
    </div>
  )
}

export default TarotCard;