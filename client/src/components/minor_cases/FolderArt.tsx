import blood from "@/assets/main_page/folders/sd_blood.png";
import sd_trim2 from "@/assets/main_page/folders/sd_trim2.png";
import birb from "@/assets/minor_cases/birbs/teaser-1.png";
import clip1 from "@/assets/minor_cases/clipping1.png";
import clip2 from "@/assets/minor_cases/clipping2.png";
import exile1 from "@/assets/minor_cases/exile/exile_teaser1.png";
import exile2 from "@/assets/minor_cases/exile/exile_teaser2.png";
import micro1 from "@/assets/minor_cases/microinfluencer/micro-teaser1.png";
import nyt1 from "@/assets/minor_cases/nyt/nyt-teaser1.png";
import nyt2 from "@/assets/minor_cases/nyt/nyt-teaser2.png";
import nyt3 from "@/assets/minor_cases/nyt/nyt-teaser3.png";
import twiqh2 from "@/assets/minor_cases/twiqh/twiqh.png";

export const BirbsCaseArt = () => {
  return (
    <div>
      <img
        className="absolute shadow-lg aspect-square object-cover w-[8vw]"
        style={{ left: "10%", top: "10%", rotate: "-27deg" }}
        src={birb}
      />
      <img
        className="absolute shadow-lg aspect-square object-cover w-[10vw]"
        style={{ left: "8%", top: "55%", rotate: "15deg" }}
        src={clip1}
      />
      <img
        className="absolute shadow-lg aspect-square object-cover w-[8vw]"
        style={{ left: "28%", top: "30%", rotate: "5deg" }}
        src={clip2}
      />
      <img
        className="absolute shadow-lg aspect-square object-cover w-[9vw]"
        style={{ left: "30%", top: "60%", rotate: "-15deg" }}
        src={birb}
      />
    </div>
  );
};

// SOCIAL DEDUCTION

export const ExileCaseArt = () => {
  return (
    <div>
      <img
        className="absolute shadow-lg aspect-square object-cover w-[8vw]"
        style={{ left: "10%", top: "10%", rotate: "-27deg" }}
        src={exile1}
      />
      <img
        className="absolute object-cover w-[20vw]"
        style={{ left: "8%", top: "60%", rotate: "15deg" }}
        src={blood}
      />
      <img
        className="absolute shadow-lg aspect-square object-cover w-[10vw]"
        style={{ left: "28%", top: "30%", rotate: "5deg" }}
        src={exile2}
      />
    </div>
  );
};

export const NYTCaseArt = () => {
  return (
    <div>
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "21%", top: "17%", rotate: "1deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "4%", top: "4%", rotate: "19deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "8%", top: "-4%", rotate: "27deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "11%", top: "10%", rotate: "-27deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "16%", top: "-2%", rotate: "22deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "23%", top: "-4%", rotate: "23deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "19%", top: "7%", rotate: "18  deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "30%", top: "12%", rotate: "13deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "28%", top: "0%", rotate: "-27deg" }}
        src={nyt1}
      />
      <img
        className="absolute aspect-square object-cover w-[8vw]"
        style={{ left: "0%", top: "-4%", rotate: "-27deg" }}
        src={nyt1}
      />
      <img
        className="absolute shadow-lg object-cover w-[29vw]"
        style={{ left: "2%", top: "45%", rotate: "5deg" }}
        src={nyt2}
      />
      <img
        className="absolute object-cover w-[29vw]"
        style={{ left: "3%", top: "53%", rotate: "0deg" }}
        src={nyt3}
      />
      {/* <img
        className="absolute object-cover w-[29vw]"
        style={{ left: "%", top: "55%", rotate: "0deg", zIndex: -1 }}
        src={sdtrim1}
      /> */}
      <img
        className="absolute object-cover w-[20vw]"
        style={{ left: "8%", top: "60%", rotate: "15deg" }}
        src={blood}
      />
    </div>
  );
};
export const MicroinfluencerCaseArt = () => {
  return (
    <div>
      <img
        className="absolute aspect-square object-cover w-[30vw]"
        style={{ left: "2%", top: "10%", rotate: "0deg" }}
        src={micro1}
      />
      <img
        className="absolute aspect-square object-cover w-[35vw]"
        style={{ left: "2%", top: "10%", rotate: "0deg", zIndex: -1 }}
        src={blood}
      />
    </div>
  );
};
export const TWIQHCaseArt = () => {
  return (
    <div>
      <img
        className="absolute object-cover w-[30vw]"
        style={{ left: "2%", top: "10%", rotate: "0deg" }}
        src={twiqh2}
      />
      <img
        className="absolute object-cover w-[30vw]"
        style={{ left: "2%", top: "10%", rotate: "0deg", zIndex: -1 }}
        src={sd_trim2}
      />
    </div>
  );
};

export const CASE_ART_BY_ROUND_SLUG: Record<string, JSX.Element> = {
  "birbs-at-brown": <BirbsCaseArt />,
  exile: <ExileCaseArt />,
  nyt: <NYTCaseArt />,
  microinfluencer: <MicroinfluencerCaseArt />,
  twiqh: <TWIQHCaseArt />,
};
