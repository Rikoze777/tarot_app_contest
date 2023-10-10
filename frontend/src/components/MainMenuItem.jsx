import { ChevronRightIcon } from '@heroicons/react/24/solid'
import { useNavigate } from 'react-router-dom'
import { useStore } from '../utils/reactive'
import { getPredictionInfo } from '../utils/predictions';
import { useThemeParams } from '@twa.js/sdk-react';

function MainMenuItem(props) {
  const navigate = useNavigate();
  const themeParams = useThemeParams();
  const [, setShowSubscription] = useStore('show_subscription');
  let state = getPredictionInfo(props.type)
  let imageUrl = 'img/' + state.image
  const onCLick = () => {
    if (props.isUnlocked) {
      let path = `/poll/${props.type}`;
      navigate(path);
    } else {
      setShowSubscription(true)
    }
  }
  return (
    <div className="flex mt-8 flex-row justify-items-center items-center p-4 rounded-3xl gap-8 active:bg-indigo-50" onClick={onCLick} style={{backgroundColor: themeParams.backgroundColor}}>
      <img className="h-12 w-12 flex-none" src={imageUrl}/>
      <div className="flex-auto">
        <p className='font-sans text-2xl font-bold' style={{color: themeParams.textColor}}>{state.title}</p>
        <p className='font-sans text-xl mt-0.5 font-light text-gray-400'>{state.description}</p>
      </div>
      <ChevronRightIcon className="h-4 w-4 flex-none shrink-0"/>
    </div>
  )
}

export default MainMenuItem;