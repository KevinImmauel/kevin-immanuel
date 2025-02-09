import { useEffect, useRef } from "react";

export default function Visualizer({ isPlaying, progress }) {
  const canvasRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const dataArrayRef = useRef(null);
  const animationIdRef = useRef(null);

  useEffect(() => {
    if (!isPlaying) {
      cancelAnimationFrame(animationIdRef.current);
      return;
    }

    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }

    // Resume AudioContext if it's suspended
    if (audioContextRef.current.state === "suspended") {
      audioContextRef.current.resume().catch((err) =>
        console.error("AudioContext resume failed:", err)
      );
    }

    if (!analyserRef.current) {
      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 256; // Higher means more detail, but heavier
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);
    }

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    const draw = () => {
      if (!isPlaying) return;
      animationIdRef.current = requestAnimationFrame(draw);

      analyserRef.current.getByteFrequencyData(dataArrayRef.current);

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const barWidth = canvas.width / dataArrayRef.current.length;
      let x = 0;

      for (let i = 0; i < dataArrayRef.current.length; i++) {
        const barHeight = dataArrayRef.current[i] * 1.5;

        ctx.fillStyle = `rgb(${barHeight + 50}, 50, 255)`;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

        // Mirrored effect
        ctx.fillRect(canvas.width - x - barWidth, canvas.height - barHeight, barWidth, barHeight);

        x += barWidth + 1;
      }
    };

    draw();
  }, [isPlaying]);

  return (
    <canvas ref={canvasRef} className="absolute bottom-0 w-full h-64 opacity-80 z-10"></canvas>
  );
}
