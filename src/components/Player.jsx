import { useEffect, useState } from "react";
import useSound from "use-sound";
import Aarena from "../assets/Aarena.mp3";
import { AiFillPlayCircle, AiFillPauseCircle } from "react-icons/ai";
import { BiSkipNext, BiSkipPrevious } from "react-icons/bi";
import { IconContext } from "react-icons";

export default function Player() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [time, setTime] = useState({
    min: "3",
    sec: "27",
  });
  const [currTime, setCurrTime] = useState({
    min: "",
    sec: "",
  });

  const [seconds, setSeconds] = useState();

  const [play, { pause, duration, sound }] = useSound(Aarena);

  useEffect(() => {
    if (duration) {
      const sec = duration / 1000;
      const min = Math.floor(sec / 60);
      const secRemain = Math.floor(sec % 60);
      setTime({
        min: min,
        sec: secRemain,
      });
    }
  }, [isPlaying]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (sound) {
        setSeconds(sound.seek([]));
        const min = Math.floor(sound.seek([]) / 60);
        const sec = Math.floor(sound.seek([]) % 60);
        setCurrTime({
          min,
          sec,
        });
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [sound]);

  const playingButton = () => {
    if (isPlaying) {
      pause();
      setIsPlaying(false);
    } else {
      play();
      setIsPlaying(true);
    }
  };

  return (
    <div className="grid grid-cols-1 grid-rows-5">
      <h3 className="row-span-1">Aarena(Knock2 remix)</h3>
      <p className="row-span-1">ISOxo, Knock2</p>
      <div className="w-full grid grid-cols-7 items-center row-span-1">
        <p className="col-span-1 flex justify-center items-center">
          {currTime.min}:{currTime.sec}
        </p>
        <div className="col-span-5 flex justify-center items-center">
          <input
            type="range"
            min="0"
            max={duration / 1000}
            default="0"
            value={seconds}
            onChange={(e) => {
              sound.seek([e.target.value]);
            }}
          />
        </div>
        <p className="col-span-1 flex justify-center items-center">
          {time.min}:{time.sec}
        </p>
      </div>
      <div className="flex row-span-1">
        <button className="playButton">
          <IconContext.Provider value={{ size: "5px", color: "#00ff00" }}>
            <BiSkipPrevious />
          </IconContext.Provider>
        </button>
        {!isPlaying ? (
          <button className="playButton" onClick={playingButton}>
            <IconContext.Provider value={{ size: "5px", color: "#00ff00" }}>
              <AiFillPlayCircle />
            </IconContext.Provider>
          </button>
        ) : (
          <button className="playButton" onClick={playingButton}>
            <IconContext.Provider value={{ size: "3em", color: "#00ff00" }}>
              <AiFillPauseCircle />
            </IconContext.Provider>
          </button>
        )}
        <button className="playButton">
          <IconContext.Provider value={{ size: "3em", color: "#00ff00" }}>
            <BiSkipNext />
          </IconContext.Provider>
        </button>
      </div>
    </div>
  );
}
