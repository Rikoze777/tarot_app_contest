import MainMenuItem from "../../components/MainMenuItem";

function App() {
  return (
    <div className="container mt-8">
      <MainMenuItem type='daily'/>
      <MainMenuItem type='love'/>
      <MainMenuItem type='finance'/>
      <MainMenuItem type='advice'/>
      <MainMenuItem type='yes_or_no'/>
    </div>

  );
}

export default App;
