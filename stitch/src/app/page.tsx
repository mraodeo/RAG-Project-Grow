"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Send, AlertTriangle, Building, MessageSquare, Loader2, Info } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatApp() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const examples = [
    "What is the expense ratio of HDFC Large Cap Fund?",
    "What is the exit load for HDFC ELSS Tax Saver Fund?",
    "Minimum SIP amount for HDFC Small Cap Fund?",
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Send request to our FastAPI backend (proxied via next.config.mjs)
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: text }),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch response");
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error connecting to the server.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-slate-100 font-sans">
      
      {/* Header */}
      <header className="sticky top-0 z-10 p-4 border-b border-slate-800/50 bg-slate-900/40 backdrop-blur-md">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/20 rounded-xl border border-indigo-500/30">
              <Building className="w-6 h-6 text-indigo-400" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">
              Mutual Fund FAQ Assistant
            </h1>
          </div>
          
          <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-500/10 border border-amber-500/20 rounded-full">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            <span className="text-xs font-medium text-amber-500/90 tracking-wide">
              FACTS ONLY. NO INVESTMENT ADVICE.
            </span>
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar">
        <div className="max-w-4xl mx-auto space-y-6 pb-24">
          
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center min-h-[60vh] text-center animate-in fade-in duration-700 zoom-in-95">
              <div className="w-20 h-20 bg-indigo-500/10 rounded-full flex items-center justify-center mb-6 border border-indigo-500/20 shadow-xl shadow-indigo-500/10">
                <MessageSquare className="w-10 h-10 text-indigo-400" />
              </div>
              <h2 className="text-3xl font-bold text-slate-200 mb-4">How can I help you today?</h2>
              <p className="text-slate-400 max-w-md mb-10 leading-relaxed">
                I can answer factual questions about HDFC mutual fund schemes, expense ratios, exit loads, and NAV details.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl">
                {examples.map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => sendMessage(example)}
                    className="group flex flex-col items-start text-left p-4 rounded-2xl bg-slate-800/30 border border-slate-700/50 hover:bg-slate-800/60 hover:border-indigo-500/50 transition-all duration-300 backdrop-blur-sm"
                  >
                    <Info className="w-5 h-5 text-indigo-400 mb-3 group-hover:scale-110 transition-transform" />
                    <span className="text-sm text-slate-300 leading-snug font-medium">{example}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[85%] md:max-w-[75%] rounded-3xl p-5 ${
                      msg.role === "user"
                        ? "bg-indigo-600/90 text-white shadow-lg shadow-indigo-900/20 rounded-tr-sm"
                        : "bg-slate-800/60 border border-slate-700/50 text-slate-200 backdrop-blur-md rounded-tl-sm prose prose-invert prose-p:leading-relaxed prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-700"
                    }`}
                  >
                    {msg.role === "user" ? (
                      msg.content
                    ) : (
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    )}
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-slate-800/60 border border-slate-700/50 backdrop-blur-md rounded-3xl rounded-tl-sm p-5 flex items-center gap-3">
                    <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
                    <span className="text-sm font-medium text-slate-400 animate-pulse">Searching knowledge base...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </main>

      {/* Input Area */}
      <div className="fixed bottom-0 w-full p-4 bg-gradient-to-t from-slate-950 via-slate-950/90 to-transparent pt-10">
        <div className="max-w-4xl mx-auto relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about HDFC mutual funds..."
            disabled={isLoading}
            className="w-full bg-slate-900/60 border border-slate-700/50 text-slate-200 rounded-full pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all backdrop-blur-xl shadow-2xl placeholder:text-slate-500 disabled:opacity-50"
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || isLoading}
            className="absolute right-2 top-2 p-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white rounded-full transition-all duration-200 shadow-md flex items-center justify-center disabled:cursor-not-allowed group"
          >
            <Send className="w-5 h-5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </button>
        </div>
        <p className="text-center text-xs text-slate-500 mt-3 font-medium">
          Answers are generated by AI and may not be perfect. Verify important data.
        </p>
      </div>
    </div>
  );
}
