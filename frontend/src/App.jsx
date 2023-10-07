import {
  BrowserRouter as Router,
  Routes,
  Route,
  Outlet,
  useLocation,
  Navigate
} from "react-router-dom";
import { motion } from "framer-motion";
import MainMenu from "./views/menu/MainMenu";
import Poll from "./views/poll/Poll";

const PageLayout = ({ children }) => children;

const pageVariants = {
  initial: {
    opacity: 0
  },
  in: {
    opacity: 1
  },
  out: {
    opacity: 0
  }
};

const pageTransition = {
  type: "tween",
  ease: "linear",
  duration: 0.5
};

const AnimationLayout = () => {
  const { pathname } = useLocation();
  return (
    <PageLayout>
      <motion.div
        key={pathname}
        initial="initial"
        animate="in"
        variants={pageVariants}
        transition={pageTransition}
      >
        <Outlet />
      </motion.div>
    </PageLayout>
  );
};

export default function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AnimationLayout />}>
          <Route path="/menu" element={<MainMenu />} />
          <Route path="/poll" element={<Poll />} />
          <Route path="*" element={<Navigate to="/menu" replace />} />
        </Route>
      </Routes>
    </Router>
  )
}