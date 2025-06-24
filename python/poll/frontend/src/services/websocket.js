export class VotingWebSocket {
    constructor(url, onMessage) {
        this.url = url;
        this.onMessage = onMessage;
        this.socket = null;
    }

    connect() {
        this.socket = new WebSocket(this.url);
        
        this.socket.onopen = () => {
            console.log('WebSocket connected');
        };
        
        this.socket.onmessage = (event) => {
            this.onMessage(JSON.parse(event.data));
        };
        
        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
        };
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}