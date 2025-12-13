import React from 'react'
import './StartScreen.css'

function StartScreen({ statistics, onStart, onStartWeakPoints, onViewStatistics }) {
  return (
    <div className="start-screen">
      <div className="welcome-card">
        <h2>ようこそ！</h2>
        <p>人体の急所70箇所を学習しましょう</p>

        {statistics && (
          <div className="stats-summary">
            <h3>学習状況</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">累計正解数</span>
                <span className="stat-value correct">{statistics.total_correct}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">累計不正解数</span>
                <span className="stat-value incorrect">{statistics.total_incorrect}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">正解率</span>
                <span className="stat-value">{statistics.accuracy_rate.toFixed(1)}%</span>
              </div>
            </div>
          </div>
        )}

        <div className="button-group">
          <button className="btn btn-primary btn-large" onClick={onStart}>
            新しいセッションを開始
          </button>
          {statistics && statistics.total_incorrect > 0 && (
            <button className="btn btn-warning btn-large" onClick={onStartWeakPoints}>
              苦手な問題から開始
            </button>
          )}
          <button className="btn btn-secondary" onClick={onViewStatistics}>
            詳細な統計を見る
          </button>
        </div>
      </div>
    </div>
  )
}

export default StartScreen
