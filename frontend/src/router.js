import {
    createBrowserRouter,
    createRoutesFromElements,
    Route,
  } from "react-router-dom";
  import App from './screen/app/App';

export const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<App />}>
        {/* <Route path="dashboard" element={<Dashboard />} /> */}
        
      </Route>
    )
  );