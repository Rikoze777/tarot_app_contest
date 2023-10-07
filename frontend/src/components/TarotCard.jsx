import React from 'react';
import './modules/tarot.css'
import backImage from '../assets/ic_card_back.png'
import frontImage from '../assets/maket1.png'

function TarotCard(props) {
  const [isRotated, setIsRotated] = React.useState(false);

  const onRotate = () => setIsRotated((rotated) => !rotated);
  return (
    <div className={`card ${isRotated ? 'rotated' : ''} mx-auto w-48 h-[19.68rem] mt-8`} onClick={onRotate}>
        <img src={backImage} className="front w-48 h-[19.68rem] shadow-lg object-cover rounded-3xl" />
        <img src={frontImage} className="back w-48 h-[19.68rem] shadow-lg object-cover rounded-3xl" />
    </div>
  )
}

export default TarotCard;