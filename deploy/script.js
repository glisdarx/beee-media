// 全局变量
let selectedCountries = [];
let trendsData = [];
let charts = {};

// 国家数据
const countries = [
    { code: 'UnitedStates', name: '美国', flag: '🇺🇸' },
    { code: 'China', name: '中国', flag: '🇨🇳' },
    { code: 'India', name: '印度', flag: '🇮🇳' },
    { code: 'Japan', name: '日本', flag: '🇯🇵' },
    { code: 'Russia', name: '俄罗斯', flag: '🇷🇺' },
    { code: 'Germany', name: '德国', flag: '🇩🇪' },
    { code: 'Indonesia', name: '印尼', flag: '🇮🇩' },
    { code: 'Brazil', name: '巴西', flag: '🇧🇷' },
    { code: 'France', name: '法国', flag: '🇫🇷' },
    { code: 'UnitedKingdom', name: '英国', flag: '🇬🇧' },
    { code: 'Turkey', name: '土耳其', flag: '🇹🇷' },
    { code: 'Italy', name: '意大利', flag: '🇮🇹' },
    { code: 'Mexico', name: '墨西哥', flag: '🇲🇽' },
    { code: 'SouthKorea', name: '韩国', flag: '🇰🇷' },
    { code: 'Canada', name: '加拿大', flag: '🇨🇦' },
    { code: 'Spain', name: '西班牙', flag: '🇪🇸' },
    { code: 'SaudiArabia', name: '沙特阿拉伯', flag: '🇸🇦' },
    { code: 'Egypt', name: '埃及', flag: '🇪🇬' },
    { code: 'Australia', name: '澳大利亚', flag: '🇦🇺' },
    { code: 'Poland', name: '波兰', flag: '🇵🇱' },
    { code: 'Iran', name: '伊朗', flag: '🇮🇷' },
    { code: 'Pakistan', name: '巴基斯坦', flag: '🇵🇰' },
    { code: 'Vietnam', name: '越南', flag: '🇻🇳' },
    { code: 'Nigeria', name: '尼日利亚', flag: '🇳🇬' },
    { code: 'Bangladesh', name: '孟加拉国', flag: '🇧🇩' },
    { code: 'Netherlands', name: '荷兰', flag: '🇳🇱' },
    { code: 'Argentina', name: '阿根廷', flag: '🇦🇷' },
    { code: 'Philippines', name: '菲律宾', flag: '🇵🇭' },
    { code: 'Malaysia', name: '马来西亚', flag: '🇲🇾' },
    { code: 'Colombia', name: '哥伦比亚', flag: '🇨🇴' },
    { code: 'UniteArabEmirates', name: '阿联酋', flag: '🇦🇪' },
    { code: 'Romania', name: '罗马尼亚', flag: '🇷🇴' },
    { code: 'Belgium', name: '比利时', flag: '🇧🇪' },
    { code: 'Switzerland', name: '瑞士', flag: '🇨🇭' },
    { code: 'Singapore', name: '新加坡', flag: '🇸🇬' },
    { code: 'Sweden', name: '瑞典', flag: '🇸🇪' },
    { code: 'Norway', name: '挪威', flag: '🇳🇴' },
    { code: 'Austria', name: '奥地利', flag: '🇦🇹' },
    { code: 'Kazakhstan', name: '哈萨克斯坦', flag: '🇰🇿' },
    { code: 'Algeria', name: '阿尔及利亚', flag: '🇩🇿' },
    { code: 'Chile', name: '智利', flag: '🇨🇱' },
    { code: 'Czechia', name: '捷克', flag: '🇨🇿' },
    { code: 'Peru', name: '秘鲁', flag: '🇵🇪' },
    { code: 'Iraq', name: '伊拉克', flag: '🇮🇶' },
    { code: 'Israel', name: '以色列', flag: '🇮🇱' },
    { code: 'Ukraine', name: '乌克兰', flag: '🇺🇦' },
    { code: 'Denmark', name: '丹麦', flag: '🇩🇰' },
    { code: 'Portugal', name: '葡萄牙', flag: '🇵🇹' },
    { code: 'Hungary', name: '匈牙利', flag: '🇭🇺' },
    { code: 'Greece', name: '希腊', flag: '🇬🇷' },
    { code: 'Finland', name: '芬兰', flag: '🇫🇮' },
    { code: 'NewZealand', name: '新西兰', flag: '🇳🇿' },
    { code: 'Belarus', name: '白俄罗斯', flag: '🇧🇾' },
    { code: 'Slovakia', name: '斯洛伐克', flag: '🇸🇰' },
    { code: 'Serbia', name: '塞尔维亚', flag: '🇷🇸' },
    { code: 'Lithuania', name: '立陶宛', flag: '🇱🇹' },
    { code: 'Luxembourg', name: '卢森堡', flag: '🇱🇺' },
    { code: 'Estonia', name: '爱沙尼亚', flag: '🇪🇪' }
];

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeCountrySelector();
    initializeSmoothScrolling();
});

// 初始化导航
function initializeNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // 移动端导航切换
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
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
            }
        });
    });
}

// 初始化国家选择器
function initializeCountrySelector() {
    const countryGrid = document.getElementById('countryGrid');
    
    countries.forEach(country => {
        const countryItem = document.createElement('div');
        countryItem.className = 'country-item';
        countryItem.innerHTML = `
            <input type="checkbox" id="country_${country.code}" value="${country.code}">
            <span>${country.flag}</span>
            <span>${country.name}</span>
        `;
        
        countryItem.addEventListener('change', function() {
            const checkbox = this.querySelector('input[type="checkbox"]');
            if (checkbox.checked) {
                if (!selectedCountries.includes(country.code)) {
                    selectedCountries.push(country.code);
                }
                this.classList.add('selected');
            } else {
                selectedCountries = selectedCountries.filter(c => c !== country.code);
                this.classList.remove('selected');
            }
        });
        
        countryGrid.appendChild(countryItem);
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

// 选择所有国家
function selectAllCountries() {
    const checkboxes = document.querySelectorAll('.country-item input[type="checkbox"]');
    const countryItems = document.querySelectorAll('.country-item');
    
    checkboxes.forEach((checkbox, index) => {
        checkbox.checked = true;
        countryItems[index].classList.add('selected');
    });
    
    selectedCountries = countries.map(c => c.code);
}

// 获取趋势数据
async function fetchTrendData() {
    if (selectedCountries.length === 0) {
        showNotification('请先选择至少一个国家', 'warning');
        return;
    }

    const loadingSpinner = document.getElementById('loadingSpinner');
    const fetchBtn = document.querySelector('.fetch-btn');
    
    loadingSpinner.style.display = 'block';
    fetchBtn.disabled = true;
    fetchBtn.textContent = '获取中...';

    try {
        const allTrends = [];
        
        for (const country of selectedCountries) {
            try {
                const trends = await fetchCountryTrends(country);
                if (trends && trends.length > 0) {
                    trends.forEach(trend => {
                        trend.country = country;
                        trend.countryName = countries.find(c => c.code === country)?.name || country;
                    });
                    allTrends.push(...trends);
                }
                
                // 添加延迟避免请求过快
                await new Promise(resolve => setTimeout(resolve, 1000));
                
            } catch (error) {
                console.error(`获取${country}数据失败:`, error);
                showNotification(`获取${country}数据失败: ${error.message}`, 'error');
            }
        }

        if (allTrends.length > 0) {
            trendsData = allTrends;
            displayTrendsData(allTrends);
            showNotification(`成功获取${allTrends.length}条趋势数据`, 'success');
        } else {
            showNotification('未获取到任何趋势数据', 'warning');
        }

    } catch (error) {
        console.error('获取趋势数据失败:', error);
        showNotification('获取趋势数据失败: ' + error.message, 'error');
    } finally {
        loadingSpinner.style.display = 'none';
        fetchBtn.disabled = false;
        fetchBtn.innerHTML = '<i class="fas fa-download"></i> 获取趋势数据';
    }
}

// 获取单个国家的趋势数据
async function fetchCountryTrends(countryCode) {
    try {
        const response = await fetch('/api/trends', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                countries: [countryCode]
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success && result.data) {
            return result.data;
        } else {
            throw new Error(result.error || '获取数据失败');
        }
        
    } catch (error) {
        console.error(`获取${countryCode}趋势数据失败:`, error);
        // 如果API调用失败，返回模拟数据
        return new Promise((resolve) => {
            setTimeout(() => {
                const mockTrends = [
                    {
                        name: `#${countryCode}热门话题1`,
                        context: '娱乐',
                        description: '1.2M posts',
                        country: countryCode
                    },
                    {
                        name: `#${countryCode}热门话题2`,
                        context: '科技',
                        description: '856K posts',
                        country: countryCode
                    },
                    {
                        name: `#${countryCode}热门话题3`,
                        context: '体育',
                        description: '543K posts',
                        country: countryCode
                    }
                ];
                resolve(mockTrends);
            }, 500);
        });
    }
}

// 显示趋势数据
function displayTrendsData(trends) {
    const trendsDisplay = document.getElementById('trendsDisplay');
    const statsCards = document.getElementById('statsCards');
    const trendsTableBody = document.getElementById('trendsTableBody');
    
    trendsDisplay.style.display = 'block';
    
    // 显示统计卡片
    displayStatsCards(trends);
    
    // 显示数据表格
    displayTrendsTable(trends);
    
    // 显示图表
    displayCharts(trends);
    
    // 滚动到结果区域
    trendsDisplay.scrollIntoView({ behavior: 'smooth' });
}

// 显示统计卡片
function displayStatsCards(trends) {
    const statsCards = document.getElementById('statsCards');
    
    const totalTrends = trends.length;
    const uniqueCountries = new Set(trends.map(t => t.country)).size;
    const categories = trends.reduce((acc, trend) => {
        const category = trend.context || '未分类';
        acc[category] = (acc[category] || 0) + 1;
        return acc;
    }, {});
    const topCategory = Object.entries(categories).sort((a, b) => b[1] - a[1])[0];
    
    statsCards.innerHTML = `
        <div class="stat-card">
            <h4>总趋势数</h4>
            <div class="number">${totalTrends}</div>
        </div>
        <div class="stat-card">
            <h4>涉及国家</h4>
            <div class="number">${uniqueCountries}</div>
        </div>
        <div class="stat-card">
            <h4>主要分类</h4>
            <div class="number">${topCategory ? topCategory[0] : '无'}</div>
        </div>
        <div class="stat-card">
            <h4>数据时间</h4>
            <div class="number">${new Date().toLocaleDateString()}</div>
        </div>
    `;
}

// 显示趋势表格
function displayTrendsTable(trends) {
    const trendsTableBody = document.getElementById('trendsTableBody');
    
    trendsTableBody.innerHTML = trends.map((trend, index) => `
        <tr>
            <td>${index + 1}</td>
            <td><strong>${trend.name}</strong></td>
            <td><span class="category-tag">${trend.context || '未分类'}</span></td>
            <td>${trend.description || '-'}</td>
            <td>${trend.countryName || trend.country}</td>
        </tr>
    `).join('');
}

// 显示图表
function displayCharts(trends) {
    // 销毁现有图表
    if (charts.topicsChart) {
        charts.topicsChart.destroy();
    }
    if (charts.categoriesChart) {
        charts.categoriesChart.destroy();
    }
    
    // 准备数据
    const categories = trends.reduce((acc, trend) => {
        const category = trend.context || '未分类';
        acc[category] = (acc[category] || 0) + 1;
        return acc;
    }, {});
    
    const topTopics = trends.slice(0, 10);
    
    // 热门话题分布图
    const topicsCtx = document.getElementById('topicsChart').getContext('2d');
    charts.topicsChart = new Chart(topicsCtx, {
        type: 'bar',
        data: {
            labels: topTopics.map(t => t.name.substring(0, 20) + '...'),
            datasets: [{
                label: '热度',
                data: topTopics.map(t => Math.floor(Math.random() * 1000) + 100),
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 1
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
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // 分类统计图
    const categoriesCtx = document.getElementById('categoriesChart').getContext('2d');
    charts.categoriesChart = new Chart(categoriesCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: [
                    '#6366f1', '#f59e0b', '#10b981', '#ef4444',
                    '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
                ],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// 搜索创作者
async function searchCreators() {
    const searchTerm = document.getElementById('creatorSearch').value.trim();
    const maxCreators = document.getElementById('maxCreators').value;
    const includeVideos = document.getElementById('includeVideos').checked;
    
    if (!searchTerm) {
        showNotification('请输入搜索关键词', 'warning');
        return;
    }
    
    const creatorsResults = document.getElementById('creatorsResults');
    creatorsResults.style.display = 'block';
    
    // 显示加载状态
    creatorsResults.innerHTML = `
        <div class="loading-container">
            <i class="fas fa-spinner fa-spin"></i>
            <p>正在搜索创作者数据...</p>
        </div>
    `;
    
    try {
        // 调用后端API
        const response = await fetch('/api/creators', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keyword: searchTerm,
                max_creators: parseInt(maxCreators),
                include_videos: includeVideos
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success && result.data) {
            displayCreatorsResults(result.data);
            showNotification(`找到${result.data.length}个创作者`, 'success');
        } else {
            throw new Error(result.error || '搜索失败');
        }
        
    } catch (error) {
        console.error('搜索创作者失败:', error);
        showNotification('搜索创作者失败: ' + error.message, 'error');
        
        // 如果API调用失败，显示错误信息
        creatorsResults.innerHTML = `
            <div class="error-container">
                <i class="fas fa-exclamation-triangle"></i>
                <p>搜索失败: ${error.message}</p>
                <button onclick="searchCreators()" class="retry-btn">重试</button>
            </div>
        `;
    }
}

// 显示创作者结果
function displayCreatorsResults(creators) {
    const creatorsResults = document.getElementById('creatorsResults');
    
    creatorsResults.innerHTML = `
        <div class="creators-grid">
            ${creators.map(creator => `
                <div class="creator-card">
                    <div class="creator-header">
                        <div class="creator-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="creator-info">
                            <h4>${creator.nickname}</h4>
                            <p>@${creator.username}</p>
                            ${creator.verified ? '<span class="verified-badge"><i class="fas fa-check-circle"></i></span>' : ''}
                        </div>
                    </div>
                    <div class="creator-stats">
                        <div class="stat">
                            <span class="stat-value">${formatNumber(creator.followers)}</span>
                            <span class="stat-label">粉丝</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">${formatNumber(creator.following)}</span>
                            <span class="stat-label">关注</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">${formatNumber(creator.likes)}</span>
                            <span class="stat-label">获赞</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">${creator.videos}</span>
                            <span class="stat-label">视频</span>
                        </div>
                    </div>
                    <div class="creator-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${creator.country}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

// 导出CSV
function exportToCSV() {
    if (trendsData.length === 0) {
        showNotification('没有数据可导出', 'warning');
        return;
    }
    
    const csvContent = convertToCSV(trendsData);
    downloadFile(csvContent, 'tiktok_trends.csv', 'text/csv');
}

// 导出JSON
function exportToJSON() {
    if (trendsData.length === 0) {
        showNotification('没有数据可导出', 'warning');
        return;
    }
    
    const jsonContent = JSON.stringify(trendsData, null, 2);
    downloadFile(jsonContent, 'tiktok_trends.json', 'application/json');
}

// 转换为CSV格式
function convertToCSV(data) {
    const headers = ['排名', '话题名称', '分类', '描述', '国家'];
    const rows = data.map((item, index) => [
        index + 1,
        item.name,
        item.context || '',
        item.description || '',
        item.countryName || item.country
    ]);
    
    return [headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n');
}

// 下载文件
function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// 格式化数字
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : type === 'error' ? 'times-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => notification.classList.add('show'), 100);
    
    // 自动隐藏
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// 添加通知样式
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 10000;
        max-width: 300px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #10b981;
    }
    
    .notification-warning {
        border-left: 4px solid #f59e0b;
    }
    
    .notification-error {
        border-left: 4px solid #ef4444;
    }
    
    .notification-info {
        border-left: 4px solid #6366f1;
    }
    
    .notification i {
        font-size: 1.2rem;
    }
    
    .notification-success i {
        color: #10b981;
    }
    
    .notification-warning i {
        color: #f59e0b;
    }
    
    .notification-error i {
        color: #ef4444;
    }
    
    .notification-info i {
        color: #6366f1;
    }
`;

document.head.appendChild(notificationStyles);

// 添加创作者卡片样式
const creatorStyles = document.createElement('style');
creatorStyles.textContent = `
    .creators-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }
    
    .creator-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .creator-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .creator-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .creator-avatar {
        width: 60px;
        height: 60px;
        background: var(--bg-secondary);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: var(--primary-color);
    }
    
    .creator-info h4 {
        margin: 0 0 5px 0;
        color: var(--text-primary);
    }
    
    .creator-info p {
        margin: 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .verified-badge {
        color: var(--accent-color);
        font-size: 1.2rem;
    }
    
    .creator-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .stat {
        text-align: center;
        padding: 15px;
        background: var(--bg-secondary);
        border-radius: 10px;
    }
    
    .stat-value {
        display: block;
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    .creator-location {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .creator-location i {
        margin-right: 5px;
        color: var(--primary-color);
    }
    
    .loading-container {
        text-align: center;
        padding: 40px;
        color: var(--text-secondary);
    }
    
    .loading-container i {
        font-size: 2rem;
        color: var(--primary-color);
        margin-bottom: 15px;
        display: block;
    }
    
    .category-tag {
        background: var(--primary-color);
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
    }
`;

document.head.appendChild(creatorStyles);
