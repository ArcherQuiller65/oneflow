/**
 * OneFlow AI Chat Widget
 * Integrates AI chat functionality directly into ComfyUI interface
 */

class OneFlowChatWidget {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.chatHistory = [];
        this.init();
    }

    init() {
        console.log('OneFlow Chat Widget: Initializing...');
        this.createChatWidget();
        this.setupEventListeners();
        this.loadChatHistory();
        console.log('OneFlow Chat Widget: Initialization complete');
    }

    createChatWidget() {
        console.log('OneFlow Chat Widget: Creating widget DOM elements...');
        // Create chat widget container
        const chatWidget = document.createElement('div');
        chatWidget.id = 'oneflow-chat-widget';
        chatWidget.className = 'oneflow-chat-widget';
        chatWidget.innerHTML = `
            <div class="chat-toggle" id="chat-toggle">
                <div class="chat-icon">🤖</div>
                <div class="chat-badge" id="chat-badge" style="display: none;">1</div>
            </div>
            <div class="chat-panel" id="chat-panel">
                <div class="chat-header">
                    <div class="chat-title">
                        <span class="chat-icon">🌊</span>
                        OneFlow AI Assistant
                    </div>
                    <div class="chat-controls">
                        <button class="chat-minimize" id="chat-minimize">−</button>
                        <button class="chat-close" id="chat-close">×</button>
                    </div>
                </div>
                <div class="chat-content">
                    <div class="chat-messages" id="chat-messages">
                        <div class="welcome-message">
                            <div class="message-avatar">🤖</div>
                            <div class="message-content">
                                <p>Hi! I'm your OneFlow AI assistant. I can help you create workflows by describing what you want to do in natural language.</p>
                                <p>Try saying something like: "Generate an image of a sunset and display it" or "Create a story about cats"</p>
                            </div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <div class="chat-input-wrapper">
                            <textarea 
                                id="chat-input" 
                                placeholder="Describe the workflow you want to create..."
                                rows="2"
                            ></textarea>
                            <button id="chat-send" class="chat-send-btn">
                                <span class="send-icon">➤</span>
                            </button>
                        </div>
                        <div class="chat-status" id="chat-status">
                            <span class="status-indicator">●</span>
                            <span class="status-text">Ready</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        console.log('OneFlow Chat Widget: Appending widget to document.body...');
        document.body.appendChild(chatWidget);
        console.log('OneFlow Chat Widget: Widget appended successfully');
    }

    setupEventListeners() {
        const toggle = document.getElementById('chat-toggle');
        const panel = document.getElementById('chat-panel');
        const minimize = document.getElementById('chat-minimize');
        const close = document.getElementById('chat-close');
        const input = document.getElementById('chat-input');
        const send = document.getElementById('chat-send');

        toggle.addEventListener('click', () => this.toggleChat());
        minimize.addEventListener('click', () => this.minimizeChat());
        close.addEventListener('click', () => this.closeChat());
        send.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        input.addEventListener('input', () => {
            this.autoResizeTextarea(input);
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const panel = document.getElementById('chat-panel');
        const badge = document.getElementById('chat-badge');
        
        if (this.isOpen) {
            panel.style.display = 'flex';
            badge.style.display = 'none';
            setTimeout(() => {
                panel.classList.add('open');
                document.getElementById('chat-input').focus();
            }, 10);
        } else {
            panel.classList.remove('open');
            setTimeout(() => {
                panel.style.display = 'none';
            }, 300);
        }
    }

    minimizeChat() {
        this.isOpen = false;
        const panel = document.getElementById('chat-panel');
        panel.classList.remove('open');
        setTimeout(() => {
            panel.style.display = 'none';
        }, 300);
    }

    closeChat() {
        this.minimizeChat();
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message || this.isLoading) return;

        this.isLoading = true;
        this.updateStatus('Generating workflow...', 'loading');
        
        // Add user message to chat
        this.addMessage('user', message);
        input.value = '';
        input.style.height = 'auto';

        try {
            // Get current workflow from canvas
            const currentWorkflow = this.getCurrentWorkflow();
            
            // Send request to generate workflow
            const response = await fetch('/api/chat/generate_workflow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    request: message,
                    current_workflow: currentWorkflow
                })
            });

            const result = await response.json();

            if (result.success) {
                this.addMessage('assistant', 'I\'ve generated a workflow for you!', result.workflow);
                this.executeWorkflow(result.workflow);
                this.updateStatus('Workflow generated successfully', 'success');
            } else {
                this.addMessage('assistant', `Sorry, I couldn't generate the workflow: ${result.error}`);
                this.updateStatus('Error generating workflow', 'error');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('assistant', 'Sorry, there was an error processing your request.');
            this.updateStatus('Connection error', 'error');
        } finally {
            this.isLoading = false;
            setTimeout(() => {
                this.updateStatus('Ready', 'ready');
            }, 3000);
        }
    }

    addMessage(sender, content, workflow = null) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = sender === 'user' ? '👤' : '🤖';
        
        let workflowHtml = '';
        if (workflow) {
            workflowHtml = `
                <div class="workflow-preview">
                    <div class="workflow-header">
                        <span class="workflow-icon">⚡</span>
                        <span class="workflow-title">${workflow.description || 'Generated Workflow'}</span>
                    </div>
                    <div class="workflow-details">
                        <div class="workflow-stat">
                            <span class="stat-label">Nodes:</span>
                            <span class="stat-value">${workflow.nodes_used ? workflow.nodes_used.length : 0}</span>
                        </div>
                        <div class="workflow-stat">
                            <span class="stat-label">Steps:</span>
                            <span class="stat-value">${workflow.workflow ? workflow.workflow.length : 0}</span>
                        </div>
                    </div>
                    <div class="workflow-actions">
                        <button class="workflow-btn" onclick="oneFlowChat.executeWorkflow(${JSON.stringify(workflow).replace(/"/g, '&quot;')})">
                            Apply to Canvas
                        </button>
                        <button class="workflow-btn secondary" onclick="oneFlowChat.showWorkflowDetails(${JSON.stringify(workflow).replace(/"/g, '&quot;')})">
                            View Details
                        </button>
                    </div>
                </div>
            `;
        }

        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <p>${content}</p>
                ${workflowHtml}
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Show notification badge if chat is closed
        if (!this.isOpen) {
            const badge = document.getElementById('chat-badge');
            badge.style.display = 'block';
        }
    }

    updateStatus(text, type = 'ready') {
        const statusText = document.getElementById('chat-status').querySelector('.status-text');
        const statusIndicator = document.getElementById('chat-status').querySelector('.status-indicator');
        
        statusText.textContent = text;
        statusIndicator.className = `status-indicator ${type}`;
    }

    async executeWorkflow(workflow) {
        if (!workflow || !workflow.workflow) {
            console.error('Invalid workflow data');
            return;
        }

        try {
            // Check if ComfyUI app is available
            if (typeof app !== 'undefined' && app.graph) {
                this.applyWorkflowToCanvas(workflow);
            } else {
                console.warn('ComfyUI app not available, workflow cannot be applied to canvas');
                this.addMessage('assistant', 'Workflow generated but cannot be applied to canvas. Please ensure ComfyUI is fully loaded.');
            }
        } catch (error) {
            console.error('Error executing workflow:', error);
            this.addMessage('assistant', 'Error applying workflow to canvas: ' + error.message);
        }
    }

    applyWorkflowToCanvas(workflow) {
        try {
            const operations = workflow.workflow;
            const nodeMap = new Map(); // Track created nodes by their workflow IDs
            
            // First pass: collect all add_node operations to assign proper IDs
            const addNodeOps = operations.filter(op => op.operation === 'add_node');
            let nextNodeId = this.getNextAvailableNodeId();
            
            // Create a mapping of node types to assigned IDs for this workflow
            const nodeTypeToId = new Map();
            addNodeOps.forEach((op, index) => {
                const nodeType = op.params.node_id;
                const assignedId = nextNodeId + index;
                nodeTypeToId.set(nodeType, assignedId);
                console.log(`Assigning ID ${assignedId} to node type ${nodeType}`);
            });
            
            // Execute operations in sequence
            operations.forEach((operation, index) => {
                switch (operation.operation) {
                    case 'add_node':
                        const nodeType = operation.params.node_id;
                        const assignedId = nodeTypeToId.get(nodeType);
                        this.addNodeToCanvas(operation.params, nodeMap, assignedId);
                        break;
                    case 'link_node':
                        this.linkNodesOnCanvas(operation.params, nodeMap);
                        break;
                    case 'set_param':
                        this.setNodeParam(operation.params, nodeMap);
                        break;
                    default:
                        console.warn('Unknown operation:', operation.operation);
                }
            });

            // Arrange nodes nicely
            this.arrangeNodes();
            
            this.addMessage('assistant', 'Workflow has been applied to the canvas! You can now execute it or modify the nodes as needed.');
            
        } catch (error) {
            console.error('Error applying workflow to canvas:', error);
            this.addMessage('assistant', 'Error applying workflow to canvas: ' + error.message);
        }
    }

    addNodeToCanvas(params, nodeMap, assignedNodeId = null) {
        if (!app || !app.graph) return;

        try {
            // Create node using ComfyUI's node creation system
            const nodeType = params.node_id;
            const position = params.position || { x: 100, y: 100 };
            
            // Use ComfyUI's LiteGraph to create the node
            const node = LiteGraph.createNode(nodeType);
            if (!node) {
                console.error('Failed to create node:', nodeType);
                return;
            }

            // Set position
            node.pos = [position.x, position.y];
            
            // Assign specific node ID if provided
            if (assignedNodeId !== null) {
                node.id = assignedNodeId;
            }
            
            // Set node parameters if provided
            if (params.node_params) {
                Object.entries(params.node_params).forEach(([key, value]) => {
                    if (node.widgets) {
                        const widget = node.widgets.find(w => w.name === key);
                        if (widget) {
                            widget.value = value;
                        }
                    }
                });
            }

            // Add node to graph
            app.graph.add(node);
            
            // Store node reference using both the node type and the actual node ID
            // This allows the AI to reference it by either identifier in link_node operations
            nodeMap.set(nodeType, node);
            nodeMap.set(String(node.id), node);
            
            console.log('Added node to canvas:', nodeType, 'with ID:', node.id);
            
        } catch (error) {
            console.error('Error adding node to canvas:', error);
        }
    }

    linkNodesOnCanvas(params, nodeMap) {
        if (!app || !app.graph) return;

        try {
            console.log('Attempting to link nodes:', params);
            console.log('Available nodes in nodeMap:', Array.from(nodeMap.keys()));
            console.log('Existing canvas nodes:', app.graph.nodes.map(n => `${n.id}:${n.type}`));
            
            // Find source node (check nodeMap first, then existing canvas nodes)
            let sourceNode = nodeMap.get(params.source_node_id);
            if (!sourceNode) {
                // Look for existing node on canvas by ID
                sourceNode = this.findExistingNodeById(params.source_node_id);
                console.log('Found existing source node:', sourceNode ? `${sourceNode.id}:${sourceNode.type}` : 'none');
            } else {
                console.log('Found source node in nodeMap:', `${sourceNode.id}:${sourceNode.type}`);
            }
            
            // Find target node (check nodeMap first, then existing canvas nodes)
            let targetNode = nodeMap.get(params.target_node_id);
            if (!targetNode) {
                // Look for existing node on canvas by ID
                targetNode = this.findExistingNodeById(params.target_node_id);
                console.log('Found existing target node:', targetNode ? `${targetNode.id}:${targetNode.type}` : 'none');
            } else {
                console.log('Found target node in nodeMap:', `${targetNode.id}:${targetNode.type}`);
            }
            
            if (!sourceNode || !targetNode) {
                console.error('Source or target node not found for linking:', {
                    source_id: params.source_node_id,
                    target_id: params.target_node_id,
                    sourceFound: !!sourceNode,
                    targetFound: !!targetNode,
                    nodeMapKeys: Array.from(nodeMap.keys()),
                    canvasNodes: app.graph.nodes.map(n => `${n.id}:${n.type}`)
                });
                return;
            }

            // Find output and input slots
            const outputSlot = sourceNode.findOutputSlot(params.source_output);
            const inputSlot = targetNode.findInputSlot(params.target_input);
            
            console.log('Slot lookup:', {
                source_output: params.source_output,
                target_input: params.target_input,
                outputSlot,
                inputSlot,
                sourceOutputs: sourceNode.outputs?.map(o => o.name) || [],
                targetInputs: targetNode.inputs?.map(i => i.name) || []
            });
            
            if (outputSlot !== -1 && inputSlot !== -1) {
                sourceNode.connect(outputSlot, targetNode, inputSlot);
                console.log('✅ Successfully connected nodes:', params.source_node_id, '->', params.target_node_id);
            } else {
                console.error('Could not find slots for connection:', {
                    source_output: params.source_output,
                    target_input: params.target_input,
                    outputSlot,
                    inputSlot,
                    sourceOutputs: sourceNode.outputs?.map(o => o.name) || [],
                    targetInputs: targetNode.inputs?.map(i => i.name) || []
                });
            }
            
        } catch (error) {
            console.error('Error linking nodes on canvas:', error);
        }
    }

    findExistingNodeById(nodeId) {
        /**
         * Find an existing node on the canvas by its ID
         * This handles both string and numeric IDs
         */
        if (!app || !app.graph || !app.graph.nodes) return null;
        
        try {
            // Convert nodeId to string for comparison
            const searchId = String(nodeId);
            
            // Search through existing nodes
            for (const node of app.graph.nodes) {
                if (node && (String(node.id) === searchId || String(node.title) === searchId)) {
                    console.log('Found existing node:', nodeId, node);
                    return node;
                }
            }
            
            console.log('Existing node not found:', nodeId);
            return null;
        } catch (error) {
            console.error('Error finding existing node:', error);
            return null;
        }
    }

    getNextAvailableNodeId() {
        /**
         * Get the next available node ID for new nodes
         */
        if (!app || !app.graph || !app.graph.nodes) return 1;
        
        let maxId = 0;
        for (const node of app.graph.nodes) {
            if (node && node.id && !isNaN(node.id)) {
                maxId = Math.max(maxId, parseInt(node.id));
            }
        }
        return maxId + 1;
    }

    setNodeParam(params, nodeMap) {
        /**
         * Set a parameter on an existing node
         */
        if (!app || !app.graph) return;

        try {
            // Find the node (check nodeMap first, then existing canvas nodes)
            let node = nodeMap.get(params.node_id);
            if (!node) {
                node = this.findExistingNodeById(params.node_id);
            }

            if (!node) {
                console.error('Node not found for set_param:', params.node_id);
                return;
            }

            // Set the parameter
            if (node.widgets) {
                const widget = node.widgets.find(w => w.name === params.param_name);
                if (widget) {
                    widget.value = params.param_value;
                    console.log('Set parameter:', params.param_name, '=', params.param_value);
                } else {
                    console.error('Widget not found:', params.param_name);
                }
            }

        } catch (error) {
            console.error('Error setting node parameter:', error);
        }
    }

    arrangeNodes() {
        if (!app || !app.graph) return;

        try {
            // Simple auto-arrangement of nodes
            app.graph.arrange();
        } catch (error) {
            console.warn('Auto-arrange not available');
        }
    }

    showWorkflowDetails(workflow) {
        const details = workflow.workflow.map((op, i) => 
            `${i + 1}. ${op.operation}: ${JSON.stringify(op.params, null, 2)}`
        ).join('\n\n');
        
        alert(`Workflow Details:\n\n${details}`);
    }

    async loadChatHistory() {
        try {
            const response = await fetch('/api/chat/history');
            const result = await response.json();
            
            if (result.success && result.history && result.history.length > 0) {
                // Load recent chat history
                result.history.slice(-5).forEach(entry => {
                    this.addMessage('user', entry.user_request);
                    if (entry.result.success) {
                        this.addMessage('assistant', 'Workflow generated', entry.result.workflow);
                    } else {
                        this.addMessage('assistant', `Error: ${entry.result.error}`);
                    }
                });
            }
        } catch (error) {
            console.warn('Could not load chat history:', error);
        }
    }

    getCurrentWorkflow() {
        /**
         * Extract current workflow from ComfyUI canvas
         * This method attempts to access the ComfyUI app instance and extract the current workflow
         */
        try {
            // Try to access ComfyUI's app instance
            if (window.app && window.app.graph) {
                const graph = window.app.graph;
                const workflow = {
                    nodes: {},
                    links: []
                };

                // Extract nodes
                if (graph.nodes) {
                    graph.nodes.forEach((node, index) => {
                        if (node) {
                            workflow.nodes[node.id || index] = {
                                id: node.id || index,
                                class_type: node.type || node.comfyClass || 'Unknown',
                                inputs: {},
                                outputs: {},
                                properties: node.properties || {},
                                widgets_values: node.widgets_values || []
                            };

                            // Extract input values from widgets
                            if (node.widgets) {
                                node.widgets.forEach((widget, widgetIndex) => {
                                    if (widget && widget.name) {
                                        workflow.nodes[node.id || index].inputs[widget.name] = widget.value;
                                    }
                                });
                            }
                        }
                    });
                }

                // Extract links/connections
                if (graph.links) {
                    Object.values(graph.links).forEach(link => {
                        if (link) {
                            workflow.links.push([
                                link.id,
                                link.origin_id,
                                link.origin_slot,
                                link.target_id,
                                link.target_slot,
                                link.type || 'unknown'
                            ]);
                        }
                    });
                }

                console.log('OneFlow Chat: Extracted current workflow:', workflow);
                return workflow;
            }

            // Fallback: try to access through other possible global variables
            if (window.litegraph && window.litegraph.LGraph) {
                console.log('OneFlow Chat: Trying LiteGraph fallback...');
                // Additional fallback logic could go here
            }

            console.log('OneFlow Chat: No current workflow found');
            return null;

        } catch (error) {
            console.warn('OneFlow Chat: Error extracting current workflow:', error);
            return null;
        }
    }
}

// Initialize chat widget when DOM is ready
function initOneFlowChat() {
    console.log('OneFlow Chat Widget: initOneFlowChat called, document.readyState:', document.readyState);
    if (document.readyState === 'loading') {
        console.log('OneFlow Chat Widget: Document still loading, adding DOMContentLoaded listener');
        document.addEventListener('DOMContentLoaded', () => {
            console.log('OneFlow Chat Widget: DOMContentLoaded fired, creating widget');
            window.oneFlowChat = new OneFlowChatWidget();
        });
    } else {
        console.log('OneFlow Chat Widget: Document ready, creating widget immediately');
        window.oneFlowChat = new OneFlowChatWidget();
    }
}

// Auto-initialize
console.log('OneFlow Chat Widget: Script loaded, calling initOneFlowChat');
initOneFlowChat();