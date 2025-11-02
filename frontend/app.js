// Configuration and State
let recognition = null;
let isRecording = false;

// API Configuration - can be overridden
let apiConfig = {
    model: null,          // Will use default from backend
    temperature: null,     // Will use default from backend
    max_tokens: null,     // Will use default from backend
    top_p: null,          // Will use default from backend
    api_key: null,        // Will use default from backend
    api_url: null         // Will use default from backend
};

// Load API configuration on page load
async function loadAPIConfig() {
    try {
        const response = await fetch('/api/config');
        if (response.ok) {
            const config = await response.json();
            console.log('Loaded API config:', config);
            // Store config for reference, but use defaults
        }
    } catch (error) {
        console.warn('Failed to load API config, using defaults:', error);
    }
}

// Load config when page loads
loadAPIConfig();

// Check if browser supports Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'zh-CN';
    
    recognition.onstart = () => {
        isRecording = true;
        updateUI('recording');
        updateStatusText('正在识别语音...');
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        displayTranscribedText(transcript);
        updateStatusText('语音识别完成，正在生成回复...');
        generateResponses(transcript);
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isRecording = false;
        updateUI('idle');
        
        if (event.error === 'no-speech') {
            updateStatusText('未检测到语音，请重试');
        } else if (event.error === 'not-allowed') {
            updateStatusText('麦克风权限未授予');
        } else {
            updateStatusText('识别出错，请重试');
        }
    };
    
    recognition.onend = () => {
        isRecording = false;
        updateUI('idle');
    };
} else {
    console.warn('Speech Recognition API not supported');
    updateStatusText('浏览器不支持语音识别');
}

// UI Elements
const recordButton = document.getElementById('recordButton');
const statusText = document.getElementById('statusText');
const transcribedText = document.getElementById('transcribedText');
const optionsContainer = document.getElementById('optionsContainer');
const loadingOverlay = document.getElementById('loadingOverlay');
const optionItems = [
    document.getElementById('option0'),
    document.getElementById('option1'),
    document.getElementById('option2')
];

// Event Listeners
recordButton.addEventListener('click', toggleRecording);

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === ' ' && !isRecording) {
        e.preventDefault();
        toggleRecording();
    } else if (e.key === '1' || e.key === '2' || e.key === '3') {
        const index = parseInt(e.key) - 1;
        selectOption(index);
    }
});

// Functions
function toggleRecording() {
    if (!recognition) {
        alert('您的浏览器不支持语音识别功能');
        return;
    }
    
    if (isRecording) {
        recognition.stop();
    } else {
        clearPreviousResults();
        recognition.start();
    }
}

function updateUI(state) {
    if (state === 'recording') {
        recordButton.classList.add('recording');
        recordButton.querySelector('.button-text').textContent = '停止识别';
    } else {
        recordButton.classList.remove('recording');
        recordButton.querySelector('.button-text').textContent = '开始识别';
    }
}

function updateStatusText(text) {
    statusText.textContent = text;
}

function displayTranscribedText(text) {
    transcribedText.textContent = `识别内容：${text}`;
}

function clearPreviousResults() {
    transcribedText.textContent = '';
    optionsContainer.style.display = 'none';
    optionItems.forEach(item => {
        item.classList.remove('selected');
    });
}

async function generateResponses(message, customParams = {}) {
    showLoading();
    
    try {
        // Build request payload with all parameters
        const payload = {
            message: message,
            ...apiConfig,  // Include API config if set
            ...customParams // Allow custom parameters to override
        };
        
        // Remove null/undefined values to use backend defaults
        Object.keys(payload).forEach(key => {
            if (payload[key] === null || payload[key] === undefined) {
                delete payload[key];
            }
        });
        
        console.log('Sending request with payload:', payload);
        
        const response = await fetch('/api/generate-responses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.options && data.options.length === 3) {
            displayOptions(data.options);
            updateStatusText('请选择回复选项');
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('Error generating responses:', error);
        updateStatusText(`生成回复失败: ${error.message}`);
        // Show fallback options
        displayOptions([
            '好的，我理解了。',
            '没问题，我知道你的意思。',
            '明白了，我会注意的。'
        ]);
    } finally {
        hideLoading();
    }
}

/**
 * Update API configuration
 * Can be called to change API parameters dynamically
 */
function updateAPIConfig(config) {
    apiConfig = { ...apiConfig, ...config };
    console.log('Updated API config:', apiConfig);
}

function displayOptions(options) {
    options.forEach((option, index) => {
        if (optionItems[index]) {
            optionItems[index].querySelector('.option-text').textContent = option;
            optionItems[index].onclick = () => selectOption(index);
        }
    });
    
    optionsContainer.style.display = 'block';
}

function selectOption(index) {
    // Remove previous selection
    optionItems.forEach(item => item.classList.remove('selected'));
    
    // Add selection to clicked option
    if (optionItems[index]) {
        optionItems[index].classList.add('selected');
        const selectedText = optionItems[index].querySelector('.option-text').textContent;
        updateStatusText(`已选择：${selectedText}`);
        
        // Optional: You can add additional actions here, such as:
        // - Sending the selected response back to the server
        // - Speaking the selected response
        // - Logging the selection
        
        console.log(`Selected option ${index + 1}: ${selectedText}`);
        
        // Auto-reset after 3 seconds
        setTimeout(() => {
            clearPreviousResults();
            updateStatusText('等待识别语音...');
        }, 3000);
    }
}

function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Initialize
updateStatusText('等待识别语音...');

