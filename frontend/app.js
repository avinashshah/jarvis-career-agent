const statusPill = document.querySelector('.status-pill');
const assistantResponse = document.getElementById('assistant-response');
const assistantInput = document.getElementById('assistant-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const navButtons = document.querySelectorAll('.nav-item');
const tabPanels = document.querySelectorAll('.tab-panel');
const actionButtons = document.querySelectorAll('.action-btn');

let recognition = null;
let isListening = false;

const activateTab = (tabName) => {
  navButtons.forEach((button) => {
    const isActive = button.textContent.trim().toLowerCase().replace(/\s+/g, '-') === tabName.toLowerCase();
    button.classList.toggle('active', isActive);
  });

  tabPanels.forEach((panel) => {
    panel.classList.toggle('active', panel.dataset.tab === tabName);
  });
};

navButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const tabName = button.textContent.trim().toLowerCase().replace(/\s+/g, '-');
    activateTab(tabName);
  });
});

actionButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const query = button.dataset.query || button.textContent.trim();
    assistantInput.value = query;
    submitQuery();
  });
});

const speakResponse = (text) => {
  if (!('speechSynthesis' in window)) {
    return;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1;
  utterance.pitch = 1;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
};

const setBackendStatus = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/');
    const data = await response.json();
    if (response.ok) {
      statusPill.innerHTML = '<span class="status-dot"></span><span>Online</span>';
      if (data.message) {
        statusPill.title = data.message;
      }
    }
  } catch (error) {
    statusPill.innerHTML = '<span class="status-dot" style="background:#f59e0b"></span><span>Offline</span>';
    statusPill.title = 'Backend not available';
  }
};

const askJarvis = async (query) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/assistant/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      throw new Error('Query failed');
    }

    const data = await response.json();
    const message = data.response || 'I am ready to help.';
    assistantResponse.textContent = message;
    speakResponse(message);
  } catch (error) {
    const message = 'I am online and ready, but the backend connection is currently unavailable.';
    assistantResponse.textContent = message;
    speakResponse(message);
  }
};

const submitQuery = () => {
  const query = assistantInput.value.trim();
  if (!query || query === 'Ask JARVIS anything...') {
    return;
  }

  if (handleWakeWord(query)) {
    return;
  }

  assistantResponse.textContent = 'Thinking...';
  askJarvis(query);
};

const handleWakeWord = (transcript) => {
  const normalized = (transcript || '').toLowerCase().replace(/[^a-z\s]/g, '').replace(/\s+/g, ' ').trim();
  const isWakePhrase = (
    normalized.includes('hey') && (
      normalized.includes('jarvis') ||
      normalized.includes('jarivs') ||
      normalized.includes('jariv') ||
      normalized.includes('jarv') ||
      normalized.includes('jervis') ||
      normalized.includes('jarris')
    )
  ) || (
    normalized.includes('jarvis') ||
    normalized.includes('jarivs') ||
    normalized.includes('jariv') ||
    normalized.includes('jarv') ||
    normalized.includes('jervis') ||
    normalized.includes('jarris')
  );

  if (isWakePhrase) {
    const readyMessage = "I'm ready to assist my BOSS.";
    assistantResponse.textContent = readyMessage;
    assistantInput.value = '';
    speakResponse(readyMessage);
    return true;
  }
  return false;
};

window.handleWakeWord = handleWakeWord;

sendBtn.addEventListener('click', submitQuery);

assistantInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    submitQuery();
  }
});

assistantInput.addEventListener('focus', () => {
  if (assistantInput.value === 'Ask JARVIS anything...') {
    assistantInput.value = '';
  }
});

const restartVoiceListener = () => {
  if (!recognition || !micBtn.dataset.autoRestart || micBtn.dataset.autoRestart !== 'true') {
    return;
  }

  try {
    recognition.start();
  } catch (error) {
    // ignore restart errors while the browser is settling
  }
};

const initSpeechRecognition = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.maxAlternatives = 5;

  recognition.onstart = () => {
    isListening = true;
    micBtn.classList.add('listening');
    assistantInput.value = 'Listening...';
  };

  recognition.onend = () => {
    isListening = false;
    micBtn.classList.remove('listening');
    if (!assistantInput.value || assistantInput.value === 'Listening...') {
      assistantInput.value = 'Ask JARVIS anything...';
    }

    restartVoiceListener();
  };

  recognition.onresult = (event) => {
    let finalTranscript = '';
    for (let i = 0; i < event.results.length; i++) {
      finalTranscript += event.results[i][0].transcript;
    }

    const transcript = finalTranscript.trim();
    if (!transcript) {
      return;
    }

    assistantInput.value = transcript;
    const isWakePhrase = handleWakeWord(transcript);

    if (!isWakePhrase) {
      submitQuery();
    }
  };
};

micBtn.addEventListener('click', () => {
  if (!recognition) {
    initSpeechRecognition();
  }

  if (!recognition) {
    assistantResponse.textContent = 'Voice input is not supported in this browser. Please type your question.';
    return;
  }

  const shouldAutoRestart = !isListening;
  micBtn.dataset.autoRestart = String(shouldAutoRestart);

  if (isListening) {
    recognition.stop();
    return;
  }

  try {
    recognition.start();
  } catch (error) {
    // ignore starts that happen while a previous instance is still active
  }
});

setBackendStatus();
askJarvis('Find AI Developer roles posted in last 24 hours');
