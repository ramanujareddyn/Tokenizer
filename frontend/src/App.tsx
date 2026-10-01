import { useMemo, useState } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE = `${import.meta.env.VITE_API_URL}/api/v1`;
function App() {
  const [text, setText] = useState('hello world hello alpha')
  const [mode, setMode] = useState<'tiktoken' | 'custom'>('tiktoken')
  const [encoding, setEncoding] = useState('gpt2')
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const stats = useMemo(() => {
    const values = result?.statistics as Record<string, number> | undefined
    return values ?? { token_count: 0, character_count: 0, word_count: 0 }
  }, [result])

  const handleTokenize = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_BASE}/tokenize`, {
        text,
        mode,
        encoding,
      })
      setResult(response.data)
    } catch (err: unknown) {
      const message = axios.isAxiosError(err)
        ? err.response?.data?.detail || 'Unable to tokenize the supplied text.'
        : 'Unable to tokenize the supplied text.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setLoading(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await axios.post(`${API_BASE}/process-file`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setText(response.data.text)
      setResult({
        token_ids: [],
        decoded_tokens: response.data.text.split(/\s+/).filter(Boolean),
        token_count: response.data.text.split(/\s+/).filter(Boolean).length,
        selected_mode: 'uploaded',
        statistics: response.data.stats,
      })
    } catch (err: unknown) {
      const message = axios.isAxiosError(err)
        ? err.response?.data?.detail || 'Unable to process the uploaded file.'
        : 'Unable to process the uploaded file.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const tokenList = Array.isArray(result?.decoded_tokens)
    ? (result.decoded_tokens as Array<string | number>)
    : []

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Tokenizer workspace</p>
          <h1>TOkenizer</h1>
        </div>
        <button className="primary" type="button" onClick={handleTokenize} disabled={loading}>
          {loading ? 'Processing...' : 'Tokenize'}
        </button>
      </header>

      <main className="content-grid">
        <section className="panel input-panel">
          <div className="row controls">
            <label>
              Mode
              <select value={mode} onChange={(event) => setMode(event.target.value as 'tiktoken' | 'custom')}>
                <option value="tiktoken">Tiktoken</option>
                <option value="custom">Custom</option>
              </select>
            </label>

            <label>
              Encoding
              <select value={encoding} onChange={(event) => setEncoding(event.target.value)}>
                <option value="gpt2">gpt2</option>
                <option value="r50k_base">r50k_base</option>
                <option value="cl100k_base">cl100k_base</option>
              </select>
            </label>
          </div>

          <label className="textarea-label">
            Input text
            <textarea
              value={text}
              onChange={(event) => setText(event.target.value)}
              rows={12}
              placeholder="Paste text or upload a .txt / .pdf document"
            />
          </label>

          <div className="row upload-row">
            <label className="upload-file">
              Upload file
              <input type="file" accept=".txt,.pdf" onChange={handleFileUpload} />
            </label>
          </div>

          {error ? <div className="error-banner">{error}</div> : null}
        </section>

        <aside className="panel stats-panel">
          <h2>Statistics</h2>
          <div className="stats-grid">
            <div><span>Tokens</span><strong>{stats.token_count ?? 0}</strong></div>
            <div><span>Words</span><strong>{stats.word_count ?? 0}</strong></div>
            <div><span>Characters</span><strong>{stats.character_count ?? 0}</strong></div>
            <div><span>Tokens/Word</span><strong>{stats.tokens_per_word ?? 0}</strong></div>
          </div>
        </aside>
      </main>

      <section className="panel results-panel">
        <h2>Token output</h2>
        <div className="token-list">
          {tokenList.length > 0 ? (
            tokenList.map((token, index) => (
              <div key={`${String(token)}-${index}`} className="token-chip">
                <span>{index}</span>
                {String(token)}
              </div>
            ))
          ) : (
            <p className="empty-state">No tokens generated yet.</p>
          )}
        </div>
      </section>
    </div>
  )
}

export default App
