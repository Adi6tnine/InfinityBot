document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const clearChatButton = document.getElementById('clear-chat');
    const themeToggleButton = document.getElementById('theme-toggle');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    let currentTheme = 'dark';
    
    // Initialize Particles.js
    if (typeof particlesJS !== 'undefined') {
        initParticles();
    }
    
    // Display welcome message when page loads with slight delay for effect
    setTimeout(() => {
        addBotMessage("नमस्ते! I'm Infinity AI, your personal knowledge assistant with special expertise on India. Ask me about Indian cities, landmarks, culture, or try questions like 'What time is it in Mumbai?' or 'Tell me about the Taj Mahal.' I can also help with general knowledge, calculations, jokes, and more. How can I assist you today?");
    }, 800);
    
    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input field
        userInput.value = '';
        
        // Process the message
        processUserMessage(message);
    });
    
    // Process user message and get response
    function processUserMessage(message) {
        // Show typing indicator with natural delay
        showTypingIndicator();
        
        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Determine typing delay based on response length (longer for longer responses)
            const responseLength = data.response.length;
            const baseDelay = 700;
            const perCharDelay = 10;
            const maxDelay = 3000;
            const typingDelay = Math.min(baseDelay + responseLength * perCharDelay, maxDelay);
            
            setTimeout(() => {
                // Remove typing indicator and add bot response
                removeTypingIndicator();
                addBotMessage(data.response);
            }, typingDelay);
        })
        .catch(error => {
            setTimeout(() => {
                removeTypingIndicator();
                addBotMessage("Sorry, I'm having trouble connecting. Please try again later.");
                console.error('Error:', error);
            }, 800);
        });
    }
    
    // Handle suggestion chips
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            userInput.value = query;
            
            // Add a visual feedback effect
            this.classList.add('active-chip');
            setTimeout(() => {
                this.classList.remove('active-chip');
            }, 300);
            
            // Trigger form submission
            const event = new Event('submit', {
                'bubbles': true,
                'cancelable': true
            });
            chatForm.dispatchEvent(event);
        });
    });
    
    // Handle clear chat button
    clearChatButton.addEventListener('click', function() {
        // Add button press effect
        this.classList.add('active');
        setTimeout(() => {
            this.classList.remove('active');
        }, 200);
        
        // Fade out all messages
        const messages = chatMessages.querySelectorAll('.message');
        messages.forEach(msg => {
            msg.style.opacity = '0';
            msg.style.transform = 'scale(0.9)';
        });
        
        // Clear all messages after fade out animation
        setTimeout(() => {
            while (chatMessages.firstChild) {
                chatMessages.removeChild(chatMessages.firstChild);
            }
            
            // Add welcome message again
            setTimeout(() => {
                addBotMessage("Chat cleared. How can I help you today?");
            }, 300);
        }, 300);
    });
    
    // Handle theme toggle
    themeToggleButton.addEventListener('click', function() {
        // Add button press effect
        this.classList.add('active');
        setTimeout(() => {
            this.classList.remove('active');
        }, 200);
        
        // Toggle theme
        const htmlElement = document.documentElement;
        
        if (currentTheme === 'dark') {
            htmlElement.setAttribute('data-bs-theme', 'light');
            this.innerHTML = '<i class="fas fa-sun"></i>';
            currentTheme = 'light';
            
            // Add custom light theme class
            document.body.classList.add('light-theme');
        } else {
            htmlElement.setAttribute('data-bs-theme', 'dark');
            this.innerHTML = '<i class="fas fa-moon"></i>';
            currentTheme = 'dark';
            
            // Remove custom light theme class
            document.body.classList.remove('light-theme');
        }
    });
    
    // Function to add user message to chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-content';
        messageText.textContent = message;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();
        
        messageElement.appendChild(messageText);
        messageElement.appendChild(messageTime);
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Function to add bot message to chat
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-content';
        
        // Format links if any present in the message
        const formattedMessage = formatLinks(message);
        messageText.innerHTML = formattedMessage;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();
        
        messageElement.appendChild(messageText);
        messageElement.appendChild(messageTime);
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Function to format links in text
    function formatLinks(text) {
        // URL pattern
        const urlPattern = /(https?:\/\/[^\s]+)/g;
        
        // Replace URLs with anchor tags
        return text.replace(urlPattern, url => {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            indicator.appendChild(dot);
        }
        
        chatMessages.appendChild(indicator);
        scrollToBottom();
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            // Fade out animation
            indicator.style.opacity = '0';
            indicator.style.transform = 'translateY(10px)';
            
            // Remove after animation completes
            setTimeout(() => {
                if (indicator && indicator.parentNode) {
                    indicator.remove();
                }
            }, 200);
        }
    }
    
    // Function to get current time
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Function to scroll to bottom of chat
    function scrollToBottom() {
        // Smooth scroll
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    // Initialize particles.js
    function initParticles() {
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 50,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: '#6a11cb'
                },
                shape: {
                    type: 'circle',
                    stroke: {
                        width: 0,
                        color: '#000000'
                    }
                },
                opacity: {
                    value: 0.3,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 1,
                        opacity_min: 0.1,
                        sync: false
                    }
                },
                size: {
                    value: 3,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 2,
                        size_min: 0.1,
                        sync: false
                    }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#6a11cb',
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 1,
                    direction: 'none',
                    random: true,
                    straight: false,
                    out_mode: 'out',
                    bounce: false,
                    attract: {
                        enable: false,
                        rotateX: 600,
                        rotateY: 1200
                    }
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: {
                        enable: true,
                        mode: 'grab'
                    },
                    onclick: {
                        enable: true,
                        mode: 'push'
                    },
                    resize: true
                },
                modes: {
                    grab: {
                        distance: 140,
                        line_linked: {
                            opacity: 0.5
                        }
                    },
                    push: {
                        particles_nb: 3
                    }
                }
            },
            retina_detect: true
        });
    }
    
    // Handle keyboard events for input field
    userInput.addEventListener('keydown', function(e) {
        // Allow submitting with Enter without Shift key
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Focus on input field when page loads
    userInput.focus();
    
    // Keep focus on input when clicking anywhere in the chat
    document.addEventListener('click', function(e) {
        // Don't focus input when clicking on links in messages
        if (!e.target.closest('a')) {
            userInput.focus();
        }
    });
});
