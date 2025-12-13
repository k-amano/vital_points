import React, { useState, useEffect } from 'react'
import { learningHistoryAPI } from '../api/client'
import './Statistics.css'

function Statistics({ onBack }) {
  const [statistics, setStatistics] = useState(null)
  const [weakPoints, setWeakPoints] = useState([])
  const [allHistory, setAllHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [statsRes, weakRes, historyRes] = await Promise.all([
        learningHistoryAPI.getStatistics(),
        learningHistoryAPI.getWeakPoints(),
        learningHistoryAPI.getAll(),
      ])

      setStatistics(statsRes.data)
      setWeakPoints(weakRes.data)
      setAllHistory(historyRes.data)
    } catch (error) {
      console.error('データの取得に失敗しました', error)
      alert('データの取得に失敗しました')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="statistics loading">読み込み中...</div>
  }

  return (
    <div className="statistics">
      <div className="statistics-header">
        <h2>学習統計</h2>
        <button className="btn btn-secondary" onClick={onBack}>
          戻る
        </button>
      </div>

      {statistics && (
        <div className="stats-overview">
          <div className="stat-card">
            <h3>総回答数</h3>
            <p className="big-number">{statistics.total_attempts}</p>
          </div>
          <div className="stat-card">
            <h3>正解数</h3>
            <p className="big-number correct">{statistics.total_correct}</p>
          </div>
          <div className="stat-card">
            <h3>不正解数</h3>
            <p className="big-number incorrect">{statistics.total_incorrect}</p>
          </div>
          <div className="stat-card">
            <h3>正解率</h3>
            <p className="big-number">{statistics.accuracy_rate.toFixed(1)}%</p>
          </div>
        </div>
      )}

      {weakPoints.length > 0 && (
        <div className="weak-points-section">
          <h3>苦手な急所（不正解が多い順）</h3>
          <div className="weak-points-list">
            {weakPoints.map((history, index) => (
              <div key={index} className="weak-point-item">
                <div className="rank">#{index + 1}</div>
                <div className="vital-point-info">
                  <span className="name">{history.vital_point.name}</span>
                  <span className="reading">({history.vital_point.reading})</span>
                </div>
                <div className="counts">
                  <span className="correct">正解: {history.correct_count}</span>
                  <span className="incorrect">不正解: {history.incorrect_count}</span>
                </div>
                <div className="accuracy">
                  正解率: {history.accuracy_rate.toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {allHistory.length > 0 && (
        <div className="all-history-section">
          <h3>全履歴</h3>
          <div className="history-table">
            <div className="table-header">
              <div className="col">番号</div>
              <div className="col">急所名</div>
              <div className="col">読み</div>
              <div className="col">正解</div>
              <div className="col">不正解</div>
              <div className="col">正解率</div>
            </div>
            {allHistory.map((history, index) => (
              <div key={index} className="table-row">
                <div className="col">{history.vital_point.number}</div>
                <div className="col">{history.vital_point.name}</div>
                <div className="col">{history.vital_point.reading}</div>
                <div className="col correct">{history.correct_count}</div>
                <div className="col incorrect">{history.incorrect_count}</div>
                <div className="col">{history.accuracy_rate.toFixed(1)}%</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Statistics
