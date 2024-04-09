import bottle from "@/assets/minor_cases/exile/bottle.png";
import exile_bg from "@/assets/minor_cases/exile/exile_bg.png";
import painting from "@/assets/minor_cases/exile/painting.png";
import victrola from "@/assets/minor_cases/exile/victrola.png";
import wine from "@/assets/minor_cases/exile/wine.png";

import whale_bg from "@/assets/minor_cases/whales/background_whale2.png";
import flowers from "@/assets/minor_cases/whales/flowers.png";
import parrot from "@/assets/minor_cases/whales/parrot.png";
import sheep from "@/assets/minor_cases/whales/sheep.png";
import stool from "@/assets/minor_cases/whales/stool.png";
import waterline from "@/assets/minor_cases/whales/waterline.png";

import { useDjangoContext } from "@/hooks/useDjangoContext";
import { useTheme } from "@/hooks/useTheme";
import { CASE_PALETTE, MajorCaseEnum } from "@/utils/constants";
import { WHALE_THEME } from "@/utils/themes";
import { PuzzleAnswer, cn, getUnlockedPuzzle } from "@/utils/utils";
import { ReactNode, useEffect, useMemo } from "react";
import RelativeAsset, { AssetProps } from "../RelativeAsset";

const ExileArt = () => {
  return (
    <ArtWrapper className="aspect-w-4 aspect-h-3 max-w-screen-xl" background_src={exile_bg}>
      <PuzzleIconWrapper
        slug="still-at-the-restaurant"
        imageSrc={painting}
        extraStyles={{
          top: "14%",
          left: "41%",
          width: "13%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="ocean-wave-blues"
        imageSrc={bottle}
        extraStyles={{
          top: "21%",
          left: "82%",
          width: "13%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="illicit-affairs"
        imageSrc={wine}
        extraStyles={{
          top: "35%",
          left: "7.5%",
          width: "8.5%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="the-day-he-died"
        imageSrc={victrola}
        extraStyles={{
          top: "33%",
          left: "64%",
          width: "10%",
          zIndex: 3,
        }}
        meta
      />
    </ArtWrapper>
  );
};

const WhaleArt = () => {
  const { setTheme } = useTheme();
  useEffect(() => {
    setTheme(WHALE_THEME);
  });

  return (
    <ArtWrapper className="" background_src={whale_bg}>
      <PuzzleIconWrapper
        slug="underwater-flora"
        imageSrc={flowers}
        extraStyles={{
          top: "40%",
          left: "63%",
          width: "10%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="waterlines"
        imageSrc={waterline}
        extraStyles={{
          top: "20%",
          left: "42%",
          width: "13%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="shoot"
        imageSrc={parrot}
        extraStyles={{
          top: "19%",
          left: "35%",
          width: "7%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="back-in-wales"
        imageSrc={sheep}
        extraStyles={{
          top: "25%",
          left: "59%",
          width: "13%",
          zIndex: 3,
        }}
      />
      <PuzzleIconWrapper
        slug="whelp"
        imageSrc={stool}
        extraStyles={{
          top: "42%",
          left: "46%",
          width: "14%",
          zIndex: 3,
        }}
      />
    </ArtWrapper>
  );
};

interface PuzzleAsset extends AssetProps {
  slug: string;
  meta?: boolean;
}

const PuzzleIconWrapper = (props: PuzzleAsset) => {
  const { context } = useDjangoContext();
  const { slug } = props;

  const puzzle_answer: PuzzleAnswer | null = useMemo(() => {
    const case_slug = window.location.pathname.split("/").pop();
    if (!context?.team_context || !case_slug) {
      return null;
    }
    return getUnlockedPuzzle(slug, context, case_slug);
  }, [context, slug]);

  return (
    <>
      {puzzle_answer && (
        <RelativeAsset
          extraClasses={`group hover:cursor-pointer ${!props.hoverImageSrc ? "hover:drop-shadow-[0_15px_15px_rgba(255,255,255,0.2)]" : ""}`}
          {...props}
          linkTo={`/puzzle/${slug}`}
        >
          <p
            className={` p-[0.2rem] font-bold text-center bg-slate-800 group-hover:bg-slate-600 rounded-xl ${props.meta ? "text-[1vw] border-2 border-sky-200" : "text-[0.65vw]"}`}
          >
            {puzzle_answer?.puzzle.name.toUpperCase()}
          </p>
          <p
            className={`answer mt-1 p-[0.2rem] font-bold text-center font-mono drop-shadow ${props.meta ? "text-[1vw]" : "text-[0.8vw]"}`}
            style={{
              color:
                CASE_PALETTE[puzzle_answer.puzzle.round.major_case.slug as MajorCaseEnum]
                  .answerColor,
            }}
          >
            {puzzle_answer?.answer?.toUpperCase()}
          </p>
        </RelativeAsset>
      )}
    </>
  );
};

export const ArtWrapper = ({
  className,
  outerClassName,
  background_src,
  children,
}: {
  className?: string;
  outerClassName?: string;
  background_src: string;
  children?: ReactNode;
}) => {
  return (
    <div className={outerClassName}>
      <div
        className={cn(
          "map relative left-1/2 transform -translate-x-1/2 w-full h-full select-none",
          className,
        )}
      >
        {children}
        <img className="art-bg-img w-full" src={background_src} />
      </div>
    </div>
  );
};

const CASE_ART_COMPONENT: { [key: string]: JSX.Element } = {
  exile: <ExileArt />,
  whales: <WhaleArt />,
};

export default function CasePageArt({ case_slug }: { case_slug: string }) {
  return CASE_ART_COMPONENT[case_slug];
}
