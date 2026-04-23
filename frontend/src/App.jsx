import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Bot, User, Shield, MessageSquare, History, Plus } from 'lucide-react';


const App = () => {
    const [messages, setMessages] = useState([
        { id: 1, text: "Hello! I am your AI Support Assistant. How can I help you today?", sender: 'bot' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [isEscalated, setIsEscalated] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMsg = { id: Date.now(), text: input, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const response = await axios.post('/api/chat', { query: input });
            const botMsg = {
                id: Date.now() + 1,
                text: response.data.response,
                sender: 'bot',
                needsConfirmation: response.data.needs_confirmation
            };

            setMessages(prev => [...prev, botMsg]);
            setIsEscalated(response.data.escalated);
        } catch (error) {
            console.error("Error sending message:", error);
            setMessages(prev => [...prev, {
                id: Date.now() + 1,
                text: "Sorry, I encountered an error. Please try again later.",
                sender: 'bot'
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleChoice = (choice) => {
        if (choice === 'human') {
            const userMsg = { id: Date.now(), text: "I'd like to speak with a human agent.", sender: 'user' };
            setMessages(prev => {
                const updated = prev.map(m => ({ ...m, needsConfirmation: false }));
                return [...updated, userMsg];
            });
            setIsEscalated(true);
            setTimeout(() => {
                simulateHumanResponse();
            }, 1000);
        } else {
            const userMsg = { id: Date.now(), text: "No thanks, I'll continue with the Bot.", sender: 'user' };
            setMessages(prev => {
                const updated = prev.map(m => ({ ...m, needsConfirmation: false }));
                return [...updated, userMsg, {
                    id: Date.now() + 1,
                    text: "Sure thing! How else can I assist you today?",
                    sender: 'bot'
                }];
            });
        }
    };

    const simulateHumanResponse = () => {
        const humanMsg = {
            id: Date.now(),
            text: "Hello, I am a Human Support Agent. I have reviewed your request and will assist you further.",
            sender: 'bot',
            isHuman: true
        };
        setMessages(prev => [...prev, humanMsg]);
        setIsEscalated(false);
    };

    const startNewChat = () => {
        setMessages([
            { id: 1, text: "Hello! I am your AI Support Assistant. How can I help you today?", sender: 'bot' }
        ]);
        setIsEscalated(false);
        setInput('');
    };

    const renderContent = (text) => {
        if (!text) return null;

        // Split by lines and handle simple markdown
        return text.split('\n').map((line, i) => {
            let processedLine = line;

            // Handle Bold (**text**)
            const boldRegex = /\*\*(.*?)\*\*/g;
            const parts = [];
            let lastIndex = 0;
            let match;

            while ((match = boldRegex.exec(processedLine)) !== null) {
                parts.push(processedLine.substring(lastIndex, match.index));
                parts.push(<strong key={match.index}>{match[1]}</strong>);
                lastIndex = boldRegex.lastIndex;
            }
            parts.push(processedLine.substring(lastIndex));

            // Handle Bullet Points
            if (line.trim().startsWith('- ')) {
                return (
                    <li key={i} style={{ marginLeft: '1rem', listStyleType: 'disc', marginBottom: '0.25rem' }}>
                        {parts.map((p, idx) => typeof p === 'string' ? p.replace('- ', '') : p)}
                    </li>
                );
            }

            // Handle Numbered Lists
            const numMatch = line.trim().match(/^\d+\.\s/);
            if (numMatch) {
                return (
                    <div key={i} style={{ marginLeft: '1rem', marginBottom: '0.5rem', display: 'flex', gap: '0.5rem' }}>
                        <span style={{ fontWeight: 'bold' }}>{numMatch[0]}</span>
                        <span>{parts.map((p, idx) => typeof p === 'string' ? p.replace(numMatch[0], '') : p)}</span>
                    </div>
                );
            }

            return <p key={i} style={{ marginBottom: '0.75rem' }}>{parts}</p>;
        });
    };

    return (
        <div className="app-container">
            <aside className="sidebar">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '2rem' }}>
                    <Shield color="#6366f1" size={24} />
                    <h2 style={{ fontSize: '1.25rem' }}>RAG Support Bot</h2>
                </div>

                <button
                    onClick={startNewChat}
                    style={{
                        background: 'var(--primary)',
                        border: 'none',
                        color: 'white',
                        padding: '0.75rem',
                        borderRadius: '8px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.5rem',
                        cursor: 'pointer',
                        marginBottom: '2rem'
                    }}>
                    <Plus size={18} /> New Chat
                </button>

                <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', paddingLeft: '0.5rem', marginBottom: '1rem' }}>RECENT TICKETS</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {[1, 2, 3].map(i => (
                        <div key={i} style={{
                            padding: '0.75rem',
                            background: 'var(--glass)',
                            borderRadius: '8px',
                            fontSize: '0.9rem',
                            border: '1px solid var(--glass-border)',
                            cursor: 'pointer'
                        }}>
                            Ticket #324{i} - Billing Issue
                        </div>
                    ))}
                </div>
            </aside>

            <main className="chat-section">
                <header className="header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#22c55e' }}></div>
                        <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>AI Agent Online</span>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <MessageSquare size={20} color="var(--text-muted)" />
                        <History size={20} color="var(--text-muted)" />
                    </div>
                </header>

                {isEscalated && (
                    <div className="status-banner" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span>⚠️ Human Agent Intervention Required</span>
                        <button
                            onClick={simulateHumanResponse}
                            style={{
                                background: 'white',
                                color: 'black',
                                border: 'none',
                                padding: '4px 12px',
                                borderRadius: '4px',
                                fontSize: '0.8rem',
                                cursor: 'pointer'
                            }}
                        >
                            Simulate Response
                        </button>
                    </div>
                )}

                <div className="messages">
                    {messages.map((msg) => (
                        <div key={msg.id} className={`message ${msg.sender} ${msg.isHuman ? 'human' : ''}`}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '4px' }}>
                                {msg.sender === 'bot' ? <Bot size={16} color={msg.isHuman ? "#c0c1ff" : "#6366f1"} /> : <User size={16} />}
                                <span style={{ fontSize: '0.7rem', opacity: 0.6, fontWeight: 'bold' }}>
                                    {msg.sender === 'bot' ? (msg.isHuman ? 'HUMAN AGENT' : 'AI ASSISTANT') : 'YOU'}
                                </span>
                            </div>
                            {msg.sender === 'bot' ? (
                                <div className="formatted-message">
                                    {renderContent(msg.text)}
                                    {msg.needsConfirmation && (
                                        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                                            <button
                                                onClick={() => handleChoice('human')}
                                                style={{
                                                    padding: '0.5rem 1rem',
                                                    borderRadius: '6px',
                                                    border: 'none',
                                                    background: 'var(--primary)',
                                                    color: 'white',
                                                    fontSize: '0.8rem',
                                                    cursor: 'pointer'
                                                }}
                                            >
                                                Talk to Human
                                            </button>
                                            <button
                                                onClick={() => handleChoice('ai')}
                                                style={{
                                                    padding: '0.5rem 1rem',
                                                    borderRadius: '6px',
                                                    border: '1px solid var(--glass-border)',
                                                    background: 'var(--glass)',
                                                    color: 'white',
                                                    fontSize: '0.8rem',
                                                    cursor: 'pointer'
                                                }}
                                            >
                                                Continue with Bot
                                            </button>
                                        </div>
                                    )}
                                </div>
                            ) : msg.text}
                        </div>
                    ))}
                    {loading && (
                        <div className="message bot">
                            <div className="loading">
                                <div className="dot"></div>
                                <div className="dot"></div>
                                <div className="dot"></div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <div className="input-area">
                    <form onSubmit={handleSend} className="input-container">
                        <input
                            type="text"
                            placeholder="Query the assistance..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={loading || isEscalated}
                        />
                        <button type="submit" className="send-btn" disabled={loading || isEscalated}>
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default App;
