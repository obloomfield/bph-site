import { useLocalStorage } from "@uidotdev/usehooks";
import { useEffect, useState } from "react";

import InputBox from "@/components/puzzle/nyt-games/letterboxed/InputBox";
import LetterBox from "@/components/puzzle/nyt-games/letterboxed/LetterBox";
import { Button } from "@/components/ui/button";
import { Puzzle, Solution } from "@/utils/minor_cases/nyt/LetterBoxedTypes";

function LetterBoxed({ puzzleNum }: { puzzleNum: 1 | 2 | 3 }) {
  const puzzles = {
    1: new Puzzle(
      [
        [
          null,
          { sides: [0], index: 0, letter: "i", uses: 1 },
          null,
          { sides: [0], index: 1, letter: "o", uses: 1 },
          null,
          { sides: [0], index: 2, letter: "r", uses: 1 },
          null,
          { sides: [0], index: 3, letter: "a", uses: 1 },
          null,
          { sides: [0], index: 4, letter: "t", uses: 1 },
          null,
        ],
        [
          null,
          { sides: [1], index: 5, letter: "c", uses: 1 },
          null,
          { sides: [1], index: 6, letter: "n", uses: 1 },
          null,
          { sides: [1], index: 7, letter: "m", uses: 1 },
          null,
          { sides: [1], index: 8, letter: "o", uses: 1 },
          null,
          { sides: [1], index: 9, letter: "n", uses: 1 },
          null,
        ],
        [
          null,
          { sides: [2], index: 10, letter: "o", uses: 1 },
          null,
          { sides: [2], index: 11, letter: "r", uses: 1 },
          null,
          { sides: [2], index: 12, letter: "a", uses: 1 },
          null,
          { sides: [2], index: 13, letter: "t", uses: 1 },
          null,
          { sides: [2], index: 14, letter: "o", uses: 1 },
          null,
        ],
      ],
      5,
    ),
    2: new Puzzle(
      [
        [
          null,
          { sides: [0], index: 0, letter: "e", uses: 2 },
          null,
          { sides: [0], index: 1, letter: "a", uses: 2 },
          null,
          { sides: [0], index: 2, letter: "u", uses: 1 },
          null,
        ],
        [
          null,
          { sides: [1], index: 3, letter: "l", uses: 1 },
          null,
          { sides: [1], index: 4, letter: "r", uses: 2 },
          null,
          { sides: [1], index: 5, letter: "i", uses: 2 },
          null,
        ],
        [
          null,
          { sides: [2], index: 6, letter: "c", uses: 1 },
          null,
          { sides: [2], index: 7, letter: "g", uses: 1 },
          null,
          { sides: [2], index: 8, letter: "b", uses: 1 },
          null,
        ],
        [
          null,
          { sides: [3], index: 9, letter: "b", uses: 1 },
          null,
          { sides: [3], index: 10, letter: "t", uses: 3 },
          null,
        ],
      ],
      6,
    ),
    3: new Puzzle(
      [
        [
          null,
          { sides: [0], index: 0, letter: "b", uses: 1 },
          { sides: [0], index: 1, letter: "r", uses: 3 },
          { sides: [0], index: 2, letter: "m", uses: 2 },
          { sides: [0, 1], index: 3, letter: "u", uses: 2 },
        ],
        [
          null,
          { sides: [1], index: 4, letter: "f", uses: 2 },
          { sides: [1], index: 5, letter: "s", uses: 2 },
          { sides: [1], index: 6, letter: "k", uses: 1 },
          { sides: [1, 2], index: 7, letter: "a", uses: 1 },
        ],
        [
          null,
          { sides: [2], index: 8, letter: "n", uses: 3 },
          { sides: [2], index: 9, letter: "c", uses: 2 },
          { sides: [2], index: 10, letter: "m", uses: 1 },
          { sides: [2, 3], index: 11, letter: "e", uses: 1 },
        ],
        [
          null,
          { sides: [3], index: 12, letter: "g", uses: 3 },
          { sides: [3], index: 13, letter: "t", uses: 1 },
          { sides: [3, 4], index: 14, letter: "i", uses: 6 },
        ],
        [
          null,
          { sides: [4], index: 15, letter: "l", uses: 1 },
          { sides: [4], index: 16, letter: "h", uses: 2 },
          { sides: [4], index: 17, letter: "d", uses: 1 },
          { sides: [4, 0], index: 18, letter: "o", uses: 1 },
        ],
      ],
      4,
    ),
  };

  const [solution, setSolution] = useLocalStorage<number[][]>(
    `nyt-letterboxed-${puzzleNum}-solution`,
    [[]],
  );
  const [answer, setAnswer] = useLocalStorage<string | null>(
    `nyt-letterboxed-${puzzleNum}-answer`,
    null,
  );
  const solutionObj = new Solution(puzzleNum, puzzles[puzzleNum], solution, setAnswer);

  /**
   * Attempts to push a new letter into the solution, checking that the solution is valid before doing so.
   * @param idx Index of new letter in solution
   */
  function attemptPushSolution(idx: number) {
    // Pushes idx to the last list in solution
    const res = solutionObj.attemptPushLetter(idx);
    if (res) {
      setSolution([...solutionObj.solution]);
    }
  }

  /**
   * Handle enters and delete keypresses using useEffect
   */
  function handleKeyPress(event: KeyboardEvent) {
    if (answer) {
      return;
    }
    if (event.key === "Enter") {
      // Check if solution is valid
      if (solutionObj.nextWord()) {
        setSolution([...solutionObj.solution]);
      }
    } else if (event.key === "Backspace") {
      // Pop last letter from solution
      if (solutionObj.popLetter()) {
        setSolution([...solutionObj.solution]);
      }
    }
  }

  useEffect(() => {
    window.addEventListener("keydown", handleKeyPress);
    return () => {
      window.removeEventListener("keydown", handleKeyPress);
    };
  });

  return (
    <>
      {/* All items centered */}
      <div className="flex flex-col mx-[5%] md:mx-[10%] my-6 items-center">
        <InputBox puzzle={puzzles[puzzleNum]} solutionArr={solution} answer={answer} />
        <LetterBox
          puzzle={puzzles[puzzleNum]}
          solutionArr={solution}
          onSelect={attemptPushSolution}
          solved={answer ? true : false}
        />
        <Button
          onClick={() => {
            setSolution([[]]);
            setAnswer(null);
          }}
        >
          Reset
        </Button>
        <div className="text-white">
          (Use the <code>enter</code> and <code>delete</code> keys to navigate)
        </div>
      </div>
    </>
  );
}

export default function LetterBoxedPuzzle() {
  const [puzzleNum, setPuzzleNum] = useState<1 | 2 | 3>(1);

  const [puzzleOneAnswer] = useLocalStorage<string | null>("nyt-letterboxed-1-answer", null);
  const [puzzleTwoAnswer] = useLocalStorage<string | null>("nyt-letterboxed-2-answer", null);

  return (
    <div className="flex flex-col items-center bg-[#fa8282]">
      <div className="flex flex-col items-center py-4">
        <div className="text-white py-2">Choose a puzzle:</div>
        <div className="flex space-x-4">
          <Button
            className={puzzleNum == 1 ? "bg-slate-800" : "bg-white"}
            onClick={() => setPuzzleNum(1)}
          >
            🥕
          </Button>
          <Button
            className={puzzleNum == 2 ? "bg-slate-800" : "bg-white"}
            onClick={() => setPuzzleNum(2)}
            disabled={puzzleOneAnswer ? false : true}
          >
            {puzzleOneAnswer ? "🐾" : "❓"}
          </Button>
          <Button
            className={puzzleNum == 3 ? "bg-slate-800" : "bg-white"}
            onClick={() => setPuzzleNum(3)}
            disabled={puzzleTwoAnswer ? false : true}
          >
            {puzzleTwoAnswer ? "🪶" : "❓"}
          </Button>
        </div>
      </div>
      <div className={puzzleNum != 1 ? "hidden" : ""}>
        <LetterBoxed puzzleNum={1} />
      </div>
      <div className={puzzleNum != 2 ? "hidden" : ""}>
        <LetterBoxed puzzleNum={2} />
      </div>
      <div className={puzzleNum != 3 ? "hidden" : ""}>
        <LetterBoxed puzzleNum={3} />
      </div>
    </div>
  );
}
