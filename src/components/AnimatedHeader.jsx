import React from "react";
import { color, motion } from "motion/react";

const AnimatedHeader = () => {
    return (
        <div className="flex content-center">
        <motion.div
          initial={{ x: "0%" }}
          animate={{ x: ["0%", "-200%", "0%"] }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="text-9xl flex flex-shrink-0 pt-[1rem] mr-[22rem]"
        >
          <div className="mx-[2rem]">kevin </div>
          <div className=""> immanuel</div>
        </motion.div>
        <motion.div
          initial={{ x: "0%" }}
          animate={{ x: ["0%", "-200%", "0%"] }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="text-9xl flex flex-shrink-0 pt-[1rem] mr-[22rem]"
        >
          <div className="mx-[2rem]">kevin </div>
          <div className=""> immanuel</div>
        </motion.div>
      </div>
    )
}

export default AnimatedHeader;