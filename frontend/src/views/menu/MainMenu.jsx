import { useEffect, useState } from "react";
import Loader from "../../components/Loader";
import MainMenuItem from "../../components/MainMenuItem";
import { apiInvoiceUrl, apiUserUrl, getConfig } from "../../utils/api";
import { useStore } from "../../utils/reactive";
import axios from "axios";
import { useWebApp } from "@twa.js/sdk-react";

function MainMenu() {
  const [apiUser, setApiUser] = useStore('api_user');
  const [isLoading, setIsLoading] = useState(apiUser == null)
  const [showModal, setShowModal] = useStore('show_subscription');
  const webApp = useWebApp();

  useEffect(() => {
    if (apiUser == null) {
      axios.get(apiUserUrl, getConfig()).then((resp) => {
        console.log(resp.data);
        setApiUser(resp.data);
      }).finally(setIsLoading(false));
    }
  }, []);

  const requestInvoice = () => {
    setIsLoading(true);
    axios.post(apiInvoiceUrl, null, getConfig()).then((resp) => {
      let invoice_link = resp.data.invoice_link
      console.log(invoice_link);
      webApp.openInvoice(invoice_link)
        .then(setIsLoading(false))
        .catch((reason) => {
          console.log(reason);
          setIsLoading(false);
        })
    }).catch(() => {
      setIsLoading(false);
    }).finally(setShowModal(false));
  }

  if (isLoading) {
    return (<Loader />)
  } else {
    let userSubscribed
    if (apiUser) {
      userSubscribed = apiUser.level == "L1"
    } else {
      userSubscribed = false
    }
    return (
      <div className="p-8 bg-slate-50 absolute min-h-full min-w-full">
        <div className="container">
          <MainMenuItem type='daily' isUnlocked={true} />
          <MainMenuItem type='love' isUnlocked={userSubscribed} />
          <MainMenuItem type='finance' isUnlocked={userSubscribed} />
          <MainMenuItem type='advice' isUnlocked={userSubscribed} />
          <MainMenuItem type='yes_or_no' isUnlocked={userSubscribed} />
        </div>
        {showModal ? (
          <>
            <div
              className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none"
            >
              <div className="relative w-auto my-6 mx-auto max-w-3xl">
                {/*content*/}
                <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                  {/*header*/}
                  <div className="flex items-start justify-between p-5 border-b border-solid border-blueGray-200 rounded-t">
                    <h3 className="text-3xl font-semibold">
                      Oops! Not enough subscription level.
                    </h3>
                    <button
                      className="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                      onClick={() => setShowModal(false)}
                    >
                      <span className="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">
                        ×
                      </span>
                    </button>
                  </div>
                  {/*body*/}
                  <div className="relative p-6 flex-auto">
                    <p className="my-4 text-blueGray-500 text-lg leading-relaxed">
                      This section is under Premium level. Want to subscribe now?
                    </p>
                  </div>
                  {/*footer*/}
                  <div className="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
                    <button
                      className="text-indigo-600 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                      type="button"
                      onClick={() => setShowModal(false)}
                    >
                      Close
                    </button>
                    <button
                      className="bg-indigo-500 text-white active:bg-indigo-600 font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                      type="button"
                      onClick={requestInvoice}
                    >
                      Apply
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
          </>
        ) : null}
      </div>
    );
  }
}

export default MainMenu;
