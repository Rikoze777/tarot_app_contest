import { XMarkIcon } from "@heroicons/react/24/solid";
import TarotCard from "../../components/TarotCard";
import { useNavigate, useParams } from "react-router-dom";
import { getPredictionInfo } from "../../utils/predictions";
import { useEffect, useState } from "react";
import { useStore } from "../../utils/reactive";
import { apiPredictionUrl, getConfig } from "../../utils/api";
import axios from "axios";
import Loader from "../../components/Loader";
import { useThemeParams } from "@twa.js/sdk-react";

function Poll() {
  let { type } = useParams();
  let navigate = useNavigate(); 
  const themeParams = useThemeParams();
  const [prediction, setPrediction] = useStore(type+"_prediction");
  const [isLoading, setIsLoading] = useState(prediction == null)

  useEffect(() => {
    if (prediction == null) {
      let fullUrl = apiPredictionUrl+"?type="+type
      axios.get(fullUrl, getConfig()).then((resp) => {
        let prediction = resp.data
        console.log(prediction)
        setPrediction(prediction)
      }).finally(setIsLoading(false));
    }
  }, []);

  let state = getPredictionInfo(type)
  const routeChange = () =>{ 
    navigate(-1);
  }

  if (isLoading) {
    return(<Loader />)
  }

  if (prediction) {
    return (
      <div className="p-4 absolute min-h-full" style={{backgroundColor: themeParams.secondaryBackgroundColor}}>
        <div className="p-4 shadow-xl rounded-2xl" style={{backgroundColor: themeParams.backgroundColor}}>
          <div className="flex items-center">
            <h2 className="ml-12 text-2xl text-center font-bold flex-auto" style={{color: themeParams.textColor}}>{state.title}</h2>
            <XMarkIcon className="w-12 h-12 p-2 rounded-full" onClick={routeChange} style={{backgroundColor: themeParams.secondaryBackgroundColor}}/>
          </div>
          <TarotCard image={prediction.image} />
          <p className="text-l mt-12 first-letter:font-bold first-letter:text-xl font-serif" style={{color: themeParams.textColor}}>
            {prediction.prediction}
          </p>
        </div>
      </div>
    )
  } else {
    return(<div>Something went wrong...</div>)
  }
  
}

export default Poll;