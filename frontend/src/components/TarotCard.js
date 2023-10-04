import React from 'react';
import './modules/tarot.css'

function TarotCard(props) {
  const [isRotated, setIsRotated] = React.useState(false);

  const onRotate = () => setIsRotated((rotated) => !rotated);
  let backImage = process.env.PUBLIC_URL + '/img/ic_card_back.png'
  let frontImage = process.env.PUBLIC_URL + '/img/maket1.png'
  return (
    <div className={`card ${isRotated ? 'rotated' : ''} mx-auto w-48 h-[19.68rem] mt-8`} onClick={onRotate}>
        <img src={backImage} className="front w-48 h-[19.68rem] shadow-lg object-cover rounded-3xl" />
        <img src={frontImage} className="back w-48 h-[19.68rem] shadow-lg object-cover rounded-3xl" />
    </div>
  )
}

export default TarotCard;