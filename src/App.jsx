import "./App.css";
import Grid from "./components/Grid"
import MatrixRainEffect from "./components/MatrixRainEffect";

function App() {
  return (
    <>
    <Grid />
    <div className="absolute opacity-[40%] h-100 top-0 z-[-1]">
      <MatrixRainEffect />
    </div>
    <div className="absolute bottom-0 right-0 w-30 h-10 flex items-center justify-center text-xs">
      Made by Kevin Immanuel
    </div>
  </>
  );
}

export default App;
