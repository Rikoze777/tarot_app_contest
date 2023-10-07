import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { SDKProvider } from '@twa.js/sdk-react';
import App from './App';
import WebAppLoader from './components/WebAppLoader';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <SDKProvider>
      <WebAppLoader>
        <App />
      </WebAppLoader>
    </SDKProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();