const API_BASE = window.location.origin.replace(/:\d+$/, '') + '/api';

let wavesurfer = null;
document.addEventListener('DOMContentLoaded', () => {
  const askBtn = document.getElementById('askBtn');
  const playBtn = document.getElementById('playTts');
  askBtn.addEventListener('click', ask);
  playBtn.addEventListener('click', playTts);

  wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#4a90e2',
    progressColor: '#2b6fb8'
  });
});

async function ask(){
  const q = document.getElementById('question').value.trim();
  if(!q) return alert('请输入问题');
  const res = await fetch('/api/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({question: q})});
  const j = await res.json();
  document.getElementById('answer').textContent = j.answerText || JSON.stringify(j);
  // enable TTS
  document.getElementById('playTts').disabled = false;
  // store ssml
  window._lastSSML = j.ssml;
}

async function playTts(){
  if(!window._lastSSML) return;
  const res = await fetch('/api/tts', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ssml: window._lastSSML})});
  if(!res.ok) return alert('TTS 合成失败');
  const blob = await res.blob();
  // load into wavesurfer
  wavesurfer.loadBlob(blob);
  wavesurfer.on('ready', () => {
    wavesurfer.play();
  });
}
