import React from "react";
import TextArt from "./TextArt";
import Player from "./Player";
import AnimatedHeader from "./AnimatedHeader";
import {
  FaGithub,
  FaInstagram,
  FaLinkedinIn,
  FaSpotify,
  FaDiscord,
  FaShare,
} from "react-icons/fa";
import { BiLogoGmail } from "react-icons/bi";

const Grid = () => {
  const technologies = [
    { name: "JavaScript", color: "#FDDC01" },
    { name: "Python", color: "#224B6C" },
    { name: "Node.js", color: "#417F39" },
    { name: "React", color: "#58C4DC" },
    { name: "Flask", color: "#3DAABE" },
    { name: "FastAPI", color: "#009485" },
    { name: "SQL", color: "#F39011" },
    { name: "Flutter", color: "#2676D6" },
    { name: "Dart", color: "#12212E" },
    { name: "Java", color: "#DE080D" },
    { name: "Tailwind CSS", color: "#01BCFE" },
    { name: "Linux", color: "#4485C4" },
    { name: "Git", color: "#F44D26" },
    { name: "Svelte", color: "#F8663D" },
    { name: "HTML", color: "#E34F26" },
    { name: "CSS", color: "#264DE4" },
    { name: "Go", color: "#6AD7E5" },
    { name: "R", color: "#9F9FA5" },
    { name: "C", color: "#6A9DD3" },
  ];

  const gen = () => {
    return Math.floor(Math.random() * 90);
  };

  return (
    <div className=" xl:grid xl:grid-cols-8 xl:grid-rows-10 gap-0 opacity-100 z-10">
      <div className="xl:row-span-2 xl:col-span-3 overflow-hidden">
        <AnimatedHeader />
      </div>
      <div className="xl:row-span-6 xl:col-span-5 leading-tight">
        <TextArt />
      </div>
      <div className="xl:row-span-1 xl:col-span-3 flex flex-col justify-center">
        <p className="text-2xl">About Me</p>
        <p>
          A 19-year-old kid trying to survive keeping his love for computers
          alive.
        </p>
      </div>
      <div className="xl:row-span-2 xl:col-span-3 flex">
        <img className="h-[10rem] w-[10rem]" src="image.png" alt="im" />
        <Player />
      </div>
      <div className="xl:row-span-3 xl:col-span-5">
        What do I usually use? <br />
        <p className="relative w-full">
          {technologies.map((tech) => (
            <span
              className="size-16"
              key={tech.name}
              style={{
                color: tech.color,
                position: "absolute",
                top: `${gen()}%`,
                left: `${gen()}%`,
              }}
            >
              {tech.name}
            </span>
          ))}
        </p>
      </div>
      <div className="row-span-2 col-span-3 flex flex-col">
        <div className="flex justify-around items-center">
          <FaGithub className="size-8" />
        <FaInstagram className="size-8" />
        <FaLinkedinIn className="size-8" />
        </div>
        <div className="flex justify-around items-center">
        <FaSpotify className="size-8" />
        <BiLogoGmail className="size-8" />
        <FaDiscord className="size-8" />
        </div>
      </div>
    </div>
  );
};

export default Grid;
