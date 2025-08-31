// 创作者搜索页面JavaScript

// 全局变量
let searchResults = [];
let currentPage = 1;
let itemsPerPage = 10;
let currentSortField = '';
let currentSortOrder = 'desc';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 检查认证状态
    if (!checkAuthStatus()) {
        showAuthRequiredMessage();
        return;
    }
    
    initializeCreatorsPage();
});

// 初始化页面
function initializeCreatorsPage() {
    initializeNavigation();
    initializeSearchForm();
    initializeModal();
    initializePagination();
    initializeExport();
    initializeSorting();
    
    // 显示空状态
    showEmptyState();
}

// 初始化导航
function initializeNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
}

// 初始化搜索表单
function initializeSearchForm() {
    const searchForm = document.getElementById('searchForm');
    const resetBtn = document.getElementById('resetBtn');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            performSearch();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            resetSearchForm();
        });
    }
}

// 执行搜索
async function performSearch() {
    const formData = new FormData(document.getElementById('searchForm'));
    const searchParams = Object.fromEntries(formData.entries());
    
    // 验证必填字段
    if (!searchParams.searchKeyword.trim()) {
        showNotification('请输入搜索关键词', 'warning');
        return;
    }

    // 显示加载状态
    showLoadingState();
    hideEmptyState();
    hideResultsSection();

    try {
        // 调用后端API
        const response = await fetch('/.netlify/functions/creators-search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchParams)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (result.success && result.data) {
            searchResults = result.data;
            currentPage = 1;
            displaySearchResults();
            showNotification(`找到 ${searchResults.length} 个创作者`, 'success');
        } else {
            throw new Error(result.error || '搜索失败');
        }

    } catch (error) {
        console.error('搜索创作者失败:', error);
        
        // 如果API调用失败，使用模拟数据
        searchResults = generateMockData(searchParams);
        currentPage = 1;
        displaySearchResults();
        showNotification(`找到 ${searchResults.length} 个创作者 (演示数据)`, 'info');
    }
}

// 生成模拟数据
function generateMockData(params) {
    const mockCreators = [];
    const keywords = params.searchKeyword.toLowerCase();
    const count = Math.floor(Math.random() * 20) + 10; // 10-30个结果

    for (let i = 0; i < count; i++) {
        const creator = {
            search_keyword: params.searchKeyword,
            nickname: `${keywords}达人${i + 1}`,
            unique_id: `creator_${Date.now()}_${i}`,
            follower_count: Math.floor(Math.random() * 1000000) + 1000,
            total_video_count: Math.floor(Math.random() * 500) + 10,
            total_likes_count: Math.floor(Math.random() * 5000000) + 10000,
            tiktok_account_url: `https://tiktok.com/@creator${i}`,
            tiktok_account_bio_description: `专注于${keywords}内容创作，分享有趣实用的${keywords}知识`,
            bio_link_url: `https://linktr.ee/creator${i}`,
            language: ['zh', 'en', 'ja', 'ko'][Math.floor(Math.random() * 4)],
            latest_video_link: `https://tiktok.com/@creator${i}/video/1`,
            latest_video_play_count: Math.floor(Math.random() * 1000000) + 1000,
            second_latest_video_link: `https://tiktok.com/@creator${i}/video/2`,
            second_latest_video_play_count: Math.floor(Math.random() * 800000) + 1000,
            third_latest_video_link: `https://tiktok.com/@creator${i}/video/3`,
            third_latest_video_play_count: Math.floor(Math.random() * 600000) + 1000,
            fourth_latest_video_link: `https://tiktok.com/@creator${i}/video/4`,
            fourth_latest_video_play_count: Math.floor(Math.random() * 400000) + 1000,
            fifth_latest_video_link: `https://tiktok.com/@creator${i}/video/5`,
            fifth_latest_video_play_count: Math.floor(Math.random() * 200000) + 1000,
            days_since_last_video: Math.floor(Math.random() * 30) + 1,
            avg_video_play_count: Math.floor(Math.random() * 500000) + 10000,
            median_view_count: Math.floor(Math.random() * 300000) + 5000,
            expected_price: Math.floor(Math.random() * 5000) + 100,
            email: `creator${i}@example.com`,
            // 添加头像和视频预览
            avatar_url: `https://picsum.photos/200/200?random=${i}`,
            video_cover_url: `https://picsum.photos/400/300?random=${i + 100}`,
            video_play_url: `https://sample-videos.com/zip/10/mp4/SampleVideo_${100 + i}.mp4`
        };

        // 应用筛选条件
        if (params.country && params.country !== '') {
            creator.country = params.country;
        }
        if (params.language && params.language !== '') {
            creator.language = params.language;
        }

        mockCreators.push(creator);
    }

    return mockCreators;
}

// 显示搜索结果
function displaySearchResults() {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = searchResults.slice(startIndex, endIndex);

    const tableBody = document.getElementById('resultsTableBody');
    const countNumber = document.getElementById('countNumber');

    // 更新结果数量
    countNumber.textContent = searchResults.length;

    // 清空表格
    tableBody.innerHTML = '';

    // 生成表格行
    pageData.forEach(creator => {
        const row = createCreatorRow(creator);
        tableBody.appendChild(row);
    });

    // 更新分页
    updatePagination();

    // 显示结果区域
    showResultsSection();
    hideLoadingState();
}

// 创建创作者表格行
function createCreatorRow(creator) {
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td>
            <div class="creator-info">
                <div class="creator-avatar">
                    ${creator.avatar_url ? 
                        `<img src="${creator.avatar_url}" alt="${creator.nickname}" onload="this.style.opacity=1" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'" style="opacity:0; transition: opacity 0.3s ease;">
                         <i class="fas fa-user" style="display:none;"></i>` : 
                        `<i class="fas fa-user"></i>`
                    }
                </div>
                <div class="creator-details">
                    <h4>${creator.nickname}</h4>
                    <p>${creator.tiktok_account_bio_description.substring(0, 50)}...</p>
                    <span class="creator-id">${creator.unique_id}</span>
                </div>
            </div>
        </td>
        <td class="data-cell">
            <div class="data-value">${formatNumber(creator.follower_count)}</div>
            <div class="data-label">粉丝数</div>
            <div class="data-value">${formatNumber(creator.total_likes_count)}</div>
            <div class="data-label">总点赞数</div>
        </td>
        <td class="data-cell">
            <div class="data-value">${creator.total_video_count}</div>
            <div class="data-label">视频总数</div>
            <div class="data-value">${creator.days_since_last_video}天</div>
            <div class="data-label">最新视频</div>
        </td>
        <td>
            <div class="video-links">
                <div class="video-link-with-preview">
                    <div class="video-preview" onclick="playVideoPreview('${creator.video_play_url}', '${creator.video_cover_url}', this)">
                        ${creator.video_cover_url ? 
                            `<img src="${creator.video_cover_url}" alt="视频封面" onload="this.style.opacity=1" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'" style="opacity:0; transition: opacity 0.3s ease;">
                             <div class="video-placeholder" style="display:none;"><i class="fas fa-video"></i></div>` : 
                            `<div class="video-placeholder"><i class="fas fa-video"></i></div>`
                        }
                        <div class="video-play-overlay">
                            <i class="fas fa-play"></i>
                        </div>
                        <div class="video-stats">
                            <span>${formatNumber(creator.latest_video_play_count)}</span>
                        </div>
                    </div>
                    <div class="video-link">
                        <span class="video-count">1</span>
                        <a href="${creator.latest_video_link}" target="_blank" title="${formatNumber(creator.latest_video_play_count)} 播放">
                            最新视频
                        </a>
                    </div>
                </div>
                <div class="video-link">
                    <span class="video-count">2</span>
                    <a href="${creator.second_latest_video_link}" target="_blank" title="${formatNumber(creator.second_latest_video_play_count)} 播放">
                        第二新视频
                    </a>
                </div>
                <div class="video-link">
                    <span class="video-count">3</span>
                    <a href="${creator.third_latest_video_link}" target="_blank" title="${formatNumber(creator.third_latest_video_play_count)} 播放">
                        第三新视频
                    </a>
                </div>
            </div>
        </td>
        <td>
            <div class="contact-info">
                <div class="contact-item">
                    <i class="fas fa-envelope"></i>
                    <a href="mailto:${creator.email}" title="${creator.email}">邮箱</a>
                </div>
                <div class="contact-item">
                    <i class="fas fa-link"></i>
                    <a href="${creator.bio_link_url}" target="_blank">个人链接</a>
                </div>
                <div class="contact-item">
                    <i class="fas fa-tiktok"></i>
                    <a href="${creator.tiktok_account_url}" target="_blank">TikTok主页</a>
                </div>
            </div>
        </td>
        <td>
            <div class="action-buttons">
                <button class="action-btn primary" onclick="viewCreatorDetails('${creator.unique_id}')">
                    <i class="fas fa-eye"></i>
                    详情
                </button>
                <button class="action-btn secondary" onclick="contactCreator('${creator.unique_id}')">
                    <i class="fas fa-envelope"></i>
                    联系
                </button>
            </div>
        </td>
    `;

    return row;
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

// 重置搜索表单
function resetSearchForm() {
    document.getElementById('searchForm').reset();
    showEmptyState();
    hideResultsSection();
}

// 初始化模态框
function initializeModal() {
    const modal = document.getElementById('creatorModal');
    const closeBtn = document.getElementById('modalClose');

    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            hideModal();
        });
    }

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideModal();
            }
        });
    }
}

// 显示模态框
function showModal() {
    const modal = document.getElementById('creatorModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// 隐藏模态框
function hideModal() {
    const modal = document.getElementById('creatorModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// 查看创作者详情
function viewCreatorDetails(creatorId) {
    const creator = searchResults.find(c => c.unique_id === creatorId);
    if (!creator) return;

    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <div class="creator-detail-grid">
            <div class="detail-section">
                <h4><i class="fas fa-user"></i> 基本信息</h4>
                <div class="detail-item">
                    <span class="detail-label">昵称</span>
                    <span class="detail-value">${creator.nickname}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">唯一ID</span>
                    <span class="detail-value">${creator.unique_id}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">个人简介</span>
                    <span class="detail-value">${creator.tiktok_account_bio_description}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">语言设置</span>
                    <span class="detail-value">${getLanguageName(creator.language)}</span>
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-chart-line"></i> 数据统计</h4>
                <div class="detail-item">
                    <span class="detail-label">粉丝数</span>
                    <span class="detail-value">${formatNumber(creator.follower_count)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">视频总数</span>
                    <span class="detail-value">${creator.total_video_count}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">总点赞数</span>
                    <span class="detail-value">${formatNumber(creator.total_likes_count)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">平均播放量</span>
                    <span class="detail-value">${formatNumber(creator.avg_video_play_count)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">中位数播放量</span>
                    <span class="detail-value">${formatNumber(creator.median_view_count)}</span>
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-video"></i> 最新视频</h4>
                <div class="detail-item">
                    <span class="detail-label">最新视频播放量</span>
                    <span class="detail-value">${formatNumber(creator.latest_video_play_count)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">第二新视频播放量</span>
                    <span class="detail-value">${formatNumber(creator.second_latest_video_play_count)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">第三新视频播放量</span>
                    <span class="detail-value">${formatNumber(creator.third_latest_video_play_count)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">最新视频发布天数</span>
                    <span class="detail-value">${creator.days_since_last_video}天</span>
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-dollar-sign"></i> 商业信息</h4>
                <div class="detail-item">
                    <span class="detail-label">预期价格</span>
                    <span class="detail-value">¥${creator.expected_price}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">邮箱地址</span>
                    <span class="detail-value">${creator.email}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">搜索关键词</span>
                    <span class="detail-value">${creator.search_keyword}</span>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 24px; text-align: center;">
            <a href="${creator.tiktok_account_url}" target="_blank" class="btn-primary">
                <i class="fas fa-external-link-alt"></i>
                访问TikTok主页
            </a>
            <a href="mailto:${creator.email}" class="btn-outline" style="margin-left: 12px;">
                <i class="fas fa-envelope"></i>
                发送邮件
            </a>
        </div>
    `;

    showModal();
}

// 联系创作者
function contactCreator(creatorId) {
    const creator = searchResults.find(c => c.unique_id === creatorId);
    if (!creator) return;

    // 这里可以打开联系表单或直接发送邮件
    window.open(`mailto:${creator.email}?subject=合作邀请&body=您好，我对您的${creator.search_keyword}内容很感兴趣，希望有机会合作。`);
}

// 获取语言名称
function getLanguageName(code) {
    const languages = {
        'zh': '中文',
        'en': '英文',
        'ja': '日文',
        'ko': '韩文',
        'fr': '法文',
        'de': '德文',
        'es': '西班牙文',
        'pt': '葡萄牙文',
        'ru': '俄文'
    };
    return languages[code] || code;
}

// 初始化分页
function initializePagination() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                displaySearchResults();
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            const totalPages = Math.ceil(searchResults.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                displaySearchResults();
            }
        });
    }
}

// 更新分页
function updatePagination() {
    const totalPages = Math.ceil(searchResults.length / itemsPerPage);
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (currentPageSpan) currentPageSpan.textContent = currentPage;
    if (totalPagesSpan) totalPagesSpan.textContent = totalPages;
    if (prevBtn) prevBtn.disabled = currentPage <= 1;
    if (nextBtn) nextBtn.disabled = currentPage >= totalPages;
}

// 初始化导出功能
function initializeExport() {
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportData();
        });
    }
}

// 导出数据
function exportData() {
    if (searchResults.length === 0) {
        showNotification('没有数据可导出', 'warning');
        return;
    }

    // 创建CSV内容
    const headers = [
        '搜索关键词', '昵称', '唯一ID', '粉丝数', '视频总数', '总点赞数',
        'TikTok链接', '个人简介', '个人链接', '语言', '最新视频链接',
        '最新视频播放量', '第二新视频链接', '第二新视频播放量',
        '第三新视频链接', '第三新视频播放量', '最新视频发布天数',
        '平均播放量', '中位数播放量', '预期价格', '邮箱'
    ];

    const csvContent = [
        headers.join(','),
        ...searchResults.map(creator => [
            creator.search_keyword,
            creator.nickname,
            creator.unique_id,
            creator.follower_count,
            creator.total_video_count,
            creator.total_likes_count,
            creator.tiktok_account_url,
            creator.tiktok_account_bio_description,
            creator.bio_link_url,
            creator.language,
            creator.latest_video_link,
            creator.latest_video_play_count,
            creator.second_latest_video_link,
            creator.second_latest_video_play_count,
            creator.third_latest_video_link,
            creator.third_latest_video_play_count,
            creator.days_since_last_video,
            creator.avg_video_play_count,
            creator.median_view_count,
            creator.expected_price,
            creator.email
        ].join(','))
    ].join('\n');

    // 下载文件
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `creators_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showNotification('数据导出成功', 'success');
}

// 初始化排序功能
function initializeSorting() {
    const sortBtn = document.getElementById('sortBtn');
    if (sortBtn) {
        sortBtn.addEventListener('click', function() {
            showSortOptions();
        });
    }
}

// 显示排序选项
function showSortOptions() {
    const sortOptions = [
        { field: 'follower_count', label: '粉丝数' },
        { field: 'total_likes_count', label: '总点赞数' },
        { field: 'avg_video_play_count', label: '平均播放量' },
        { field: 'total_video_count', label: '视频总数' },
        { field: 'expected_price', label: '预期价格' },
        { field: 'days_since_last_video', label: '最新视频天数' }
    ];

    const sortMenu = document.createElement('div');
    sortMenu.className = 'sort-menu';
    sortMenu.style.cssText = `
        position: absolute;
        top: 100%;
        right: 0;
        background: white;
        border: 1px solid var(--light-gray);
        border-radius: 8px;
        box-shadow: var(--shadow-md);
        z-index: 1000;
        min-width: 150px;
        padding: 8px 0;
    `;

    sortOptions.forEach(option => {
        const item = document.createElement('div');
        item.style.cssText = `
            padding: 8px 16px;
            cursor: pointer;
            transition: background 0.3s ease;
            font-size: 14px;
        `;
        item.textContent = option.label;
        item.addEventListener('mouseenter', () => {
            item.style.background = 'var(--bg-secondary)';
        });
        item.addEventListener('mouseleave', () => {
            item.style.background = 'transparent';
        });
        item.addEventListener('click', () => {
            sortData(option.field);
            document.body.removeChild(sortMenu);
        });
        sortMenu.appendChild(item);
    });

    // 定位排序菜单
    const sortBtn = document.getElementById('sortBtn');
    sortBtn.style.position = 'relative';
    sortBtn.appendChild(sortMenu);

    // 点击外部关闭
    document.addEventListener('click', function closeSortMenu(e) {
        if (!sortMenu.contains(e.target) && e.target !== sortBtn) {
            if (sortMenu.parentNode) {
                sortMenu.parentNode.removeChild(sortMenu);
            }
            document.removeEventListener('click', closeSortMenu);
        }
    });
}

// 排序数据
function sortData(field) {
    currentSortField = field;
    currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';

    searchResults.sort((a, b) => {
        let aVal = a[field];
        let bVal = b[field];

        if (currentSortOrder === 'asc') {
            return aVal - bVal;
        } else {
            return bVal - aVal;
        }
    });

    currentPage = 1;
    displaySearchResults();
    showNotification(`已按${getSortFieldName(field)}${currentSortOrder === 'asc' ? '升序' : '降序'}排序`, 'success');
}

// 获取排序字段名称
function getSortFieldName(field) {
    const fieldNames = {
        'follower_count': '粉丝数',
        'total_likes_count': '总点赞数',
        'avg_video_play_count': '平均播放量',
        'total_video_count': '视频总数',
        'expected_price': '预期价格',
        'days_since_last_video': '最新视频天数'
    };
    return fieldNames[field] || field;
}

// 显示/隐藏状态函数
function showLoadingState() {
    const loadingContainer = document.getElementById('loadingContainer');
    if (loadingContainer) loadingContainer.style.display = 'block';
}

function hideLoadingState() {
    const loadingContainer = document.getElementById('loadingContainer');
    if (loadingContainer) loadingContainer.style.display = 'none';
}

function showResultsSection() {
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) resultsSection.style.display = 'block';
}

function hideResultsSection() {
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) resultsSection.style.display = 'none';
}

function showEmptyState() {
    const emptyState = document.getElementById('emptyState');
    if (emptyState) emptyState.style.display = 'block';
}

function hideEmptyState() {
    const emptyState = document.getElementById('emptyState');
    if (emptyState) emptyState.style.display = 'none';
}

// 滚动到搜索区域
function scrollToSearch() {
    const searchSection = document.querySelector('.search-section');
    if (searchSection) {
        searchSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: white;
        border-radius: 10px;
        box-shadow: var(--shadow-lg);
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 10000;
        max-width: 300px;
        border-left: 4px solid ${getNotificationColor(type)};
    `;
    
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => notification.style.transform = 'translateX(0)', 100);
    
    // 自动隐藏
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// 获取通知颜色
function getNotificationColor(type) {
    const colors = {
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6'
    };
    return colors[type] || colors.info;
}

// 获取通知图标
function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'error': 'times-circle',
        'info': 'info-circle'
    };
    return icons[type] || icons.info;
}

// 播放视频预览
function playVideoPreview(videoUrl, coverUrl, element) {
    if (!videoUrl) {
        showNotification('暂无视频预览', 'warning');
        return;
    }

    // 创建视频预览模态框
    const videoModal = document.createElement('div');
    videoModal.className = 'video-preview-modal';
    videoModal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;

    const videoContainer = document.createElement('div');
    videoContainer.style.cssText = `
        position: relative;
        max-width: 90%;
        max-height: 90%;
        background: black;
        border-radius: 10px;
        overflow: hidden;
    `;

    const video = document.createElement('video');
    video.style.cssText = `
        width: 100%;
        height: auto;
        max-height: 80vh;
    `;
    video.src = videoUrl;
    video.controls = true;
    video.autoplay = true;
    video.poster = coverUrl;

    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.style.cssText = `
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        cursor: pointer;
        z-index: 10001;
        font-size: 16px;
        transition: background 0.3s ease;
    `;

    closeBtn.addEventListener('click', closeVideoModal);
    closeBtn.addEventListener('mouseenter', () => {
        closeBtn.style.background = 'rgba(0, 0, 0, 0.8)';
    });
    closeBtn.addEventListener('mouseleave', () => {
        closeBtn.style.background = 'rgba(0, 0, 0, 0.5)';
    });

    videoContainer.appendChild(video);
    videoContainer.appendChild(closeBtn);
    videoModal.appendChild(videoContainer);
    document.body.appendChild(videoModal);

    // 显示动画
    setTimeout(() => {
        videoModal.style.opacity = '1';
    }, 10);

    // 点击外部关闭
    videoModal.addEventListener('click', function(e) {
        if (e.target === videoModal) {
            closeVideoModal();
        }
    });

    // 阻止body滚动
    document.body.style.overflow = 'hidden';

    function closeVideoModal() {
        videoModal.style.opacity = '0';
        document.body.style.overflow = 'auto';
        setTimeout(() => {
            if (videoModal.parentNode) {
                document.body.removeChild(videoModal);
            }
        }, 300);
    }

    // ESC键关闭
    function handleEscKey(e) {
        if (e.key === 'Escape') {
            closeVideoModal();
            document.removeEventListener('keydown', handleEscKey);
        }
    }
    document.addEventListener('keydown', handleEscKey);
}

// ================================
// 认证相关功能
// ================================

// 检查认证状态
function checkAuthStatus() {
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    
    if (!token || !userData) {
        return false;
    }
    
    // 检查token是否过期（简单检查）
    try {
        const user = JSON.parse(userData);
        return true;
    } catch (e) {
        return false;
    }
}

// 获取认证token
function getAuthToken() {
    return localStorage.getItem('auth_token');
}

// 获取用户数据
function getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

// 显示需要认证的消息
function showAuthRequiredMessage() {
    const container = document.querySelector('.container');
    if (container) {
        container.innerHTML = `
            <div class="auth-required-message">
                <div class="auth-card">
                    <div class="auth-icon">
                        <i class="fas fa-lock"></i>
                    </div>
                    <h2>需要登录</h2>
                    <p>请先登录您的账户以使用创作者搜索功能</p>
                    <div class="auth-actions">
                        <a href="./auth.html" class="btn btn-primary">立即登录</a>
                        <a href="./index.html" class="btn btn-secondary">返回首页</a>
                    </div>
                </div>
            </div>
            <style>
                .auth-required-message {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 60vh;
                    padding: 2rem;
                }
                
                .auth-card {
                    background: white;
                    border-radius: 20px;
                    padding: 3rem;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    max-width: 400px;
                    width: 100%;
                }
                
                .auth-icon {
                    font-size: 3rem;
                    color: #FFD700;
                    margin-bottom: 1.5rem;
                }
                
                .auth-card h2 {
                    color: #333;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                }
                
                .auth-card p {
                    color: #666;
                    margin-bottom: 2rem;
                    line-height: 1.6;
                }
                
                .auth-actions {
                    display: flex;
                    gap: 1rem;
                    justify-content: center;
                    flex-wrap: wrap;
                }
                
                .auth-actions .btn {
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: 500;
                    transition: all 0.3s ease;
                }
                
                .auth-actions .btn-primary {
                    background: linear-gradient(135deg, #FFD700, #FFA500);
                    color: #333;
                }
                
                .auth-actions .btn-secondary {
                    background: transparent;
                    color: #666;
                    border: 2px solid #e9ecef;
                }
                
                .auth-actions .btn:hover {
                    transform: translateY(-2px);
                }
            </style>
        `;
    }
}

// 更新API调用以包含认证头
function makeAuthenticatedRequest(url, options = {}) {
    const token = getAuthToken();
    
    if (!token) {
        throw new Error('No authentication token found');
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    return fetch(url, {
        ...options,
        headers
    });
}
