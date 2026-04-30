// src/JS/modules/agent.js
/**
 * AI Agent Chat Module
 * LangGraph-based intelligent opportunity finder
 */

let messageHistory = [];
let isWaiting = false;

async function sendMessage(message = null) {
    const input = document.getElementById('agentInput');
    const userMessage = message || input.value.trim();
    
    if (!userMessage || isWaiting) return;
    
    // Clear input
    input.value = '';
    
    // Add to message history
    messageHistory.push({ role: 'user', content: userMessage });
    
    // Show thinking state
    showThinking();
    isWaiting = true;
    
    try {
        // Send request to agent
        const response = await fetch('/agent/search/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: userMessage,
                opportunity_type: 'all'
            })
        });
        
        // Handle streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            buffer += decoder.decode(value);
            const lines = buffer.split('\n');
            buffer = lines.pop();
            
            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const data = line.slice(6);
                if (data === '[DONE]') break;
                
                try {
                    const event = JSON.parse(data);
                    handleAgentEvent(event);
                } catch (e) {}
            }
        }
        
        isWaiting = false;
        hideThinking();
        
    } catch (error) {
        console.error('Error:', error);
        isWaiting = false;
        hideThinking();
    }
}

function handleAgentEvent(event) {
    switch (event.type) {
        case 'thinking':
            updateThinkingMessage(event.content);
            break;
        case 'opportunity':
            addOpportunityCard(event.data);
            break;
        case 'reasoning':
            showAgentReasoning(event.content);
            break;
        case 'error':
            showError(event.error);
            break;
    }
}

function showThinking() {
    const bubble = document.getElementById('thinkingBubble');
    bubble.style.display = 'block';
}

function hideThinking() {
    const bubble = document.getElementById('thinkingBubble');
    bubble.style.display = 'none';
}

function updateThinkingMessage(message) {
    const text = document.querySelector('#thinkingBubble p');
    if (text) {
        text.textContent = message;
    }
}

function showAgentReasoning(reasoning) {
    const bubble = document.getElementById('responseBubble');
    bubble.style.display = 'block';
    bubble.textContent = reasoning;
}

function showError(error) {
    const bubble = document.getElementById('responseBubble');
    bubble.style.display = 'block';
    bubble.style.backgroundColor = 'rgba(248, 113, 113, 0.1)';
    bubble.style.borderColor = '#f87171';
    bubble.textContent = `خطأ: ${error}`;
}

function addOpportunityCard(data) {
    const container = document.getElementById('opportunitiesContainer');
    if (!container) return;
    
    // Make container visible when first opportunity is added
    if (container.style.display === 'none') {
        container.style.display = 'block';
    }
    
    const card = document.createElement('div');
    card.className = 'bg-[#161f30] border border-[#1e2d42] rounded-xl p-4 mb-4';
    
    card.innerHTML = `
        <div class="flex items-start gap-3 mb-3">
            <div class="w-8 h-8 flex items-center justify-center bg-teal-400/10 rounded-full text-teal-400 flex-shrink-0">
                💼
            </div>
            <div>
                <h4 class="font-bold text-[#f1ede6] mb-1">${data.title}</h4>
                <p class="text-teal-400 text-sm">${data.company}</p>
                <p class="text-slate-400 text-sm">${data.location}</p>
            </div>
        </div>
        <p class="text-slate-400 text-sm mb-2">${data.description}</p>
        <div class="flex flex-wrap gap-2 mb-3">
            <span class="bg-white/[0.04] border border-[#1e2d42] rounded-full px-3 py-1 text-xs text-slate-400">
                📅 ${data.posted_date}
            </span>
            <span class="bg-white/[0.04] border border-[#1e2d42] rounded-full px-3 py-1 text-xs text-slate-400">
                ⏰ ${data.experience}
            </span>
            <span class="bg-white/[0.04] border border-[#1e2d42] rounded-full px-3 py-1 text-xs text-slate-400">
                💰 ${data.salary}
            </span>
        </div>
        <a href="${data.url}" target="_blank" 
           class="inline-flex items-center gap-2 border border-teal-400 text-teal-400 hover:bg-teal-400 hover:text-[#0b1120] rounded-xl px-4 py-2 text-sm font-bold transition-all duration-200">
            عرض التفاصيل →
        </a>
    `;
    
    container.appendChild(card);
}

// Initialize module
document.addEventListener('DOMContentLoaded', () => {
    console.log('Agent module initialized');
    // Any initialization logic can go here
});