const axios = require('axios');

// TikHub API配置
const API_KEY = process.env.TIKHUB_API_KEY || "w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA==";
const BASE_URL = "https://api.tikhub.io";

const API_HEADERS = {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
    "User-Agent": "Beee-Media-Web/1.0"
};

// Helper functions
function extractBioLink(signature) {
    if (!signature) return "";
    const urlPattern = /https?:\/\/[^\s]+/;
    const match = signature.match(urlPattern);
    return match ? match[0] : "";
}

function extractEmail(signature) {
    if (!signature) return "";
    const emailPattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;
    const match = signature.match(emailPattern);
    return match ? match[0] : "";
}

function detectLanguage(text) {
    if (!text) return "zh";
    const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    const englishChars = (text.match(/[a-zA-Z]/g) || []).length;
    return chineseChars > englishChars ? "zh" : "en";
}

function calculateDaysSinceLastVideo(createTime) {
    if (!createTime) return 0;
    const now = Date.now();
    const videoTime = createTime * 1000;
    return Math.floor((now - videoTime) / (1000 * 60 * 60 * 24));
}

function calculateAvgPlayCount(awemeInfo) {
    const stats = awemeInfo.statistics || {};
    return stats.play_count || 0;
}

function calculateMedianViewCount(awemeInfo) {
    const stats = awemeInfo.statistics || {};
    return stats.play_count || 0;
}

function calculateExpectedPrice(followerCount, totalLikes) {
    const basePrice = Math.floor(followerCount / 1000) * 10;
    const engagementBonus = Math.floor(totalLikes / 10000) * 5;
    return Math.max(100, basePrice + engagementBonus);
}

function applyFilters(creator, filters) {
    // 粉丝数范围筛选
    if (filters.followerRange) {
        const followerCount = creator.follower_count || 0;
        const range = filters.followerRange;
        if (range === '0-10000' && followerCount >= 10000) return false;
        if (range === '10000-100000' && (followerCount < 10000 || followerCount >= 100000)) return false;
        if (range === '100000-1000000' && (followerCount < 100000 || followerCount >= 1000000)) return false;
        if (range === '1000000-10000000' && (followerCount < 1000000 || followerCount >= 10000000)) return false;
        if (range === '10000000-999999999' && followerCount < 10000000) return false;
    }
    
    return true;
}

async function searchCreatorsFromTikHub(keyword, filters) {
    try {
        const url = `${BASE_URL}/api/v1/tiktok/app/v3/fetch_general_search_result`;
        const params = {
            keyword: keyword,
            offset: 0,
            count: 50,
            sort_type: 0,
            publish_time: 0
        };

        console.log('🔍 调用TikHub API搜索:', keyword);
        
        const response = await axios.get(url, { 
            headers: API_HEADERS, 
            params: params,
            timeout: 30000 
        });

        if (response.status !== 200) {
            throw new Error(`API请求失败: ${response.status}`);
        }

        const result = response.data;
        const data = result.data || {};
        
        if (data.status_code !== 0) {
            throw new Error(`TikHub API错误: ${data.status_msg || 'Unknown error'}`);
        }

        const items = data.data || [];
        console.log('📊 找到搜索结果:', items.length);

        const creators = [];
        const creatorMap = {};

        for (const item of items) {
            if (item.type === 1 && item.aweme_info) {
                const awemeInfo = item.aweme_info;
                const author = awemeInfo.author || {};

                if (!author) continue;

                const uniqueId = author.unique_id || author.sec_uid || author.nickname || "";
                if (!uniqueId || creatorMap[uniqueId]) continue;

                // 提取头像和视频预览URL
                let avatarUrl = "";
                let videoCoverUrl = "";
                let videoPlayUrl = "";

                if (author.avatar_larger && author.avatar_larger.url_list) {
                    avatarUrl = author.avatar_larger.url_list[0] || "";
                } else if (author.avatar_medium && author.avatar_medium.url_list) {
                    avatarUrl = author.avatar_medium.url_list[0] || "";
                }

                const videoInfo = awemeInfo.video || {};
                if (videoInfo.cover && videoInfo.cover.url_list) {
                    videoCoverUrl = videoInfo.cover.url_list[0] || "";
                }
                if (videoInfo.play_addr && videoInfo.play_addr.url_list) {
                    videoPlayUrl = videoInfo.play_addr.url_list[0] || "";
                }

                const statistics = awemeInfo.statistics || {};
                
                const creator = {
                    search_keyword: keyword,
                    nickname: author.nickname || "",
                    unique_id: uniqueId,
                    follower_count: author.follower_count || 0,
                    total_video_count: author.aweme_count || 0,
                    total_likes_count: author.total_favorited || 0,
                    tiktok_account_url: `https://tiktok.com/@${author.unique_id || ''}`,
                    tiktok_account_bio_description: author.signature || "",
                    bio_link_url: extractBioLink(author.signature || ""),
                    language: detectLanguage(author.signature || ""),
                    latest_video_link: `https://tiktok.com/@${author.unique_id || ''}/video/${awemeInfo.aweme_id || ''}`,
                    latest_video_play_count: statistics.play_count || 0,
                    second_latest_video_link: "",
                    second_latest_video_play_count: 0,
                    third_latest_video_link: "",
                    third_latest_video_play_count: 0,
                    fourth_latest_video_link: "",
                    fourth_latest_video_play_count: 0,
                    fifth_latest_video_link: "",
                    fifth_latest_video_play_count: 0,
                    days_since_last_video: calculateDaysSinceLastVideo(awemeInfo.create_time || 0),
                    avg_video_play_count: calculateAvgPlayCount(awemeInfo),
                    median_view_count: calculateMedianViewCount(awemeInfo),
                    expected_price: calculateExpectedPrice(author.follower_count || 0, author.total_favorited || 0),
                    email: extractEmail(author.signature || ""),
                    avatar_url: avatarUrl,
                    video_cover_url: videoCoverUrl,
                    video_play_url: videoPlayUrl
                };

                if (applyFilters(creator, filters)) {
                    creators.push(creator);
                    creatorMap[uniqueId] = true;
                }
            }
        }

        console.log('✅ 找到符合条件的创作者:', creators.length);
        return creators;

    } catch (error) {
        console.error('TikHub API调用失败:', error.message);
        throw error;
    }
}

exports.handler = async (event, context) => {
    // 处理CORS预检请求
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const body = JSON.parse(event.body || '{}');
        const searchKeyword = (body.searchKeyword || '').trim();

        if (!searchKeyword) {
            return {
                statusCode: 400,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ error: '请输入搜索关键词' })
            };
        }

        console.log('🔍 搜索创作者:', searchKeyword);

        const filters = {
            country: body.country || '',
            followerRange: body.followerRange || '',
            language: body.language || '',
            videoCount: body.videoCount || '',
            daysSinceLastVideo: body.daysSinceLastVideo || '',
            avgPlayCount: body.avgPlayCount || ''
        };

        const creators = await searchCreatorsFromTikHub(searchKeyword, filters);

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                success: true,
                data: creators,
                total: creators.length,
                keyword: searchKeyword,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('搜索创作者失败:', error);
        
        return {
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ error: error.message })
        };
    }
};
