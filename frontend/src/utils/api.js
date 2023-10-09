import { getStore } from "./reactive";

const apiUserUrl = `${import.meta.env.VITE_API_BASE_URL}/api/user`
const apiPredictionUrl = `${import.meta.env.VITE_API_BASE_URL}/api/prediction`
const apiInvoiceUrl = `${import.meta.env.VITE_API_BASE_URL}/api/invoice`

function getConfig() {
    return {
        headers: {
            Authorization: `${getStore("init_data")}`
        }
    }
}

export {
    getConfig,
    apiUserUrl,
    apiPredictionUrl,
    apiInvoiceUrl
}