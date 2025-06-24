<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { getPollData, submitVote } from './services/api';
import PollChart from './components/PollChart.vue';
import { VotingWebSocket } from './services/websocket';

const poll = ref(null);
const selectedOption = ref(null);
const loading = ref(false);
const error = ref(null);
const socket = ref(null);

// 获取初始投票数据
const fetchPollData = async () => {
    try {
        loading.value = true;
        const response = await getPollData();
        poll.value = response.data;
    } catch (err) {
        error.value = '获取投票数据失败';
    } finally {
        loading.value = false;
    }
};

// 处理投票
const handleVote = async () => {
    if (!selectedOption.value) return;
    
    try {
        loading.value = true;
        await submitVote(selectedOption.value);
        selectedOption.value = null;
    } catch (err) {
        error.value = '投票失败';
    } finally {
        loading.value = false;
    }
};

// 处理WebSocket消息
const handleWebSocketMessage = (data) => {
  console.log('收到WebSocket消息:', data);
  
  if (poll.value && data.poll_id === poll.value.id) {
    // 创建新的选项数组，确保触发Vue响应式更新
    const updatedOptions = [...data.options];
    
    // 创建新的投票对象，确保触发Vue响应式更新
    poll.value = {
      ...poll.value,
      options: updatedOptions
    };
    
    console.log('更新后的投票数据:', poll.value);
  }
};


// 初始化WebSocket
const initWebSocket = () => {
    const wsUrl = `ws://${window.location.hostname}:8000/ws/poll`;
    socket.value = new VotingWebSocket(wsUrl, handleWebSocketMessage);
    socket.value.connect();
};

onMounted(() => {
    fetchPollData();
    initWebSocket();
});

onUnmounted(() => {
    if (socket.value) {
        socket.value.disconnect();
    }
});
</script>

<template>
    <div class="container">
        <h1>实时投票系统</h1>
        
        <div v-if="loading" class="loading">加载中...</div>
        <div v-if="error" class="error">{{ error }}</div>
        
        <div v-if="poll" class="poll-container">
            <h2>{{ poll.title }}</h2>
            
            <form @submit.prevent="handleVote">
                <div v-for="option in poll.options" :key="option.id" class="option">
                    <input 
                        type="radio" 
                        :id="`option-${option.id}`" 
                        :value="option.id" 
                        v-model="selectedOption"
                    >
                    <label :for="`option-${option.id}`">{{ option.text }}</label>
                </div>
                
                <button type="submit" :disabled="!selectedOption">提交投票</button>
            </form>
            
            <PollChart :poll-data="poll" />
        </div>
    </div>
</template>

<style>
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.container {
    padding: 20px;
    border: 1px solid #eee;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.poll-container {
    margin-top: 20px;
}

.option {
    margin: 10px 0;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    margin-top: 15px;
    padding: 10px 20px;
    background-color: #42b883;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:disabled {
    background-color: #ccc;
}

.loading, .error {
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
}

.loading {
    background-color: #f0f9ff;
    color: #0c6efd;
}

.error {
    background-color: #fff0f0;
    color: #dc3545;
}
</style>