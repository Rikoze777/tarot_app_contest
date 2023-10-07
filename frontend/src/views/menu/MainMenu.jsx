import MainMenuItem from "../../components/MainMenuItem";

function MainMenu() {
  return (
    <div className="p-8 bg-slate-50 absolute min-h-full min-w-full">
      <div className="container">
        <MainMenuItem type='daily' />
        <MainMenuItem type='love' />
        <MainMenuItem type='finance' />
        <MainMenuItem type='advice' />
        <MainMenuItem type='yes_or_no' />
      </div>
    </div>
  );
}

export default MainMenu;
