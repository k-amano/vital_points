import React, { useState, useEffect } from 'react'
import { quizSessionAPI } from '../api/client'
import './QuizView.css'

function QuizView({ sessionId, onComplete, onPause }) {
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isCompleted, setIsCompleted] = useState(false)
  const [result, setResult] = useState(null)

  useEffect(() => {
    loadQuestion()
  }, [sessionId])

  const getCompletionMessage = (score, mode) => {
    if (score === 100) {
      return {
        title: '素晴らしい！',
        message: '完璧です！全問正解おめでとうございます！'
      }
    } else if (score >= 90) {
      return {
        title: '優秀です！',
        message: 'ほぼ完璧ですね。素晴らしい成績です！'
      }
    } else if (score >= 80) {
      return {
        title: 'よくできました！',
        message: '高得点です！この調子で続けましょう。'
      }
    } else if (score >= 70) {
      return {
        title: '合格です！',
        message: '合格ラインに達しました。順調に学習が進んでいます。'
      }
    } else if (score >= 60) {
      return {
        title: 'もう少しです',
        message: 'あと少しで合格です。復習を続けましょう。'
      }
    } else {
      return {
        title: 'だめです',
        message: '復習モードで苦手な問題を集中的に学習しましょう。'
      }
    }
  }

  const loadQuestion = async () => {
    setLoading(true)
    setSelectedAnswer(null)
    setFeedback(null)

    try {
      const response = await quizSessionAPI.getCurrentQuestion(sessionId)

      if (response.data.message === '全ての問題に回答済みです') {
        const completeResponse = await quizSessionAPI.complete(sessionId)
        setResult(completeResponse.data)
        setIsCompleted(true)
      } else {
        setQuestion(response.data)
      }
    } catch (error) {
      console.error('問題の取得に失敗しました', error)
      alert('問題の取得に失敗しました')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSelect = async (choice) => {
    if (feedback) return // すでに回答済みの場合は何もしない

    setSelectedAnswer(choice.name)

    try {
      const response = await quizSessionAPI.submitAnswer(sessionId, {
        session_id: sessionId,
        question_id: question.question_id,
        selected_answer: choice.name,
      })

      setFeedback(response.data)
    } catch (error) {
      console.error('回答の送信に失敗しました', error)
      alert('回答の送信に失敗しました')
    }
  }

  const handleNextQuestion = () => {
    loadQuestion()
  }

  const handleEndSession = async () => {
    try {
      await quizSessionAPI.complete(sessionId)
      onComplete()
    } catch (error) {
      console.error('セッションの終了に失敗しました', error)
    }
  }

  const handlePause = async () => {
    try {
      await quizSessionAPI.pause(sessionId)
      onPause()
    } catch (error) {
      console.error('セッションの中断に失敗しました', error)
    }
  }

  if (loading) {
    return <div className="quiz-view loading">読み込み中...</div>
  }

  if (isCompleted && result) {
    const completionMsg = getCompletionMessage(result.score, result.mode)
    const modeText = result.mode === 'test' ? 'テスト' : '復習'

    return (
      <div className="quiz-view completed">
        <div className="completion-card">
          <h2>{completionMsg.title}</h2>
          <p className="completion-message">{completionMsg.message}</p>

          <div className="result-summary">
            <h3>{modeText}結果</h3>
            <div className="result-stats">
              <div className="result-item">
                <span className="result-label">正解数</span>
                <span className="result-value correct">{result.correct_count} / {result.total_questions}</span>
              </div>
              <div className="result-item">
                <span className="result-label">不正解数</span>
                <span className="result-value incorrect">{result.incorrect_count}</span>
              </div>
              <div className="result-item score">
                <span className="result-label">スコア</span>
                <span className="result-value">{result.score}点</span>
              </div>
            </div>
          </div>

          <button className="btn btn-primary" onClick={onComplete}>
            ホームに戻る
          </button>
        </div>
      </div>
    )
  }

  if (!question) {
    return <div className="quiz-view">問題がありません</div>
  }

  const imageUrl = `http://localhost:8000/static/images/${question.image_file}`

  return (
    <div className="quiz-view">
      <div className="quiz-header">
        <div className="progress">
          問題 {question.answered_count + 1} / {question.total_questions}
        </div>
        <button className="btn btn-secondary btn-small" onClick={handlePause}>
          中断
        </button>
      </div>

      <div className="question-card">
        <div className="question-label">
          この急所「{question.number}」の名前は？
        </div>

        <div className="choices">
          {question.choices.map((choice, index) => {
            const isSelected = selectedAnswer === choice.name
            const isCorrect = feedback && choice.name === feedback.correct_answer
            let className = 'choice-button'

            if (isSelected) {
              className += ' selected'
              if (feedback) {
                className += feedback.is_correct ? ' correct' : ' incorrect'
              }
            } else if (feedback && isCorrect) {
              className += ' correct-answer'
            }

            return (
              <button
                key={index}
                className={className}
                onClick={() => handleAnswerSelect(choice)}
                disabled={feedback !== null}
              >
                <span className="choice-name">{choice.name}</span>
                <span className="choice-reading">（{choice.reading}）</span>
              </button>
            )
          })}
        </div>

        <div className="question-image">
          <img src={imageUrl} alt="急所の図" />
        </div>

        {feedback && (
          <div className={`feedback ${feedback.is_correct ? 'correct' : 'incorrect'}`}>
            <p className="feedback-message">{feedback.message}</p>
            {!feedback.is_correct && (
              <p className="correct-answer-text">
                正解: {feedback.correct_answer}
              </p>
            )}
            <div className="feedback-buttons">
              <button className="btn btn-primary" onClick={handleNextQuestion}>
                次の問題へ
              </button>
              <button className="btn btn-secondary" onClick={handleEndSession}>
                学習を終える
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default QuizView
