import { XMarkIcon } from "@heroicons/react/24/solid";
import TarotCard from "../../components/TarotCard";
import { useNavigate, useParams } from "react-router-dom";
import { getPredictionInfo } from "../../utils/predictions";
import { useEffect, useState } from "react";
import { useStore } from "../../utils/reactive";
import { apiPredictionUrl, getConfig } from "../../utils/api";
import axios from "axios";
import Loader from "../../components/Loader";

function Poll() {
  let { type } = useParams();
  let navigate = useNavigate(); 
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
      <div className="p-4 bg-indigo-50 absolute min-h-full">
        <div className="p-4 shadow-xl bg-white rounded-2xl">
          <div className="flex items-center">
            <h2 className="ml-12 text-2xl text-center font-bold flex-auto">{state.title}</h2>
            <XMarkIcon className="w-12 h-12 p-2 bg-indigo-50 rounded-full" onClick={routeChange}/>
          </div>
          <TarotCard image={prediction.image} />
          <p className="text-l mt-12 first-letter:font-bold first-letter:text-xl font-serif">
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