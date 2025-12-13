import { useState, useEffect } from 'react'
import './App.css'
import { learningHistoryAPI, quizSessionAPI } from './api/client'
import QuizView from './components/QuizView'
import Statistics from './components/Statistics'
import StartScreen from './components/StartScreen'

function App() {
  const [view, setView] = useState('start') // start, quiz, statistics
  const [sessionId, setSessionId] = useState(null)
  const [statistics, setStatistics] = useState(null)

  useEffect(() => {
    loadStatistics()
  }, [])

  // viewが'start'に変わったときに統計を再読み込み
  useEffect(() => {
    if (view === 'start') {
      loadStatistics()
    }
  }, [view])

  const loadStatistics = async () => {
    try {
      const response = await learningHistoryAPI.getStatistics()
      setStatistics(response.data)
    } catch (error) {
      console.error('統計情報の取得に失敗しました', error)
    }
  }

  const startNewSession = async () => {
    try {
      const response = await quizSessionAPI.startNew()
      setSessionId(response.data.id)
      setView('quiz')
    } catch (error) {
      console.error('セッションの開始に失敗しました', error)
      alert('セッションの開始に失敗しました')
    }
  }

  const handleQuizComplete = () => {
    loadStatistics()
    setView('start')
    setSessionId(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>人体の急所 学習アプリ</h1>
      </header>

      <main className="app-main">
        {view === 'start' && (
          <StartScreen
            statistics={statistics}
            onStart={startNewSession}
            onViewStatistics={() => setView('statistics')}
          />
        )}

        {view === 'quiz' && sessionId && (
          <QuizView
            sessionId={sessionId}
            onComplete={handleQuizComplete}
            onPause={() => setView('start')}
          />
        )}

        {view === 'statistics' && (
          <Statistics
            onBack={() => setView('start')}
          />
        )}
      </main>
    </div>
  )
}

export default App
