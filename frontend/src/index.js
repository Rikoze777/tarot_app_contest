import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { SDKProvider } from '@twa.js/sdk-react';
import { RouterProvider } from "react-router-dom";
import { router } from './router';
import WebAppLoader from './component/WebAppLoader';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <SDKProvider>
      <WebAppLoader>
        <RouterProvider router={router} />
      </WebAppLoader>
    </SDKProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
