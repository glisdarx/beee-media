/**
 * Beee Media 认证系统 JavaScript
 * 处理登录、注册、Google OAuth等功能
 */

// 配置
const API_BASE_URL = 'https://your-backend-api.com'; // TODO: 更新为实际API地址
const GOOGLE_CLIENT_ID = 'your-google-client-id'; // TODO: 更新为实际Google Client ID

// DOM 元素
const elements = {
    // 表单
    loginForm: document.getElementById('loginForm'),
    registerForm: document.getElementById('registerForm'),
    
    // 输入框
    loginEmail: document.getElementById('loginEmail'),
    loginPassword: document.getElementById('loginPassword'),
    registerName: document.getElementById('registerName'),
    registerEmail: document.getElementById('registerEmail'),
    registerPassword: document.getElementById('registerPassword'),
    registerPasswordConfirm: document.getElementById('registerPasswordConfirm'),
    
    // 按钮
    loginBtn: document.getElementById('loginBtn'),
    registerBtn: document.getElementById('registerBtn'),
    
    // 消息
    successMessage: document.getElementById('successMessage'),
    errorMessage: document.getElementById('errorMessage'),
    
    // 切换按钮
    toggleBtns: document.querySelectorAll('.toggle-btn')
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
    setupEventListeners();
    checkAuthStatus();
});

/**
 * 初始化认证系统
 */
function initializeAuth() {
    // 清除之前的消息
    clearMessages();
    
    // 检查URL参数
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const action = urlParams.get('action');
    
    if (token && action === 'verify-email') {
        verifyEmail(token);
    } else if (token && action === 'reset-password') {
        showResetPasswordForm(token);
    }
}

/**
 * 设置事件监听器
 */
function setupEventListeners() {
    // 表单提交
    elements.loginForm.addEventListener('submit', handleLogin);
    elements.registerForm.addEventListener('submit', handleRegister);
    
    // 实时验证
    elements.registerPassword.addEventListener('input', validatePasswordStrength);
    elements.registerPasswordConfirm.addEventListener('input', validatePasswordMatch);
    elements.registerEmail.addEventListener('blur', validateEmail);
    elements.loginEmail.addEventListener('blur', validateEmail);
}

/**
 * 显示登录表单
 */
function showLogin() {
    elements.loginForm.classList.add('active');
    elements.registerForm.classList.remove('active');
    
    // 更新切换按钮状态
    elements.toggleBtns.forEach((btn, index) => {
        btn.classList.toggle('active', index === 0);
    });
    
    clearMessages();
}

/**
 * 显示注册表单
 */
function showRegister() {
    elements.registerForm.classList.add('active');
    elements.loginForm.classList.remove('active');
    
    // 更新切换按钮状态
    elements.toggleBtns.forEach((btn, index) => {
        btn.classList.toggle('active', index === 1);
    });
    
    clearMessages();
}

/**
 * 处理登录
 */
async function handleLogin(event) {
    event.preventDefault();
    
    const email = elements.loginEmail.value.trim();
    const password = elements.loginPassword.value;
    
    // 客户端验证
    if (!validateLoginForm(email, password)) {
        return;
    }
    
    // 显示加载状态
    setButtonLoading(elements.loginBtn, true);
    clearMessages();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 保存token
            localStorage.setItem('auth_token', data.token);
            localStorage.setItem('user_data', JSON.stringify(data.user));
            
            showSuccessMessage('登录成功！正在跳转...');
            
            // 延迟跳转
            setTimeout(() => {
                window.location.href = '/creators';
            }, 1500);
        } else {
            showErrorMessage(data.message || '登录失败，请重试');
        }
    } catch (error) {
        console.error('Login error:', error);
        showErrorMessage('网络错误，请检查您的连接');
    } finally {
        setButtonLoading(elements.loginBtn, false);
    }
}

/**
 * 处理注册
 */
async function handleRegister(event) {
    event.preventDefault();
    
    const name = elements.registerName.value.trim();
    const email = elements.registerEmail.value.trim();
    const password = elements.registerPassword.value;
    const passwordConfirm = elements.registerPasswordConfirm.value;
    
    // 客户端验证
    if (!validateRegisterForm(name, email, password, passwordConfirm)) {
        return;
    }
    
    // 显示加载状态
    setButtonLoading(elements.registerBtn, true);
    clearMessages();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccessMessage('注册成功！请检查您的邮箱并点击验证链接。');
            
            // 清空表单
            elements.registerForm.reset();
            
            // 可选择性切换到登录表单
            setTimeout(() => {
                showLogin();
                showSuccessMessage('账户已创建，请查收验证邮件后登录');
            }, 3000);
        } else {
            showErrorMessage(data.message || '注册失败，请重试');
        }
    } catch (error) {
        console.error('Register error:', error);
        showErrorMessage('网络错误，请检查您的连接');
    } finally {
        setButtonLoading(elements.registerBtn, false);
    }
}

/**
 * 处理Google登录
 */
async function handleGoogleLogin(credentialResponse) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/google-login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                google_token: credentialResponse.credential 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 保存token
            localStorage.setItem('auth_token', data.token);
            localStorage.setItem('user_data', JSON.stringify(data.user));
            
            showSuccessMessage('Google登录成功！正在跳转...');
            
            setTimeout(() => {
                window.location.href = '/creators';
            }, 1500);
        } else {
            showErrorMessage(data.message || 'Google登录失败');
        }
    } catch (error) {
        console.error('Google login error:', error);
        showErrorMessage('Google登录出错，请重试');
    }
}

/**
 * 处理Google注册（实际上是同一个流程）
 */
function handleGoogleRegister() {
    // Google OAuth 会自动处理注册和登录
    // 实际的处理逻辑在 handleGoogleLogin 中
    showSuccessMessage('请在弹出窗口中完成Google登录...');
}

/**
 * 验证邮箱
 */
async function verifyEmail(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/verify-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccessMessage('邮箱验证成功！您现在可以登录了。');
            showLogin();
        } else {
            showErrorMessage(data.message || '邮箱验证失败');
        }
    } catch (error) {
        console.error('Email verification error:', error);
        showErrorMessage('验证过程出错，请重试');
    }
}

/**
 * 显示忘记密码表单
 */
function showForgotPassword() {
    const email = prompt('请输入您的邮箱地址：');
    if (email && validateEmailFormat(email)) {
        requestPasswordReset(email);
    } else if (email) {
        showErrorMessage('请输入有效的邮箱地址');
    }
}

/**
 * 请求密码重置
 */
async function requestPasswordReset(email) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/forgot-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        showSuccessMessage('密码重置链接已发送到您的邮箱');
    } catch (error) {
        console.error('Password reset error:', error);
        showErrorMessage('密码重置请求失败，请重试');
    }
}

/**
 * 表单验证函数
 */
function validateLoginForm(email, password) {
    let isValid = true;
    
    if (!email) {
        showFieldError('loginEmailError', '请输入邮箱地址');
        isValid = false;
    } else if (!validateEmailFormat(email)) {
        showFieldError('loginEmailError', '邮箱格式无效');
        isValid = false;
    } else {
        hideFieldError('loginEmailError');
    }
    
    if (!password) {
        showFieldError('loginPasswordError', '请输入密码');
        isValid = false;
    } else {
        hideFieldError('loginPasswordError');
    }
    
    return isValid;
}

function validateRegisterForm(name, email, password, passwordConfirm) {
    let isValid = true;
    
    if (!name) {
        showFieldError('registerNameError', '请输入姓名');
        isValid = false;
    } else {
        hideFieldError('registerNameError');
    }
    
    if (!email) {
        showFieldError('registerEmailError', '请输入邮箱地址');
        isValid = false;
    } else if (!validateEmailFormat(email)) {
        showFieldError('registerEmailError', '邮箱格式无效');
        isValid = false;
    } else {
        hideFieldError('registerEmailError');
    }
    
    if (!password) {
        showFieldError('registerPasswordError', '请输入密码');
        isValid = false;
    } else if (password.length < 6) {
        showFieldError('registerPasswordError', '密码长度至少6位');
        isValid = false;
    } else {
        hideFieldError('registerPasswordError');
    }
    
    if (password !== passwordConfirm) {
        showFieldError('registerPasswordConfirmError', '两次输入的密码不一致');
        isValid = false;
    } else {
        hideFieldError('registerPasswordConfirmError');
    }
    
    return isValid;
}

function validateEmailFormat(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateEmail(event) {
    const email = event.target.value.trim();
    const errorId = event.target.id + 'Error';
    
    if (email && !validateEmailFormat(email)) {
        showFieldError(errorId, '邮箱格式无效');
        event.target.classList.add('error');
    } else {
        hideFieldError(errorId);
        event.target.classList.remove('error');
    }
}

function validatePasswordStrength(event) {
    const password = event.target.value;
    const errorId = 'registerPasswordError';
    
    if (password.length > 0 && password.length < 6) {
        showFieldError(errorId, '密码长度至少6位');
        event.target.classList.add('error');
    } else {
        hideFieldError(errorId);
        event.target.classList.remove('error');
    }
}

function validatePasswordMatch(event) {
    const password = elements.registerPassword.value;
    const confirmPassword = event.target.value;
    const errorId = 'registerPasswordConfirmError';
    
    if (confirmPassword && password !== confirmPassword) {
        showFieldError(errorId, '两次输入的密码不一致');
        event.target.classList.add('error');
    } else {
        hideFieldError(errorId);
        event.target.classList.remove('error');
    }
}

/**
 * UI 辅助函数
 */
function showSuccessMessage(message) {
    elements.successMessage.textContent = message;
    elements.successMessage.classList.add('show');
    elements.errorMessage.classList.remove('show');
}

function showErrorMessage(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.classList.add('show');
    elements.successMessage.classList.remove('show');
}

function clearMessages() {
    elements.successMessage.classList.remove('show');
    elements.errorMessage.classList.remove('show');
}

function showFieldError(errorId, message) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
}

function hideFieldError(errorId) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.classList.remove('show');
    }
}

function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

/**
 * 检查认证状态
 */
function checkAuthStatus() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        // 如果已经登录，可以选择重定向
        // window.location.href = '/creators';
    }
}

/**
 * 返回上一页
 */
function goBack() {
    window.history.back();
}

/**
 * 登出功能
 */
function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = '/';
}

/**
 * 获取认证token
 */
function getAuthToken() {
    return localStorage.getItem('auth_token');
}

/**
 * 获取用户数据
 */
function getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

/**
 * 检查用户是否已登录
 */
function isLoggedIn() {
    return !!getAuthToken();
}

// 导出函数供其他模块使用
window.authModule = {
    logout,
    getAuthToken,
    getUserData,
    isLoggedIn,
    showLogin,
    showRegister
};
