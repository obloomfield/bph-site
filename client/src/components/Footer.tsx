import { FaInstagram } from "react-icons/fa";

export default function Footer() {
  return (
    <div className="footer bg-intherit text-white text-center p-3">
      <a
        href="https://www.instagram.com/brownpuzzlehunt/"
        className="border-r-2 border-muted-foreground pr-3"
      >
        <FaInstagram
          className="inline-block text-muted-foreground hover:text-white transition-colors"
          size={24}
        />
      </a>
      <span className="text-muted-foreground pl-3">
        powered by{" "}
        <a
          className="underline font-semibold hover:text-white transition-colors"
          href="https://github.com/galacticpuzzlehunt/gph-site/tree/master"
        >
          gph-site
        </a>
      </span>
    </div>
  );
}
