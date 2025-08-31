const axios = require('axios');

// TikHub API配置
const API_KEY = process.env.TIKHUB_API_KEY || "w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA==";
const BASE_URL = "https://api.tikhub.io";

const API_HEADERS = {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
    "User-Agent": "Beee-Media-Web/1.0"
};

async function fetchCountryTrends(country) {
    try {
        const url = `${BASE_URL}/api/v1/twitter/web/fetch_trending`;
        const params = { country: country };

        console.log('🔍 获取趋势数据:', country);
        
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

        const trends = data.data || [];
        console.log('📊 找到趋势数据:', trends.length);

        return trends.map(trend => ({
            name: trend.name || '',
            context: trend.context || '',
            description: trend.description || '',
            volume: trend.volume || 0
        }));

    } catch (error) {
        console.error('获取趋势数据失败:', error.message);
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
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'GET') {
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
        const country = event.queryStringParameters?.country || 'UnitedStates';
        
        console.log('🔍 获取趋势数据:', country);

        const trends = await fetchCountryTrends(country);

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                success: true,
                data: trends,
                total: trends.length,
                country: country,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('获取趋势数据失败:', error);
        
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
