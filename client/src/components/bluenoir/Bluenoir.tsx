import { animate, motion, useMotionValue } from "framer-motion";
import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { useGesture } from "react-use-gesture";

import useBPHStore from "@/stores/useBPHStore";
import { cn } from "@/utils/utils";

import BluenoirFrame from "./BluenoirFrame";
import BluenoirSpeech from "./BluenoirSpeech";

export const IDLE_TIMER = 60; // 1 minute

const Bluenoir = () => {
  const speak = useBPHStore((state) => state.bluenoirSpeak);
  const start = useBPHStore((state) => state.startIdleTimer);

  const position = useBPHStore((state) => state.getBluenoirPosition());
  const previousPosition = useBPHStore((state) => state.getPreviousPosition());
  const setPosition = useBPHStore((state) => state.setBluenoirPosition);
  const centered = useBPHStore((state) => state.bluenoirCentered);
  const getNearestSnapPoint = useBPHStore((state) => state.getNearestSnapPoint);

  const x = useMotionValue(position.x);
  const y = useMotionValue(position.y);
  const scale = useMotionValue(1);

  const dragRef = useRef<HTMLDivElement>(null);
  const measureRef = useRef<HTMLDivElement>(null);

  const location = useLocation();

  useEffect(() => {
    start(speak, IDLE_TIMER * 1000);
  });

  useEffect(() => {
    if (measureRef.current) {
      const centeredPositionX = position.x - (measureRef.current.offsetWidth ?? 0) / 2;
      const centeredPositionY = position.y - (measureRef.current.offsetHeight ?? 0) / 2;

      x.set(centeredPositionX);
      y.set(centeredPositionY);
    }
  });

  useEffect(() => {
    const pos = centered ? centered : previousPosition;
    const centeredPositionX =
      pos.x * window.innerWidth - (measureRef.current?.offsetWidth ?? 0) / 2;
    const centeredPositionY =
      pos.y * window.innerHeight - (measureRef.current?.offsetHeight ?? 0) / 2;

    animate(x, centeredPositionX);
    animate(y, centeredPositionY);
    animate(scale, centered ? 2 : 1);
    setPosition(pos);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [centered, setPosition]);

  useGesture(
    {
      onDrag: ({ event, movement: [dx, dy] }) => {
        event.preventDefault();
        x.stop();
        y.stop();

        x.set(dx);
        y.set(dy);
      },
      onDragEnd: () => {
        console.log(location.pathname.includes("final-verdict"));
        const pos = centered
          ? centered
          : getNearestSnapPoint(
              { x: x.get(), y: y.get() },
              location.pathname.includes("final-verdict"),
            );
        const centeredPositionX = pos.x * innerWidth - (measureRef.current?.offsetWidth ?? 0) / 2;
        const centeredPositionY = pos.y * innerHeight - (measureRef.current?.offsetHeight ?? 0) / 2;

        animate(x, centeredPositionX);
        animate(y, centeredPositionY);
        animate(scale, centered ? 2 : 1);
        setPosition(pos);
      },
    },
    {
      drag: { initial: () => [x.get(), y.get()], filterTaps: true },
      domTarget: dragRef,
      eventOptions: { passive: false },
    },
  );

  return (
    <motion.div
      className="fixed z-[100] text-white rounded-lg bg-slate-900 p-3 pr-4 shadow-lg shadow-slate-800"
      style={{
        x,
        y,
        scale,
        touchAction: "none",
        userSelect: "none",
        MozUserSelect: "none",
        WebkitUserSelect: "none",
      }}
    >
      <div ref={dragRef} className={cn("flex items-center select-none")}>
        <BluenoirFrame ref={measureRef} />
        <BluenoirSpeech />
      </div>
    </motion.div>
  );
};

export default Bluenoir;
