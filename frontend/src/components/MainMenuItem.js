import { ChevronRightIcon } from '@heroicons/react/24/solid'

function getStateByType(type) {
  let image, title, description
  switch (type) {
    case 'daily':
      image = "ic_daily.png"
      title = "Daily"
      description = "Get daily advice"
      break;
    case 'love':
      image = "ic_love.png"
      title = "Love"
      description = "Get relationship advice"
      break;
    case 'finance':
      image = "ic_finance.png"
      title = "Finance"
      description = "Get financial advice"
      break;
    case 'advice':
      image = "ic_advice.png"
      title = "Question"
      description = "Get advice on any issue you are interested in"
      break;
    case 'yes_or_no':
      image = "ic_yes_or_no.png"
      title = "Yes or No"
      description = "Get positive or negative advice on an issue of interest"
      break;
    default:
      break;
  }
  return {
    image: image,
    title: title,
    description: description
  }
}

function MainMenuItem(props) {
  let state = getStateByType(props.type)
  let imageUrl = process.env.PUBLIC_URL + '/img/' + state.image
  return (
    <div className="flex flex-row justify-items-center items-center p-4 rounded-3xl gap-8 active:bg-sky-100">
      <img className="h-12 w-12 flex-none" src={imageUrl}/>
      <div className="flex-auto">
        <p className='font-sans text-2xl font-bold'>{state.title}</p>
        <p className='font-sans text-xl mt-0.5 font-light text-gray-400'>{state.description}</p>
      </div>
      <ChevronRightIcon className="h-4 w-4 flex-none shrink-0"/>
    </div>
  )
}

export default MainMenuItem;