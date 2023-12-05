import { useState } from 'react'
import './App.css'
import reactLogo from './assets/react.svg'
import { usePageContext } from './hooks/usePageContext'
import viteLogo from '/vite.svg'


function App() {
  const [count, setCount] = useState(0)

  const pageContext = usePageContext<{test: number, test2: number}>();
  const test = pageContext?.test
  const test2 = pageContext?.test2
  // console.log(pageContext)
  // console.log(context)

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <p>test: {test}</p>
        <p>test2: {test2}</p>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
          <br></br>
          HI THERE
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
