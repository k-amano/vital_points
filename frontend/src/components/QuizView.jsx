import React, { useState, useEffect } from 'react'
import { quizSessionAPI } from '../api/client'
import './QuizView.css'

function QuizView({ sessionId, onComplete, onPause }) {
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isCompleted, setIsCompleted] = useState(false)

  useEffect(() => {
    loadQuestion()
  }, [sessionId])

  const loadQuestion = async () => {
    setLoading(true)
    setSelectedAnswer(null)
    setFeedback(null)

    try {
      const response = await quizSessionAPI.getCurrentQuestion(sessionId)

      if (response.data.message === '全ての問題に回答済みです') {
        setIsCompleted(true)
        await quizSessionAPI.complete(sessionId)
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

  if (isCompleted) {
    return (
      <div className="quiz-view completed">
        <div className="completion-card">
          <h2>おめでとうございます！</h2>
          <p>全ての問題に回答しました</p>
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
        <div className="question-image">
          <img src={imageUrl} alt="急所の図" />
          <div className="question-label">
            この急所「{question.number}」の名前は？
          </div>
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
                {choice.name}
              </button>
            )
          })}
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
