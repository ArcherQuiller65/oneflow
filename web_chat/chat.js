/**
 * OneFlow AI Chat Interface
 * Handles chat interactions and workflow generation
 */

class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.nodesInfo = document.getElementById('nodesInfo');
        this.statusBar = document.getElementById('statusBar');
        this.nodeCount = document.getElementById('nodeCount');
        
        this.isLoading = false;
        this.nodesData = null;
        
        this.init();
    }
    
    init() {
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Load initial data
        this.loadNodesInfo();
        this.checkStatus();
    }
    
    async loadNodesInfo() {
        try {
            const response = await fetch('/api/chat/nodes_info');
            const result = await response.json();
            
            if (result.success) {
                this.nodesData = result.data;
                this.displayNodesInfo(result.data);
                this.nodeCount.textContent = `${result.data.total_nodes} nodes`;
            } else {
                this.showError('Failed to load nodes information');
            }
        } catch (error) {
            console.error('Error loading nodes info:', error);
            this.showError('Failed to connect to server');
        }
    }
    
    displayNodesInfo(data) {
        const categories = data.categories;
        let html = '';
        
        for (const [categoryName, categoryData] of Object.entries(categories)) {
            html += `
                <div class="category">
                    <div class="category-title">${categoryName} (${categoryData.count})</div>
            `;
            
            for (const node of categoryData.nodes) {
                html += `
                    <div class="node-item">
                        <div class="node-name">${node.display_name}</div>
                        <div class="node-desc">${node.description || 'No description available'}</div>
                    </div>
                `;
            }
            
            html += '</div>';
        }
        
        this.nodesInfo.innerHTML = html;
    }
    
    async checkStatus() {
        try {
            const response = await fetch('/api/chat/status');
            const result = await response.json();
            
            if (result.success) {
                this.statusBar.innerHTML = `
                    Ready • ${result.nodes_loaded} nodes available • ${result.chat_entries} chat entries
                `;
            }
        } catch (error) {
            console.error('Error checking status:', error);
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        this.messageInput.value = '';
        
        // Show loading
        this.setLoading(true);
        const loadingMessageId = this.addMessage('assistant', '', true);
        
        try {
            const response = await fetch('/api/chat/generate_workflow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    request: message
                })
            });
            
            const result = await response.json();
            
            // Remove loading message
            this.removeMessage(loadingMessageId);
            
            if (result.success) {
                this.addWorkflowMessage(result.workflow);
            } else {
                this.addMessage('assistant', `❌ Error: ${result.error}`);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.removeMessage(loadingMessageId);
            this.addMessage('assistant', '❌ Failed to connect to server. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessage(sender, content, isLoading = false) {
        const messageId = Date.now() + Math.random();
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.dataset.messageId = messageId;
        
        if (isLoading) {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="loading">
                        <div class="spinner"></div>
                        Generating workflow...
                    </div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div>${content}</div>
                    <div class="message-time">${new Date().toLocaleTimeString()}</div>
                </div>
            `;
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageId;
    }
    
    removeMessage(messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement) {
            messageElement.remove();
        }
    }
    
    addWorkflowMessage(workflowData) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant';
        
        let workflowHtml = '';
        if (workflowData.description) {
            workflowHtml += `<div><strong>📋 Workflow:</strong> ${workflowData.description}</div>`;
        }
        
        if (workflowData.workflow && workflowData.workflow.length > 0) {
            workflowHtml += '<div class="workflow-display">';
            workflowHtml += '<div><strong>🔧 Steps:</strong></div>';
            
            workflowData.workflow.forEach((step, index) => {
                const operation = step.operation;
                const params = step.params;
                
                let stepDescription = '';
                if (operation === 'add_node') {
                    stepDescription = `Add ${params.node_id} node`;
                    if (params.node_params && Object.keys(params.node_params).length > 0) {
                        const paramsList = Object.entries(params.node_params)
                            .map(([key, value]) => `${key}: ${JSON.stringify(value)}`)
                            .join(', ');
                        stepDescription += ` (${paramsList})`;
                    }
                } else if (operation === 'link_node') {
                    stepDescription = `Connect ${params.source_node_id}.${params.source_output} → ${params.target_node_id}.${params.target_input}`;
                } else if (operation === 'set_param') {
                    stepDescription = `Set ${params.node_id}.${params.param_name} = ${JSON.stringify(params.param_value)}`;
                }
                
                workflowHtml += `
                    <div class="workflow-step">
                        <strong>${index + 1}.</strong> ${stepDescription}
                    </div>
                `;
            });
            
            workflowHtml += '</div>';
        }
        
        // Add nodes used summary
        if (workflowData.nodes_used && workflowData.nodes_used.length > 0) {
            workflowHtml += `
                <div style="margin-top: 10px;">
                    <strong>🎯 Nodes used:</strong> ${workflowData.nodes_used.join(', ')}
                </div>
            `;
        }
        
        // Add validation button
        workflowHtml += `
            <div style="margin-top: 15px;">
                <button onclick="chatInterface.validateWorkflow(${JSON.stringify(workflowData).replace(/"/g, '&quot;')})" 
                        style="background: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    ✅ Validate Workflow
                </button>
                <button onclick="chatInterface.showRawWorkflow(${JSON.stringify(workflowData).replace(/"/g, '&quot;')})" 
                        style="background: #6c757d; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; margin-left: 10px;">
                    📄 Show Raw JSON
                </button>
            </div>
        `;
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${workflowHtml}
                <div class="message-time">${new Date().toLocaleTimeString()}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    async validateWorkflow(workflowData) {
        try {
            const response = await fetch('/api/chat/validate_workflow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    workflow: workflowData
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                const validation = result.validation;
                let message = '';
                
                if (validation.valid) {
                    message = '✅ Workflow validation passed! The workflow structure is correct.';
                } else {
                    message = '❌ Workflow validation failed:\n';
                    validation.errors.forEach(error => {
                        message += `• ${error}\n`;
                    });
                    
                    if (validation.warnings.length > 0) {
                        message += '\n⚠️ Warnings:\n';
                        validation.warnings.forEach(warning => {
                            message += `• ${warning}\n`;
                        });
                    }
                }
                
                this.addMessage('assistant', message);
            } else {
                this.addMessage('assistant', `❌ Validation error: ${result.error}`);
            }
        } catch (error) {
            console.error('Error validating workflow:', error);
            this.addMessage('assistant', '❌ Failed to validate workflow');
        }
    }
    
    showRawWorkflow(workflowData) {
        const jsonString = JSON.stringify(workflowData, null, 2);
        const message = `
            <div><strong>📄 Raw Workflow JSON:</strong></div>
            <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 10px; margin-top: 10px; font-family: monospace; font-size: 0.85em; white-space: pre-wrap; max-height: 300px; overflow-y: auto;">${jsonString}</div>
        `;
        this.addMessage('assistant', message);
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.sendButton.disabled = loading;
        this.messageInput.disabled = loading;
        
        if (loading) {
            this.sendButton.textContent = 'Generating...';
        } else {
            this.sendButton.textContent = 'Send';
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showError(message) {
        this.nodesInfo.innerHTML = `
            <div class="error-message">
                ❌ ${message}
            </div>
        `;
    }
}

// Initialize chat interface when page loads
let chatInterface;
document.addEventListener('DOMContentLoaded', () => {
    chatInterface = new ChatInterface();
});