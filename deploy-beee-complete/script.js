// 全局变量
let currentSection = 'home';
let charts = {};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeHeroChart();
    initializeScrollAnimations();
    initializeSmoothScrolling();
    initializeAIAssistant();
});

// 初始化导航
function initializeNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // 移动端导航切换
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        // 汉堡菜单动画
        this.classList.toggle('active');
    });

    // 导航链接点击
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
                
                // 更新活动状态
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                
                // 移动端关闭导航
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    });

    // 滚动时更新导航状态
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section');
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
                currentSection = sectionId;
            }
        });
    });
}

// 初始化Hero图表
function initializeHeroChart() {
    const ctx = document.getElementById('heroChart');
    if (!ctx) return;

    charts.heroChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
            datasets: [{
                label: '内容热度',
                data: [65, 78, 90, 85, 95, 88],
                borderColor: '#FFD93D',
                backgroundColor: 'rgba(255, 217, 61, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#FFD93D',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            },
            elements: {
                point: {
                    hoverRadius: 8
                }
            }
        }
    });
}

// 初始化滚动动画
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // 观察需要动画的元素
    const animateElements = document.querySelectorAll('.feature-card, .product-card, .solution-card, .pricing-card, .case-item');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// 初始化平滑滚动
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// 初始化AI助手
function initializeAIAssistant() {
    const aiFab = document.querySelector('.ai-assistant-fab');
    const aiAssistant = document.querySelector('.ai-assistant');
    
    if (aiFab) {
        aiFab.addEventListener('click', function() {
            showAIChat();
        });
    }
    
    if (aiAssistant) {
        aiAssistant.addEventListener('click', function() {
            showAIChat();
        });
    }
}

// 显示AI聊天界面
function showAIChat() {
    // 创建AI聊天模态框
    const modal = document.createElement('div');
    modal.className = 'ai-chat-modal';
    modal.innerHTML = `
        <div class="ai-chat-container">
            <div class="ai-chat-header">
                <div class="ai-chat-title">
                    <i class="fas fa-robot"></i>
                    <span>Ask Beee - AI助手</span>
                </div>
                <button class="ai-chat-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="ai-chat-messages">
                <div class="ai-message">
                    <div class="ai-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        你好！我是Beee Media的AI助手，有什么可以帮助你的吗？
                    </div>
                </div>
            </div>
            <div class="ai-chat-input">
                <input type="text" placeholder="输入你的问题..." class="ai-input">
                <button class="ai-send">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
        .ai-chat-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        }
        
        .ai-chat-container {
            background: white;
            border-radius: 20px;
            width: 90%;
            max-width: 500px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            animation: slideUp 0.3s ease;
        }
        
        .ai-chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid #E9ECEF;
        }
        
        .ai-chat-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            color: #2C3E50;
        }
        
        .ai-chat-title i {
            color: #FFD93D;
            font-size: 20px;
        }
        
        .ai-chat-close {
            background: none;
            border: none;
            font-size: 20px;
            color: #6C757D;
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        
        .ai-chat-close:hover {
            background: #F8F9FA;
            color: #2C3E50;
        }
        
        .ai-chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            max-height: 400px;
        }
        
        .ai-message {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .ai-avatar {
            width: 40px;
            height: 40px;
            background: #FFD93D;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #2C3E50;
            font-size: 18px;
        }
        
        .message-content {
            background: #F8F9FA;
            padding: 12px 16px;
            border-radius: 18px;
            color: #2C3E50;
            line-height: 1.5;
        }
        
        .ai-chat-input {
            display: flex;
            gap: 12px;
            padding: 20px;
            border-top: 1px solid #E9ECEF;
        }
        
        .ai-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #E9ECEF;
            border-radius: 25px;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .ai-input:focus {
            outline: none;
            border-color: #FFD93D;
        }
        
        .ai-send {
            width: 45px;
            height: 45px;
            background: #FFD93D;
            border: none;
            border-radius: 50%;
            color: #2C3E50;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .ai-send:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(255, 217, 61, 0.3);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    
    document.head.appendChild(style);
    
    // 关闭模态框
    const closeBtn = modal.querySelector('.ai-chat-close');
    closeBtn.addEventListener('click', function() {
        modal.remove();
    });
    
    // 点击外部关闭
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    // 发送消息
    const sendBtn = modal.querySelector('.ai-send');
    const input = modal.querySelector('.ai-input');
    
    function sendMessage() {
        const message = input.value.trim();
        if (!message) return;
        
        // 添加用户消息
        addMessage(message, 'user');
        input.value = '';
        
        // 模拟AI回复
        setTimeout(() => {
            const aiResponse = generateAIResponse(message);
            addMessage(aiResponse, 'ai');
        }, 1000);
    }
    
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // 聚焦输入框
    input.focus();
}

// 添加消息到聊天界面
function addMessage(content, type) {
    const messagesContainer = document.querySelector('.ai-chat-messages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'user' ? 'user-message' : 'ai-message';
    
    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content user-content">
                ${content}
            </div>
            <div class="user-avatar">
                <i class="fas fa-user"></i>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="ai-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                ${content}
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // 添加用户消息样式
    if (type === 'user') {
        const style = document.createElement('style');
        style.textContent = `
            .user-message {
                display: flex;
                gap: 12px;
                margin-bottom: 20px;
                justify-content: flex-end;
            }
            
            .user-content {
                background: #FFD93D !important;
                color: #2C3E50 !important;
            }
            
            .user-avatar {
                width: 40px;
                height: 40px;
                background: #2C3E50;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
            }
        `;
        document.head.appendChild(style);
    }
}

// 生成AI回复
function generateAIResponse(userMessage) {
    const responses = {
        '你好': '你好！很高兴见到你！我是Beee Media的AI助手，可以帮你了解我们的产品和服务。',
        '价格': '我们提供三个套餐：标准版299元/月，专业版599元/月，企业版1999元/月。每个套餐都有免费试用期！',
        '功能': '我们的主要功能包括：趋势捕捉与分析、AI内容生成、效果预测与分发。你想了解哪个功能？',
        '试用': '当然可以！我们为所有新用户提供免费试用期。你可以先体验我们的核心功能，再决定是否购买。',
        '联系': '你可以通过以下方式联系我们：邮箱 hello@beeemedia.com，电话 +86 400-888-8888。',
        'default': '这是一个很好的问题！让我为你详细介绍一下...'
    };
    
    for (const [key, response] of Object.entries(responses)) {
        if (userMessage.includes(key)) {
            return response;
        }
    }
    
    return responses.default;
}

// 按钮点击效果
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn-primary, .btn-secondary, .btn-outline')) {
        // 添加点击波纹效果
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        e.target.appendChild(ripple);
        
        const rect = e.target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        setTimeout(() => ripple.remove(), 600);
    }
});

// 添加波纹效果样式
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .btn-primary, .btn-secondary, .btn-outline {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;

document.head.appendChild(rippleStyle);

// 添加滚动进度条
function addScrollProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress-bar';
    document.body.appendChild(progressBar);
    
    const style = document.createElement('style');
    style.textContent = `
        .scroll-progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #FFD93D, #F4C430);
            z-index: 10001;
            transition: width 0.1s ease;
        }
    `;
    document.head.appendChild(style);
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.body.offsetHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

// 初始化滚动进度条
addScrollProgressBar();

// 添加页面加载动画
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
    
    const style = document.createElement('style');
    style.textContent = `
        body {
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        
        body.loaded {
            opacity: 1;
        }
        
        .feature-card, .product-card, .solution-card, .pricing-card, .case-item {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease;
        }
        
        .animate-in {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
});

// 添加视差滚动效果
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.floating-elements .element');
    
    parallaxElements.forEach((element, index) => {
        const speed = 0.5 + (index * 0.1);
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px) rotate(${scrolled * 0.1}deg)`;
    });
});

// 添加鼠标跟随效果
document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.custom-cursor');
    if (cursor) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    }
});

// 创建自定义鼠标光标
function createCustomCursor() {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);
    
    const style = document.createElement('style');
    style.textContent = `
        .custom-cursor {
            position: fixed;
            width: 20px;
            height: 20px;
            background: rgba(255, 217, 61, 0.3);
            border: 2px solid #FFD93D;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transition: all 0.1s ease;
            mix-blend-mode: difference;
        }
        
        .custom-cursor.hover {
            transform: scale(2);
            background: rgba(255, 217, 61, 0.6);
        }
    `;
    document.head.appendChild(style);
    
    // 为可交互元素添加悬停效果
    const interactiveElements = document.querySelectorAll('button, a, .feature-card, .product-card');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
}

// 初始化自定义光标
createCustomCursor();
