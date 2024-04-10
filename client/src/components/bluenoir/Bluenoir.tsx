import {
  AnimatePresence,
  animate,
  motion,
  useMotionValue,
  useMotionValueEvent,
  type Variants,
} from "framer-motion";
import { forwardRef, useCallback, useEffect, useRef, useState } from "react";
import { useGesture } from "react-use-gesture";
import Typewriter from "typewriter-effect";

import frame from "@/assets/bluenoir/frame.png";
import frame_bg from "@/assets/bluenoir/frame_bg.png";
import useBPHStore from "@/stores/useBPHStore";
import { BluenoirReactionImage } from "@/utils/bluenoir_dialogue";
import { cn } from "@/utils/utils";

import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../ui/tooltip";

const BluenoirFrame = forwardRef<HTMLDivElement>((_props, ref) => {
  const open = useBPHStore((state) => state.bluenoirOpen);
  const toggleOpen = useBPHStore((state) => state.toggleBluenoirOpen);
  const speechDialogue = useBPHStore((state) => state.bluenoirDialogue);

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>
          <div ref={ref} className="cursor-pointer h-[80px] w-[80px]">
            <div className="h-[55px] w-[55px] absolute mx-[12px] my-[12px]">
              <img
                className="select-none"
                src={BluenoirReactionImage[speechDialogue.reaction]}
                style={{
                  backgroundImage: `url(${frame_bg})`,
                }}
              />
            </div>
            <div
              onDoubleClick={toggleOpen}
              className="h-[100px] w-[100px] absolute mx-auto my-auto"
            >
              <img className="select-none" src={frame} />
            </div>
          </div>
        </TooltipTrigger>
        {!open && (
          <TooltipContent className="bg-slate-900 text-white border-none">
            <p>Double Click Me!</p>
          </TooltipContent>
        )}
      </Tooltip>
    </TooltipProvider>
  );
});
BluenoirFrame.displayName = "BluenoirFrame";

const frameSlideInOut = 0.15;
const textFadeInOut = 0.25;
const totalAnimationTime = frameSlideInOut + textFadeInOut;

const frameVariants: Variants = {
  visible: {
    width: "auto",
    transition: { duration: frameSlideInOut },
  },
  hidden: {
    width: 0,
    transition: { duration: frameSlideInOut, delay: textFadeInOut },
  },
};

const textVariants: Variants = {
  visible: {
    opacity: 1,
    height: "auto",
    transition: { duration: textFadeInOut, delay: frameSlideInOut },
  },
  hidden: {
    opacity: 0,
    height: 0,
    transition: { duration: textFadeInOut },
  },
};

interface BluenoirSpeechProps {
  isLeft: boolean;
}

const BluenoirSpeech = ({ isLeft }: BluenoirSpeechProps) => {
  const open = useBPHStore((state) => state.bluenoirOpen);
  const setOpen = useBPHStore((state) => state.setBluenoirOpen);
  const speechDialogue = useBPHStore((state) => state.bluenoirDialogue);
  const speak = useBPHStore((state) => state.bluenoirSpeak);

  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const speechTimeout = useCallback(
    () =>
      setTimeout(() => {
        speak(undefined, true);
        console.log("timeout!");
        timeoutRef.current = speechTimeout();
      }, 5000),
    [speak],
  );

  useEffect(() => {
    timeoutRef.current = setTimeout(() => {
      speechTimeout();
    }, 5000);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  });

  useEffect(() => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    if (open) {
      timeoutRef.current = speechTimeout();
    }

    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [open, speechTimeout]);

  return (
    <motion.div
      className="flex flex-col"
      variants={frameVariants}
      initial={false}
      animate={open ? "visible" : "hidden"}
    >
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            className="px-4"
            variants={textVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
          >
            <div
              className={cn("absolute text-slate-500 text-sm top-1", isLeft ? "right-2" : "left-2")}
            >
              <button
                onClick={() => {
                  setOpen(false);
                  if (timeoutRef.current) clearTimeout(timeoutRef.current);
                  timeoutRef.current = speechTimeout();
                }}
              >
                ✕
              </button>
            </div>
            <div
              className={cn(
                "font-extrabold font-mono text-sm underline underline-offset-2",
                !isLeft && "text-right",
              )}
            >
              Bluenoir
            </div>
            <div className="grid font-mono font-light max-w-xs text-xs">
              <p className="text-slate-900 col-start-1 row-start-1">{speechDialogue.text}</p>
              <div className="w-full col-start-1 row-start-1" key={speechDialogue.text}>
                <Typewriter
                  onInit={(typewriter) => {
                    typewriter
                      .pauseFor(totalAnimationTime * 1000)
                      .typeString(speechDialogue.text)
                      .start();
                  }}
                  options={{
                    cursor: "",
                    delay: 30,
                  }}
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

const Bluenoir = () => {
  const position = useBPHStore((state) => state.getBluenoirPosition());
  const setPosition = useBPHStore((state) => state.setBluenoirPosition);
  const getNearestSnapPoint = useBPHStore((state) => state.getNearestSnapPoint);
  const dragRef = useRef<HTMLDivElement>(null);
  const measureRef = useRef<HTMLDivElement>(null);

  const x = useMotionValue(position.x);
  const y = useMotionValue(position.y);

  const [isLeft, setIsLeft] = useState(
    x.get() < (window.innerWidth - (measureRef.current?.offsetWidth ?? 0)) / 2,
  );

  useEffect(() => {
    if (measureRef.current) {
      const centeredPositionX = position.x - (measureRef.current.offsetWidth ?? 0) / 2;
      const centeredPositionY = position.y - (measureRef.current.offsetHeight ?? 0) / 2;

      x.set(centeredPositionX);
      y.set(centeredPositionY);
    }
  });

  useMotionValueEvent(x, "change", (val) => {
    setIsLeft(val < (window.innerWidth - (measureRef.current?.offsetWidth ?? 0)) / 2);
  });

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
        console.log(x.get(), y.get());
        const snapPosition = getNearestSnapPoint({ x: x.get(), y: y.get() });
        const centeredPositionX =
          snapPosition.x * window.innerWidth - (measureRef.current?.offsetWidth ?? 0) / 2;
        const centeredPositionY =
          snapPosition.y * window.innerHeight - (measureRef.current?.offsetHeight ?? 0) / 2;

        console.log(centeredPositionX, centeredPositionY);

        animate(x, centeredPositionX);
        animate(y, centeredPositionY);
        setPosition(snapPosition);
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
      className="fixed z-[50] text-white rounded-lg bg-slate-900 p-3 pr-4 shadow-lg shadow-slate-800"
      style={{
        x,
        y,
        touchAction: "none",
        userSelect: "none",
        MozUserSelect: "none",
        WebkitUserSelect: "none",
      }}
    >
      <div
        ref={dragRef}
        className={cn("flex items-center select-none", isLeft ? "flex-row" : "flex-row-reverse")}
      >
        <BluenoirFrame ref={measureRef} />
        <BluenoirSpeech isLeft={isLeft} />
      </div>
    </motion.div>
  );
};

export default Bluenoir;
