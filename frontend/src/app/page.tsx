"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { 
  ArrowUp, 
  AlertTriangle, 
  Landmark, 
  MessageSquare, 
  Loader2, 
  Settings, 
  PanelLeft, 
  Bot,
  BarChart3,
  Banknote,
  ArrowRightLeft
} from "lucide-react";

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
    {
      icon: <BarChart3 className="w-5 h-5 text-slate-400" />,
      text: "What is the expense ratio of HDFC Large Cap Fund?"
    },
    {
      icon: <Landmark className="w-5 h-5 text-slate-400" />,
      text: "What is the exit load for HDFC ELSS Tax Saver Fund?"
    },
    {
      icon: <Banknote className="w-5 h-5 text-slate-400" />,
      text: "Minimum SIP amount for HDFC Small Cap Fund?"
    },
    {
      icon: <ArrowRightLeft className="w-5 h-5 text-slate-400" />,
      text: "Compare HDFC Mid Cap vs Large Cap"
    }
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
    <div className="flex flex-col h-screen bg-[#0B1420] text-slate-100 font-sans">
      
      {/* Header */}
      <header className="flex flex-col">
        <div className="flex items-center justify-between p-4 bg-[#0B1420]">
          <div className="flex items-center gap-4">
            <button className="p-1 hover:bg-[#172132] rounded-md transition-colors text-slate-300">
              <PanelLeft className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <Landmark className="w-6 h-6 text-slate-200" />
              <h1 className="text-xl font-bold text-white tracking-tight leading-tight">
                Mutual Fund FAQ<br/>Assistant
              </h1>
            </div>
          </div>
          <button className="p-2 hover:bg-[#172132] rounded-full transition-colors text-slate-300">
            <Settings className="w-5 h-5" />
          </button>
        </div>
        
        {/* Warning Banner */}
        <div className="bg-[#D1AD3B] py-2 px-4 flex items-center justify-center gap-2 w-full">
          <AlertTriangle className="w-4 h-4 text-[#0B1420]" />
          <AlertTriangle className="w-4 h-4 text-[#0B1420] text-opacity-70" />
          <span className="text-sm font-semibold text-[#0B1420] tracking-wide">
            Facts-only. No investment advice.
          </span>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar flex flex-col">
        <div className="max-w-2xl mx-auto w-full flex-1 flex flex-col pb-6">
          
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center flex-1 py-10 animate-in fade-in duration-500">
              <div className="w-16 h-16 bg-[#1F2B3D] rounded-full flex items-center justify-center mb-6">
                <Bot className="w-8 h-8 text-[#BDE7E0]" />
              </div>
              <h2 className="text-lg font-medium text-slate-200 mb-2">Hello! How can I help you today?</h2>
              <p className="text-[#94A3B8] text-center max-w-sm mb-10 leading-relaxed text-sm">
                Ask me facts about HDFC Mutual Funds, expense ratios, exit loads, or compare funds.
              </p>
              
              <div className="w-full space-y-3">
                {examples.map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => sendMessage(example.text)}
                    className="w-full flex items-center gap-4 text-left p-4 rounded-xl bg-[#172132] border border-[#26334A] hover:bg-[#1F2B3D] transition-colors"
                  >
                    <div className="shrink-0">
                      {example.icon}
                    </div>
                    <span className="text-sm text-slate-200 font-medium leading-snug">
                      {example.text}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6 flex-1">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl p-4 ${
                      msg.role === "user"
                        ? "bg-[#172132] border border-[#26334A] text-slate-200"
                        : "bg-transparent text-slate-200 prose prose-invert prose-p:leading-relaxed prose-pre:bg-[#172132] prose-pre:border prose-pre:border-[#26334A]"
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
                  <div className="bg-transparent text-slate-200 p-4 flex items-center gap-3">
                    <Loader2 className="w-5 h-5 text-[#BDE7E0] animate-spin" />
                    <span className="text-sm font-medium text-slate-400">Thinking...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </main>

      {/* Input Area */}
      <div className="w-full p-4 bg-[#0B1420]">
        <div className="max-w-2xl mx-auto relative flex flex-col items-center">
          <div className="relative w-full">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about HDFC Mutual Funds..."
              disabled={isLoading}
              className="w-full bg-[#172132] border border-[#26334A] text-slate-200 rounded-xl pl-4 pr-14 py-4 focus:outline-none focus:border-[#475E82] transition-colors placeholder:text-[#64748B] disabled:opacity-50 text-sm"
            />
            <button
              onClick={() => sendMessage(input)}
              disabled={!input.trim() || isLoading}
              className="absolute right-2 top-2 bottom-2 aspect-square bg-[#BDE7E0] hover:bg-[#A3D9D0] disabled:bg-[#1F2B3D] disabled:text-[#475E82] text-[#0B1420] rounded-lg transition-colors flex items-center justify-center disabled:cursor-not-allowed"
            >
              <ArrowUp className="w-5 h-5" />
            </button>
          </div>
          <p className="text-center text-[11px] text-[#64748B] mt-3 max-w-sm">
            AI may produce inaccurate information about financial products.
          </p>
        </div>
      </div>
    </div>
  );
}
